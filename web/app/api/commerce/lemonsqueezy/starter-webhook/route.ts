import { currentStarterCommerceMode } from "@/lib/commerce-mode";
import { STARTER_COLLECTION_RELEASE, type CommerceGate } from "@/lib/starter-collection-release";
import { evaluateLemonSqueezyWebhook, type LemonSqueezyConfig } from "@/lib/lemonsqueezy";

export const runtime = "nodejs";

function loadConfig(): LemonSqueezyConfig | null {
  const commerceMode = currentStarterCommerceMode();
  if (commerceMode === "off") return null;

  const publicSaleLive = process.env.NEXT_PUBLIC_STARTER_COLLECTION_SALE_STATUS === "LIVE";
  if (commerceMode === "test" && publicSaleLive) return null;

  const webhookSecret = process.env.LEMONSQUEEZY_WEBHOOK_SECRET;
  const storeId = process.env.LEMONSQUEEZY_STORE_ID;
  const productId = process.env.LEMONSQUEEZY_STARTER_PRODUCT_ID;
  const variantId = process.env.LEMONSQUEEZY_STARTER_VARIANT_ID;

  if (!webhookSecret || !storeId || !productId || !variantId) return null;

  const commerceGate: CommerceGate = commerceMode === "test"
    ? "provider_test"
    : publicSaleLive
      ? "live"
      : "live_canary";

  return {
    webhookSecret,
    storeId,
    productId,
    variantId,
    commerceMode,
    commerceGate,
    release: STARTER_COLLECTION_RELEASE,
  };
}

export async function POST(request: Request) {
  const config = loadConfig();
  if (!config) {
    return Response.json(
      { ok: false, error: "starter_commerce_not_configured" },
      { status: 503 },
    );
  }

  const rawBody = await request.text();
  const signature = request.headers.get("x-signature") ?? "";
  const eventName = request.headers.get("x-event-name") ?? "";

  const evaluation = evaluateLemonSqueezyWebhook({
    rawBody,
    signature,
    eventName,
    config,
  });

  if (evaluation.kind === "invalid_signature") {
    return Response.json({ ok: false, error: "invalid_signature" }, { status: 401 });
  }

  if (evaluation.kind === "malformed") {
    return Response.json({ ok: false, error: evaluation.reason }, { status: 400 });
  }

  if (evaluation.kind === "ignored") {
    return Response.json({ ok: true, ignored: true, reason: evaluation.reason });
  }

  // Intentionally excludes customer name/email and payment details.
  // This is provider-signed order evidence only; it does not prove custody or delivery.
  console.info("PM_STARTER_COMMERCE_EVENT", JSON.stringify(evaluation.evidence));

  return Response.json({
    ok: true,
    accepted: true,
    event: evaluation.evidence.event,
    commerce_gate: evaluation.evidence.commerce_gate,
    provider_order_id: evaluation.evidence.provider_order_id,
    test_mode: evaluation.evidence.test_mode,
    release: evaluation.evidence.release,
  });
}
