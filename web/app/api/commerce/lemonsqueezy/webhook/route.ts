import { currentCommerceMode } from "@/lib/commerce-mode";
import { evaluateLemonSqueezyWebhook, type LemonSqueezyConfig } from "@/lib/lemonsqueezy";

export const runtime = "nodejs";

function loadConfig(): LemonSqueezyConfig | null {
  const commerceMode = currentCommerceMode();
  if (commerceMode === "off") return null;

  const webhookSecret = process.env.LEMONSQUEEZY_WEBHOOK_SECRET;
  const storeId = process.env.LEMONSQUEEZY_STORE_ID;
  const productId = process.env.LEMONSQUEEZY_DEVELOPER_PACK_PRODUCT_ID;
  const variantId = process.env.LEMONSQUEEZY_DEVELOPER_PACK_VARIANT_ID;

  if (!webhookSecret || !storeId || !productId || !variantId) return null;

  return {
    webhookSecret,
    storeId,
    productId,
    variantId,
    commerceMode,
  };
}

export async function POST(request: Request) {
  const config = loadConfig();
  if (!config) {
    return Response.json(
      { ok: false, error: "commerce_not_configured" },
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
    return Response.json(
      { ok: false, error: evaluation.reason },
      { status: 400 },
    );
  }

  if (evaluation.kind === "ignored") {
    return Response.json({ ok: true, ignored: true, reason: evaluation.reason });
  }

  // Deliberately excludes customer name/email. Provider-signed order evidence only.
  console.info("PQ_COMMERCE_EVENT", JSON.stringify(evaluation.evidence));

  return Response.json({
    ok: true,
    accepted: true,
    event: evaluation.evidence.event,
    provider_order_id: evaluation.evidence.provider_order_id,
    test_mode: evaluation.evidence.test_mode,
    release: evaluation.evidence.release,
  });
}
