import { randomUUID } from "node:crypto";
import { NextRequest, NextResponse } from "next/server";

import {
  allowVerluneRecoveryEmail,
  createVerluneAccessKey,
  entitlementMatchesEmail,
  getVerluneAccessConfigState,
  getVerlunePremiumEntitlementByEmail,
  isValidVerluneEmail,
  normalizeVerluneEmail,
  sendVerluneAccessEmail,
  syncVerlunePremiumEntitlement,
  VerluneAccessError
} from "@/lib/verlune-access";
import {
  getVerluneMercadoPagoConfigState,
  MercadoPagoApiError,
  readMercadoPagoPayment,
  verifyVerlunePremiumPayment
} from "@/lib/verlune-mercado-pago";

export const runtime = "nodejs";

function accepted() {
  return NextResponse.json({
    ok: true,
    message: "If that email has an active Verlune Premium purchase, its existing Access Key will be sent again."
  }, { status: 202 });
}

export async function POST(request: NextRequest) {
  const access = getVerluneAccessConfigState();
  const provider = getVerluneMercadoPagoConfigState();
  if (!access.ready || !provider.ready) {
    return NextResponse.json({ ok: false, message: "Access-key recovery is temporarily unavailable." }, { status: 503 });
  }

  const body = await request.json().catch(() => null) as { email?: unknown } | null;
  const email = normalizeVerluneEmail(body?.email);
  if (!isValidVerluneEmail(email)) return accepted();

  try {
    const entitlement = await getVerlunePremiumEntitlementByEmail(email);
    if (!entitlement || entitlement.status !== "active" || !entitlementMatchesEmail(entitlement, email)) return accepted();
    if (!await allowVerluneRecoveryEmail(entitlement.entitlementId)) return accepted();

    const payment = await readMercadoPagoPayment(entitlement.paymentId);
    const verification = verifyVerlunePremiumPayment(payment, email);
    const refreshed = await syncVerlunePremiumEntitlement(verification);
    if (!verification.entitled || !refreshed || refreshed.status !== "active") return accepted();

    await sendVerluneAccessEmail({
      email,
      accessKey: createVerluneAccessKey(email),
      entitlementId: refreshed.entitlementId,
      reason: "recovery",
      idempotencyKey: `verlune-access-recovery/${refreshed.entitlementId}/${randomUUID()}`
    });
    return accepted();
  } catch (error) {
    if (error instanceof MercadoPagoApiError || error instanceof VerluneAccessError) {
      return NextResponse.json({ ok: false, message: "Access-key recovery is temporarily unavailable." }, { status: 503 });
    }
    return NextResponse.json({ ok: false, message: "Access-key recovery is temporarily unavailable." }, { status: 502 });
  }
}
