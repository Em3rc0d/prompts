import { createHmac, timingSafeEqual } from "node:crypto";

export type LemonSqueezyConfig = {
  webhookSecret: string;
  storeId: string;
  productId: string;
  variantId: string;
  allowTestMode: boolean;
};

type OrderCreatedPayload = {
  meta?: {
    event_name?: string;
  };
  data?: {
    type?: string;
    id?: string;
    attributes?: {
      store_id?: number;
      identifier?: string;
      order_number?: number;
      currency?: string;
      total?: number;
      total_usd?: number;
      status?: string;
      test_mode?: boolean;
      created_at?: string;
      first_order_item?: {
        product_id?: number;
        variant_id?: number;
        price?: number;
      };
    };
  };
};

export type CommerceEvidence = {
  event: "purchase_completed";
  source: "lemonsqueezy_webhook";
  evidence: "provider_signed_order_created";
  provider_order_id: string;
  provider_identifier?: string;
  order_number?: number;
  store_id: number;
  product_id: number;
  variant_id: number;
  currency?: string;
  total?: number;
  total_usd?: number;
  test_mode: boolean;
  created_at?: string;
};

export type WebhookEvaluation =
  | { kind: "accepted"; evidence: CommerceEvidence }
  | { kind: "ignored"; reason: string }
  | { kind: "invalid_signature" }
  | { kind: "malformed"; reason: string };

function signaturesMatch(rawBody: string, signature: string, secret: string): boolean {
  if (!signature || !secret) return false;
  const expectedHex = createHmac("sha256", secret).update(rawBody).digest("hex");
  const expected = Buffer.from(expectedHex, "utf8");
  const observed = Buffer.from(signature, "utf8");
  return expected.length === observed.length && timingSafeEqual(expected, observed);
}

export function evaluateLemonSqueezyWebhook(input: {
  rawBody: string;
  signature: string;
  eventName: string;
  config: LemonSqueezyConfig;
}): WebhookEvaluation {
  const { rawBody, signature, eventName, config } = input;

  if (!signaturesMatch(rawBody, signature, config.webhookSecret)) {
    return { kind: "invalid_signature" };
  }

  let payload: OrderCreatedPayload;
  try {
    payload = JSON.parse(rawBody) as OrderCreatedPayload;
  } catch {
    return { kind: "malformed", reason: "invalid_json" };
  }

  const payloadEvent = payload.meta?.event_name;
  if (eventName !== "order_created" || payloadEvent !== "order_created") {
    return { kind: "ignored", reason: "unsupported_event" };
  }

  if (payload.data?.type !== "orders" || !payload.data.id || !payload.data.attributes) {
    return { kind: "malformed", reason: "missing_order_shape" };
  }

  const attributes = payload.data.attributes;
  const item = attributes.first_order_item;
  if (!item?.product_id || !item.variant_id || !attributes.store_id) {
    return { kind: "malformed", reason: "missing_product_identity" };
  }

  if (attributes.status !== "paid") {
    return { kind: "ignored", reason: "order_not_paid" };
  }

  if (String(attributes.store_id) !== config.storeId) {
    return { kind: "ignored", reason: "store_mismatch" };
  }
  if (String(item.product_id) !== config.productId) {
    return { kind: "ignored", reason: "product_mismatch" };
  }
  if (String(item.variant_id) !== config.variantId) {
    return { kind: "ignored", reason: "variant_mismatch" };
  }

  const testMode = attributes.test_mode === true || item.test_mode === true;
  if (testMode && !config.allowTestMode) {
    return { kind: "ignored", reason: "test_mode_not_allowed" };
  }

  return {
    kind: "accepted",
    evidence: {
      event: "purchase_completed",
      source: "lemonsqueezy_webhook",
      evidence: "provider_signed_order_created",
      provider_order_id: payload.data.id,
      provider_identifier: attributes.identifier,
      order_number: attributes.order_number,
      store_id: attributes.store_id,
      product_id: item.product_id,
      variant_id: item.variant_id,
      currency: attributes.currency,
      total: attributes.total,
      total_usd: attributes.total_usd,
      test_mode: testMode,
      created_at: attributes.created_at,
    },
  };
}
