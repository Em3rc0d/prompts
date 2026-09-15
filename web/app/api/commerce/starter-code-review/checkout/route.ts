import { timingSafeEqual } from "node:crypto";

import { currentStarterCodeReviewCommerceMode } from "@/lib/commerce-mode";
import {
  STARTER_CODE_REVIEW_RELEASE,
  starterCodeReviewCheckoutCustomData,
  type CommerceGate,
} from "@/lib/starter-code-review-release";

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
  notConfiguredError: string;
  unauthorizedError: string;
}): Response | null {
  if (!input.expected) {
    return Response.json({ ok: false, error: input.notConfiguredError }, { status: 503 });
  }
  if (!secretsMatch(input.expected, input.observed)) {
    return Response.json({ ok: false, error: input.unauthorizedError }, { status: 403 });
  }
  return null;
}

export async function GET(request: Request) {
  const mode = currentStarterCodeReviewCommerceMode();
  const publicSaleLive = process.env.NEXT_PUBLIC_STARTER_CODE_REVIEW_SALE_STATUS === "LIVE";

  if (mode === "off") {
    return Response.json(
      { ok: false, error: "commerce_disabled", sale_status: "NOT_FOR_SALE", commerce_mode: "off" },
      { status: 503 },
    );
  }

  if (mode === "test" && publicSaleLive) {
    return Response.json(
      { ok: false, error: "commerce_configuration_conflict", detail: "public_sale_cannot_be_live_in_test_mode" },
      { status: 503 },
    );
  }

  let gate: CommerceGate;
  if (mode === "test") {
    gate = "provider_test";
    const denial = authorizeGateToken({
      expected: process.env.LEMONSQUEEZY_STARTER_CODE_REVIEW_PROVIDER_TEST_TOKEN,
      observed: request.headers.get("x-pm-starter-code-review-provider-test-token"),
      notConfiguredError: "provider_test_token_not_configured",
      unauthorizedError: "provider_test_not_authorized",
    });
    if (denial) return denial;
  } else if (!publicSaleLive) {
    gate = "live_canary";
    const denial = authorizeGateToken({
      expected: process.env.LEMONSQUEEZY_STARTER_CODE_REVIEW_LIVE_CANARY_TOKEN,
      observed: request.headers.get("x-pm-starter-code-review-live-canary-token"),
      notConfiguredError: "live_canary_token_not_configured",
      unauthorizedError: "live_canary_not_authorized",
    });
    if (denial) return denial;
  } else {
    gate = "live";
  }

  const checkoutUrl = mode === "test"
    ? process.env.LEMONSQUEEZY_STARTER_CODE_REVIEW_TEST_CHECKOUT_URL
    : process.env.LEMONSQUEEZY_STARTER_CODE_REVIEW_LIVE_CHECKOUT_URL;

  if (!checkoutUrl) {
    return Response.json(
      { ok: false, error: "checkout_not_configured", sale_status: publicSaleLive ? "LIVE" : "NOT_FOR_SALE", commerce_mode: mode, commerce_gate: gate },
      { status: 503 },
    );
  }

  let destination: URL;
  try {
    destination = new URL(checkoutUrl);
  } catch {
    return Response.json({ ok: false, error: "checkout_url_invalid" }, { status: 500 });
  }

  if (destination.protocol !== "https:") {
    return Response.json({ ok: false, error: "checkout_url_must_use_https" }, { status: 500 });
  }

  for (const [key, value] of Object.entries(starterCodeReviewCheckoutCustomData(gate))) {
    destination.searchParams.set(`checkout[custom][${key}]`, value);
  }

  const incoming = new URL(request.url);
  const attribution: Partial<Record<AttributionField, string>> = {};
  for (const field of ATTRIBUTION_FIELDS) {
    const value = clean(incoming.searchParams.get(field));
    if (!value) continue;
    attribution[field] = value;
    destination.searchParams.set(`checkout[custom][${field}]`, value);
  }

  const event = gate === "provider_test"
    ? "provider_test_checkout_started"
    : gate === "live_canary"
      ? "live_delivery_canary_checkout_started"
      : "checkout_started";

  console.info("PM_FUNNEL_EVENT", JSON.stringify({
    event,
    commerce_gate: gate,
    product_id: STARTER_CODE_REVIEW_RELEASE.productId,
    product_version: STARTER_CODE_REVIEW_RELEASE.version,
    archive_sha256: STARTER_CODE_REVIEW_RELEASE.archiveSha256,
    archive_size: STARTER_CODE_REVIEW_RELEASE.archiveSize,
    timestamp: new Date().toISOString(),
    ...attribution,
  }));

  return Response.redirect(destination, 302);
}
