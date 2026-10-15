import { NextResponse } from "next/server";

import { currentCommerceMode } from "@/lib/commerce-mode";
import {
  diagnoseVerluneMercadoPagoTestCredentials,
  getVerluneMercadoPagoCoreConfigState,
  MercadoPagoApiError
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
