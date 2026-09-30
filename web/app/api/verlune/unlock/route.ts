import { NextRequest, NextResponse } from "next/server";

import { safePremiumNextPath } from "@/lib/verlune-auth.server";
import {
  getVerluneMercadoPagoConfigState,
  MercadoPagoApiError,
  readMercadoPagoPayment,
  verifyVerlunePremiumPayment
} from "@/lib/verlune-mercado-pago";
import {
  clearPremiumCookieOptions,
  newMercadoPagoPremiumSession,
  premiumCookieOptions,
  signPremiumSession,
  VERLUNE_DEVICE_COOKIE,
  VERLUNE_SESSION_COOKIE
} from "@/lib/verlune-session";

export const runtime = "nodejs";

export async function POST(request: NextRequest) {
  const config = getVerluneMercadoPagoConfigState();
  if (!config.ready) {
    return NextResponse.json({ ok: false, message: "Premium access is not configured on this deployment." }, { status: 503 });
  }

  const body = await request.json().catch(() => null) as
    | { paymentId?: unknown; email?: unknown; next?: unknown }
    | null;

  const paymentId = typeof body?.paymentId === "string" ? body.paymentId.trim() : "";
  const email = typeof body?.email === "string" ? body.email.trim().toLowerCase() : "";
  const nextPath = safePremiumNextPath(typeof body?.next === "string" ? body.next : "/app");

  if (!/^[1-9][0-9]{0,29}$/.test(paymentId) || !email || email.length > 254) {
    return NextResponse.json({ ok: false, message: "Enter the Mercado Pago payment ID and the email used at checkout." }, { status: 400 });
  }

  try {
    const payment = await readMercadoPagoPayment(paymentId);
    const verification = verifyVerlunePremiumPayment(payment, email);
    if (!verification.entitled) {
      return NextResponse.json({ ok: false, message: "That Mercado Pago payment does not match an active Verlune Premium purchase." }, { status: 401 });
    }

    const session = newMercadoPagoPremiumSession({
      paymentId: verification.paymentId,
      customerEmail: verification.customerEmail
    });
    const response = NextResponse.json({ ok: true, redirect: nextPath });
    response.cookies.set(VERLUNE_SESSION_COOKIE, signPremiumSession(session), premiumCookieOptions(session));
    response.cookies.set(VERLUNE_DEVICE_COOKIE, "", clearPremiumCookieOptions);
    return response;
  } catch (error) {
    if (error instanceof MercadoPagoApiError && (error.status === 400 || error.status === 404)) {
      return NextResponse.json({ ok: false, message: "That Mercado Pago payment could not be verified." }, { status: 401 });
    }
    return NextResponse.json({ ok: false, message: "Premium access could not be verified right now. Please try again." }, { status: 502 });
  }
}
