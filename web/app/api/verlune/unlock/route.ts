import { NextRequest, NextResponse } from "next/server";

import { safePremiumNextPath } from "@/lib/verlune-auth.server";
import {
  entitlementMatchesEmail,
  getVerluneEntitlementConfigState,
  getVerlunePremiumEntitlementByEmail,
  isValidVerluneEmail,
  normalizeVerluneEmail,
  syncVerlunePremiumEntitlement,
  verifyVerluneAccessKey,
  VerluneAccessError
} from "@/lib/verlune-access";
import {
  getVerluneMercadoPagoConfigState,
  MercadoPagoApiError,
  readMercadoPagoPayment,
  verifyVerlunePremiumPayment
} from "@/lib/verlune-mercado-pago";
import {
  clearPremiumCookieOptions,
  newAccessKeyPremiumSession,
  premiumCookieOptions,
  signPremiumSession,
  VERLUNE_DEVICE_COOKIE,
  VERLUNE_SESSION_COOKIE
} from "@/lib/verlune-session";

export const runtime = "nodejs";

export async function POST(request: NextRequest) {
  const access = getVerluneEntitlementConfigState();
  const provider = getVerluneMercadoPagoConfigState();
  if (!access.ready || !provider.ready) {
    return NextResponse.json({ ok: false, message: "Premium access is not configured on this deployment." }, { status: 503 });
  }

  const body = await request.json().catch(() => null) as
    | { accessKey?: unknown; email?: unknown; next?: unknown }
    | null;

  const email = normalizeVerluneEmail(body?.email);
  const accessKey = typeof body?.accessKey === "string" ? body.accessKey.trim() : "";
  const nextPath = safePremiumNextPath(typeof body?.next === "string" ? body.next : "/app");

  if (!isValidVerluneEmail(email) || !verifyVerluneAccessKey(email, accessKey)) {
    return NextResponse.json({ ok: false, message: "That email and Verlune Access Key do not match an active Premium purchase." }, { status: 401 });
  }

  try {
    const entitlement = await getVerlunePremiumEntitlementByEmail(email);
    if (!entitlement || entitlement.status !== "active" || !entitlementMatchesEmail(entitlement, email)) {
      return NextResponse.json({ ok: false, message: "That email and Verlune Access Key do not match an active Premium purchase." }, { status: 401 });
    }

    const payment = await readMercadoPagoPayment(entitlement.paymentId);
    const verification = verifyVerlunePremiumPayment(payment, email);
    const refreshedEntitlement = await syncVerlunePremiumEntitlement(verification);
    if (!verification.entitled || !refreshedEntitlement || refreshedEntitlement.status !== "active") {
      return NextResponse.json({ ok: false, message: "That Premium purchase is not currently active." }, { status: 401 });
    }

    const session = newAccessKeyPremiumSession({
      entitlementId: refreshedEntitlement.entitlementId,
      customerEmail: verification.customerEmail
    });
    const response = NextResponse.json({ ok: true, redirect: nextPath });
    response.cookies.set(VERLUNE_SESSION_COOKIE, signPremiumSession(session), premiumCookieOptions(session));
    response.cookies.set(VERLUNE_DEVICE_COOKIE, "", clearPremiumCookieOptions);
    return response;
  } catch (error) {
    if (error instanceof MercadoPagoApiError && (error.status === 400 || error.status === 404)) {
      return NextResponse.json({ ok: false, message: "That Premium purchase could not be verified." }, { status: 401 });
    }
    if (error instanceof MercadoPagoApiError || error instanceof VerluneAccessError) {
      return NextResponse.json({ ok: false, message: "Premium access could not be verified right now. Please try again." }, { status: 502 });
    }
    return NextResponse.json({ ok: false, message: "Premium access could not be verified right now. Please try again." }, { status: 502 });
  }
}
