import { timingSafeEqual } from "node:crypto";

import { currentCommerceMode } from "@/lib/commerce-mode";
import { DEVELOPER_PACK_RELEASE, releaseCheckoutCustomData } from "@/lib/developer-pack-release";

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

export async function GET(request: Request) {
  const mode = currentCommerceMode();
  if (mode === "off") {
    return Response.json(
      { ok: false, error: "commerce_disabled", sale_status: "NOT_FOR_SALE", commerce_mode: "off" },
      { status: 503 },
    );
  }

  if (mode === "test") {
    const expectedToken = process.env.LEMONSQUEEZY_PROVIDER_TEST_TOKEN;
    if (!expectedToken) {
      return Response.json({ ok: false, error: "provider_test_token_not_configured" }, { status: 503 });
    }
    if (!secretsMatch(expectedToken, request.headers.get("x-pq-provider-test-token"))) {
      return Response.json({ ok: false, error: "provider_test_not_authorized" }, { status: 403 });
    }
  }

  const checkoutUrl = mode === "test"
    ? process.env.LEMONSQUEEZY_DEVELOPER_PACK_TEST_CHECKOUT_URL
    : process.env.LEMONSQUEEZY_DEVELOPER_PACK_LIVE_CHECKOUT_URL;

  if (!checkoutUrl) {
    return Response.json(
      { ok: false, error: "checkout_not_configured", sale_status: "NOT_FOR_SALE", commerce_mode: mode },
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

  const gate = mode === "test" ? "provider_test" : "live";
  for (const [key, value] of Object.entries(releaseCheckoutCustomData(gate))) {
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

  const event = mode === "test" ? "provider_test_checkout_started" : "checkout_started";
  console.info("PQ_FUNNEL_EVENT", JSON.stringify({
    event,
    product_id: DEVELOPER_PACK_RELEASE.productId,
    product_version: DEVELOPER_PACK_RELEASE.version,
    archive_sha256: DEVELOPER_PACK_RELEASE.archiveSha256,
    archive_size: DEVELOPER_PACK_RELEASE.archiveSize,
    timestamp: new Date().toISOString(),
    ...attribution,
  }));

  return Response.redirect(destination, 302);
}
