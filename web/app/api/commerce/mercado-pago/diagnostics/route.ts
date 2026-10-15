import { NextResponse } from "next/server";

import { currentCommerceMode } from "@/lib/commerce-mode";
import {
  getVerluneAccessConfigState,
  isValidVerluneEmail,
  normalizeVerluneEmail,
  provisionVerlunePremiumAccess,
  VerluneAccessError
} from "@/lib/verlune-access";
import {
  diagnoseVerluneMercadoPagoTestCredentials,
  getVerluneMercadoPagoConfigState,
  getVerluneMercadoPagoCoreConfigState,
  MercadoPagoApiError,
  readMercadoPagoPayment,
  verifyVerlunePremiumPayment
} from "@/lib/verlune-mercado-pago";
import { providerTestTokenMatches } from "@/lib/verlune-premium-test-session";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";

function bearerToken(request: Request): string {
  const value = request.headers.get("authorization") ?? "";
  const match = /^Bearer\s+(.+)$/i.exec(value);
  return match?.[1]?.trim() ?? "";
}

export async function GET(request: Request) {
  const mode = currentCommerceMode("VERLUNE_PREMIUM_COMMERCE_MODE");
  const publicSaleLive = process.env.VERLUNE_PREMIUM_PUBLIC_SALE_STATUS === "LIVE";
  const core = getVerluneMercadoPagoCoreConfigState();

  if (mode !== "test" || publicSaleLive || core.environment !== "test") {
    return NextResponse.json({ ok: false, error: "diagnostics_not_available" }, {
      status: 404,
      headers: { "Cache-Control": "no-store" }
    });
  }

  if (!providerTestTokenMatches(bearerToken(request))) {
    return NextResponse.json({ ok: false, error: "diagnostics_unauthorized" }, {
      status: 401,
      headers: { "Cache-Control": "no-store" }
    });
  }

  if (!core.ready) {
    return NextResponse.json({ ok: false, error: "mercado_pago_core_not_configured", missing: core.missing }, {
      status: 503,
      headers: { "Cache-Control": "no-store" }
    });
  }

  try {
    const diagnostics = await diagnoseVerluneMercadoPagoTestCredentials();
    return NextResponse.json({ ok: true, diagnostics }, {
      headers: { "Cache-Control": "no-store" }
    });
  } catch (error) {
    if (error instanceof MercadoPagoApiError) {
      return NextResponse.json({ ok: false, error: error.code }, {
        status: error.status,
        headers: { "Cache-Control": "no-store" }
      });
    }
    return NextResponse.json({ ok: false, error: "diagnostics_unavailable" }, {
      status: 502,
      headers: { "Cache-Control": "no-store" }
    });
  }
}


export async function POST(request: Request) {
  const mode = currentCommerceMode("VERLUNE_PREMIUM_COMMERCE_MODE");
  const publicSaleLive = process.env.VERLUNE_PREMIUM_PUBLIC_SALE_STATUS === "LIVE";
  const provider = getVerluneMercadoPagoConfigState();
  const access = getVerluneAccessConfigState();

  if (mode !== "test" || publicSaleLive || provider.environment !== "test") {
    return NextResponse.json({ ok: false, error: "diagnostics_not_available" }, {
      status: 404,
      headers: { "Cache-Control": "no-store" }
    });
  }

  if (!providerTestTokenMatches(bearerToken(request))) {
    return NextResponse.json({ ok: false, error: "diagnostics_unauthorized" }, {
      status: 401,
      headers: { "Cache-Control": "no-store" }
    });
  }

  if (!provider.ready || !access.ready) {
    return NextResponse.json({
      ok: false,
      error: "test_reconcile_not_configured",
      missing: [...new Set([...provider.missing, ...access.missing])]
    }, {
      status: 503,
      headers: { "Cache-Control": "no-store" }
    });
  }

  const body = await request.json().catch(() => null) as { paymentId?: unknown; email?: unknown } | null;
  const paymentId = typeof body?.paymentId === "string" ? body.paymentId.trim() : String(body?.paymentId ?? "").trim();
  const email = normalizeVerluneEmail(body?.email);

  if (!/^[1-9][0-9]{0,29}$/.test(paymentId) || !isValidVerluneEmail(email)) {
    return NextResponse.json({ ok: false, error: "invalid_test_reconcile_input" }, {
      status: 400,
      headers: { "Cache-Control": "no-store" }
    });
  }

  try {
    const payment = await readMercadoPagoPayment(paymentId);
    const verification = verifyVerlunePremiumPayment(payment, email);
    if (!verification.entitled) {
      return NextResponse.json({
        ok: false,
        error: "payment_not_entitled",
        status: verification.status,
        reason: verification.reason ?? null
      }, {
        status: 409,
        headers: { "Cache-Control": "no-store" }
      });
    }

    const provisioned = await provisionVerlunePremiumAccess(verification);
    if (!provisioned.entitlement) throw new VerluneAccessError(503, "entitlement_not_created");

    return NextResponse.json({
      ok: true,
      paymentId: verification.paymentId,
      status: verification.status,
      paymentMethodId: verification.paymentMethodId,
      entitled: true,
      entitlementId: provisioned.entitlement.entitlementId,
      accessEmail: provisioned.emailSent ? "sent" : "deferred"
    }, {
      headers: { "Cache-Control": "no-store" }
    });
  } catch (error) {
    if (error instanceof MercadoPagoApiError || error instanceof VerluneAccessError) {
      return NextResponse.json({ ok: false, error: error.code }, {
        status: error.status,
        headers: { "Cache-Control": "no-store" }
      });
    }
    return NextResponse.json({ ok: false, error: "test_reconcile_failed" }, {
      status: 502,
      headers: { "Cache-Control": "no-store" }
    });
  }
}
