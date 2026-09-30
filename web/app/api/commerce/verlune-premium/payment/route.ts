import { NextRequest, NextResponse } from "next/server";

import { currentCommerceMode } from "@/lib/commerce-mode";
import {
  createVerlunePremiumPayment,
  getVerluneMercadoPagoConfigState,
  MercadoPagoApiError
} from "@/lib/verlune-mercado-pago";
import {
  clearPremiumCookieOptions,
  newMercadoPagoPremiumSession,
  premiumCookieOptions,
  signPremiumSession,
  VERLUNE_DEVICE_COOKIE,
  VERLUNE_SESSION_COOKIE
} from "@/lib/verlune-session";
import {
  premiumTestSessionMatches,
  VERLUNE_PREMIUM_TEST_SESSION_COOKIE
} from "@/lib/verlune-premium-test-session";

export const runtime = "nodejs";

function cookieValue(request: Request, name: string): string | null {
  const cookie = request.headers.get("cookie");
  if (!cookie) return null;
  for (const pair of cookie.split(";")) {
    const [key, ...rest] = pair.trim().split("=");
    if (key === name) return decodeURIComponent(rest.join("="));
  }
  return null;
}

export async function POST(request: NextRequest) {
  const mode = currentCommerceMode("VERLUNE_PREMIUM_COMMERCE_MODE");
  const publicSaleLive = process.env.VERLUNE_PREMIUM_PUBLIC_SALE_STATUS === "LIVE";
  const provider = getVerluneMercadoPagoConfigState();

  if (mode === "off") {
    return NextResponse.json({ ok: false, error: "commerce_disabled" }, { status: 503 });
  }
  if (!provider.ready) {
    return NextResponse.json({ ok: false, error: "mercado_pago_not_configured", missing: provider.missing }, { status: 503 });
  }
  if (mode === "test") {
    if (publicSaleLive || provider.environment !== "test") {
      return NextResponse.json({ ok: false, error: "commerce_configuration_conflict" }, { status: 503 });
    }
    const authorized = premiumTestSessionMatches(cookieValue(request, VERLUNE_PREMIUM_TEST_SESSION_COOKIE));
    if (!authorized) return NextResponse.json({ ok: false, error: "provider_test_not_authorized" }, { status: 403 });
  } else {
    if (!publicSaleLive || provider.environment !== "live" || !provider.liveAllowed) {
      return NextResponse.json({ ok: false, error: "public_sale_not_ready" }, { status: 503 });
    }
  }

  const idempotencyKey = request.headers.get("x-idempotency-key") ?? "";
  const formData = await request.json().catch(() => null);
  const configuredWebhook = process.env.MP_NOTIFICATION_URL?.trim();
  const inferredWebhook = new URL("/api/commerce/mercado-pago/webhook", request.url).toString();
  const notificationUrl = configuredWebhook?.startsWith("https://")
    ? configuredWebhook
    : inferredWebhook.startsWith("https://")
      ? inferredWebhook
      : undefined;

  try {
    const payment = await createVerlunePremiumPayment({ formData, idempotencyKey, notificationUrl });
    const response = NextResponse.json({
      ok: true,
      paymentId: payment.paymentId,
      status: payment.status,
      paymentMethodId: payment.paymentMethodId,
      entitled: payment.entitled,
      redirect: payment.entitled ? "/app" : undefined
    });

    if (payment.entitled) {
      const session = newMercadoPagoPremiumSession({
        paymentId: payment.paymentId,
        customerEmail: payment.customerEmail
      });
      response.cookies.set(VERLUNE_SESSION_COOKIE, signPremiumSession(session), premiumCookieOptions(session));
      response.cookies.set(VERLUNE_DEVICE_COOKIE, "", clearPremiumCookieOptions);
    }

    console.info("VERLUNE_FUNNEL_EVENT", JSON.stringify({
      event: payment.entitled ? "premium_purchase_completed" : "premium_payment_updated",
      provider: "mercado_pago",
      payment_id: payment.paymentId,
      status: payment.status,
      commerce_mode: mode,
      timestamp: new Date().toISOString()
    }));

    return response;
  } catch (error) {
    if (error instanceof MercadoPagoApiError) {
      return NextResponse.json({ ok: false, error: error.code }, { status: error.status });
    }
    return NextResponse.json({ ok: false, error: "payment_unavailable" }, { status: 502 });
  }
}
