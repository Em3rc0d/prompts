import { NextResponse } from "next/server";

import { currentCommerceMode } from "@/lib/commerce-mode";
import {
  premiumTestSessionValue,
  providerTestTokenMatches,
  VERLUNE_PREMIUM_TEST_SESSION_COOKIE,
  VERLUNE_PREMIUM_TEST_SESSION_MAX_AGE_SECONDS,
} from "@/lib/verlune-premium-test-session";

function redirectTo(request: Request, suffix: string) {
  return NextResponse.redirect(new URL(`/premium/test${suffix}`, request.url), 303);
}

export async function POST(request: Request) {
  const mode = currentCommerceMode("VERLUNE_PREMIUM_COMMERCE_MODE");
  const publicSaleLive = process.env.VERLUNE_PREMIUM_PUBLIC_SALE_STATUS === "LIVE";
  const checkoutConfigured = Boolean(process.env.LEMONSQUEEZY_VERLUNE_PREMIUM_TEST_CHECKOUT_URL?.trim());
  const signature = premiumTestSessionValue();

  if (mode !== "test" || publicSaleLive || !checkoutConfigured || !signature) {
    return redirectTo(request, "?error=not-ready");
  }

  const form = await request.formData();
  const observed = typeof form.get("token") === "string" ? String(form.get("token")) : "";
  if (!providerTestTokenMatches(observed)) {
    return redirectTo(request, "?error=unauthorized");
  }

  const response = redirectTo(request, "?authorized=1");
  response.cookies.set(VERLUNE_PREMIUM_TEST_SESSION_COOKIE, signature, {
    httpOnly: true,
    secure: true,
    sameSite: "lax",
    path: "/",
    maxAge: VERLUNE_PREMIUM_TEST_SESSION_MAX_AGE_SECONDS,
  });
  return response;
}
