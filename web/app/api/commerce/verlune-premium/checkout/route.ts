import { timingSafeEqual } from "node:crypto";

import { currentCommerceMode } from "@/lib/commerce-mode";
import { getVerluneAccessConfigState } from "@/lib/verlune-access";
import {
  premiumTestSessionMatches,
  VERLUNE_PREMIUM_TEST_SESSION_COOKIE,
} from "@/lib/verlune-premium-test-session";

const ATTRIBUTION_FIELDS = ["source", "medium", "campaign", "content"] as const;

type AttributionField = (typeof ATTRIBUTION_FIELDS)[number];

function clean(value: string | null): string | undefined {
  if (!value) return undefined;
  const normalized = value.trim().slice(0, 120);
  if (!normalized) return undefined;
  return normalized.replace(/[^a-zA-Z0-9._:/-]/g, "-");
}

function secretsMatch(expected: string | undefined, observed: string | null): boolean {
  if (!expected || !observed) return false;
  const expectedBytes = Buffer.from(expected, "utf8");
  const observedBytes = Buffer.from(observed, "utf8");
  return expectedBytes.length === observedBytes.length && timingSafeEqual(expectedBytes, observedBytes);
}

function authorizeGateToken(input: {
  expected: string | undefined;
  observed: string | null;
  sessionAuthorized?: boolean;
  notConfiguredError: string;
  unauthorizedError: string;
}): Response | null {
  if (!input.expected) return Response.json({ ok: false, error: input.notConfiguredError }, { status: 503 });
  if (!input.sessionAuthorized && !secretsMatch(input.expected, input.observed)) {
    return Response.json({ ok: false, error: input.unauthorizedError }, { status: 403 });
  }
  return null;
}

function cookieValue(request: Request, name: string): string | null {
  const cookie = request.headers.get("cookie");
  if (!cookie) return null;
  for (const pair of cookie.split(";")) {
    const [key, ...rest] = pair.trim().split("=");
    if (key === name) return decodeURIComponent(rest.join("="));
  }
  return null;
}

function isLemonSqueezyCheckout(destination: URL): boolean {
  return destination.hostname === "lemonsqueezy.com" || destination.hostname.endsWith(".lemonsqueezy.com");
}

export async function GET(request: Request) {
  const mode = currentCommerceMode("VERLUNE_PREMIUM_COMMERCE_MODE");
  const publicSaleLive = process.env.VERLUNE_PREMIUM_PUBLIC_SALE_STATUS === "LIVE";
  const access = getVerluneAccessConfigState();

  if (!access.ready) {
    return Response.json(
      { ok: false, error: "premium_access_not_configured", missing: access.missing },
      { status: 503 }
    );
  }

  if (mode === "off") {
    return Response.json(
      { ok: false, error: "commerce_disabled", sale_status: "NOT_FOR_SALE", commerce_mode: "off" },
      { status: 503 }
    );
  }

  let gate: "provider_test" | "live_canary" | "live";
  if (mode === "test") {
    if (publicSaleLive) {
      return Response.json(
        { ok: false, error: "commerce_configuration_conflict", detail: "public_sale_cannot_be_live_in_test_mode" },
        { status: 503 }
      );
    }
    gate = "provider_test";
    const denial = authorizeGateToken({
      expected: process.env.VERLUNE_PREMIUM_PROVIDER_TEST_TOKEN,
      observed: request.headers.get("x-verlune-provider-test-token"),
      sessionAuthorized: premiumTestSessionMatches(cookieValue(request, VERLUNE_PREMIUM_TEST_SESSION_COOKIE)),
      notConfiguredError: "provider_test_token_not_configured",
      unauthorizedError: "provider_test_not_authorized"
    });
    if (denial) return denial;
  } else if (!publicSaleLive) {
    gate = "live_canary";
    const denial = authorizeGateToken({
      expected: process.env.VERLUNE_PREMIUM_LIVE_CANARY_TOKEN,
      observed: request.headers.get("x-verlune-live-canary-token"),
      notConfiguredError: "live_canary_token_not_configured",
      unauthorizedError: "live_canary_not_authorized"
    });
    if (denial) return denial;
  } else {
    gate = "live";
  }

  const checkoutUrl = mode === "test"
    ? process.env.LEMONSQUEEZY_VERLUNE_PREMIUM_TEST_CHECKOUT_URL
    : process.env.LEMONSQUEEZY_VERLUNE_PREMIUM_LIVE_CHECKOUT_URL;

  if (!checkoutUrl) {
    return Response.json(
      {
        ok: false,
        error: "checkout_not_configured",
        sale_status: publicSaleLive ? "LIVE" : "NOT_FOR_SALE",
        commerce_mode: mode,
        commerce_gate: gate
      },
      { status: 503 }
    );
  }

  let destination: URL;
  try {
    destination = new URL(checkoutUrl);
  } catch {
    return Response.json({ ok: false, error: "checkout_url_invalid" }, { status: 500 });
  }

  if (destination.protocol !== "https:" || !isLemonSqueezyCheckout(destination)) {
    return Response.json({ ok: false, error: "checkout_url_not_allowed" }, { status: 500 });
  }

  destination.searchParams.set("checkout[custom][verlune_surface]", "premium");
  destination.searchParams.set("checkout[custom][commerce_gate]", gate);

  const incoming = new URL(request.url);
  const attribution: Partial<Record<AttributionField, string>> = {};
  for (const field of ATTRIBUTION_FIELDS) {
    const value = clean(incoming.searchParams.get(field));
    if (!value) continue;
    attribution[field] = value;
    destination.searchParams.set(`checkout[custom][${field}]`, value);
  }

  console.info("VERLUNE_FUNNEL_EVENT", JSON.stringify({
    event: gate === "provider_test"
      ? "premium_provider_test_checkout_started"
      : gate === "live_canary"
        ? "premium_live_canary_checkout_started"
        : "premium_checkout_started",
    commerce_gate: gate,
    timestamp: new Date().toISOString(),
    ...attribution
  }));

  if (request.headers.get("accept")?.includes("application/json")) {
    return Response.json({
      ok: true,
      checkoutUrl: destination.toString(),
      commerce_gate: gate,
      commerce_mode: mode,
    });
  }

  return Response.redirect(destination, 302);
}
