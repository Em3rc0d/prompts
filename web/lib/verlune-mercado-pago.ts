import { createHmac, timingSafeEqual } from "node:crypto";

const UUID_V4 = /^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;
const VERLUNE_REFERENCE = /^verlune-premium:[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$/i;

export const VERLUNE_PREMIUM_PRICE_USD = 5;
export const VERLUNE_PREMIUM_PRODUCT_TAG = "verlune-premium-v1";
export const VERLUNE_PREMIUM_DESCRIPTION = "Verlune Premium";
export const DEFAULT_VERLUNE_PREMIUM_PRICE_PEN_MINOR = 1700;

export type MercadoPagoEnvironment = "test" | "live";

export type MercadoPagoConfigState = {
  ready: boolean;
  missing: string[];
  environment: MercadoPagoEnvironment | null;
  liveAllowed: boolean;
  publicKey: string;
  collectorId: string;
  pricePenMinor: number;
};

export type MercadoPagoPayment = {
  id?: string | number;
  live_mode?: boolean;
  status?: string;
  status_detail?: string;
  currency_id?: string;
  transaction_amount?: string | number;
  transaction_amount_refunded?: string | number;
  collector_id?: string | number;
  payment_method_id?: string;
  external_reference?: string | null;
  description?: string | null;
  date_last_updated?: string;
  payer?: { email?: string | null };
  metadata?: Record<string, unknown> | null;
};

export class MercadoPagoApiError extends Error {
  constructor(public readonly status: number, public readonly code: string) {
    super(code);
    this.name = "MercadoPagoApiError";
  }
}

export type VerifiedVerlunePayment = {
  paymentId: string;
  status: string;
  paymentMethodId: string;
  customerEmail: string;
  entitled: boolean;
  reason?: string;
};

function providerId(value: unknown): string | null {
  if (typeof value === "number" && Number.isSafeInteger(value) && value > 0) return String(value);
  if (typeof value === "string" && /^[1-9][0-9]{0,29}$/.test(value)) return value;
  return null;
}

function normalizeEmail(value: unknown): string {
  return typeof value === "string" ? value.trim().toLowerCase() : "";
}

function amountToMinor(value: unknown): number | null {
  if (typeof value !== "number" && typeof value !== "string") return null;
  const match = /^(0|[1-9]\d*)(?:\.(\d+))?$/.exec(String(value));
  if (!match) return null;
  const fraction = match[2] ?? "";
  if (/[1-9]/.test(fraction.slice(2))) return null;
  const minor = Number(match[1]) * 100 + Number(fraction.slice(0, 2).padEnd(2, "0"));
  return Number.isSafeInteger(minor) ? minor : null;
}

function configuredPriceMinor(): number {
  const parsed = Number(process.env.VERLUNE_PREMIUM_PRICE_PEN_MINOR ?? String(DEFAULT_VERLUNE_PREMIUM_PRICE_PEN_MINOR));
  return Number.isSafeInteger(parsed) && parsed >= 100 && parsed <= 1000000
    ? parsed
    : DEFAULT_VERLUNE_PREMIUM_PRICE_PEN_MINOR;
}

function environment(): MercadoPagoEnvironment | null {
  const value = process.env.MP_ENVIRONMENT?.trim();
  return value === "test" || value === "live" ? value : null;
}

export function getVerluneMercadoPagoConfigState(): MercadoPagoConfigState {
  const publicKey = process.env.MP_PUBLIC_KEY?.trim() ?? "";
  const collectorId = process.env.MP_COLLECTOR_ID?.trim() ?? "";
  const env = environment();
  const liveAllowed = process.env.MP_ALLOW_LIVE === "true";
  const missing: string[] = [];

  if (!process.env.MP_ACCESS_TOKEN?.trim()) missing.push("MP_ACCESS_TOKEN");
  if (!publicKey) missing.push("MP_PUBLIC_KEY");
  if (!/^[1-9][0-9]{0,29}$/.test(collectorId)) missing.push("MP_COLLECTOR_ID");
  if (!env) missing.push("MP_ENVIRONMENT");
  if (env === "live" && !liveAllowed) missing.push("MP_ALLOW_LIVE");
  if ((process.env.VERLUNE_SESSION_SECRET?.trim().length ?? 0) < 32) missing.push("VERLUNE_SESSION_SECRET");
  if ((process.env.VERLUNE_LICENSE_FINGERPRINT_SECRET?.trim().length ?? 0) < 32) {
    missing.push("VERLUNE_LICENSE_FINGERPRINT_SECRET");
  }

  return {
    ready: missing.length === 0,
    missing,
    environment: env,
    liveAllowed,
    publicKey,
    collectorId,
    pricePenMinor: configuredPriceMinor()
  };
}

function requireProviderConfig() {
  const state = getVerluneMercadoPagoConfigState();
  if (!state.ready || !state.environment) {
    throw new MercadoPagoApiError(503, `mercado_pago_not_configured:${state.missing.join(",")}`);
  }
  return {
    accessToken: process.env.MP_ACCESS_TOKEN!.trim(),
    collectorId: state.collectorId,
    environment: state.environment,
    liveMode: state.environment === "live",
    pricePenMinor: state.pricePenMinor
  };
}

async function mpFetch(path: string, init: RequestInit = {}): Promise<MercadoPagoPayment> {
  const config = requireProviderConfig();
  let response: Response;
  try {
    response = await fetch(`https://api.mercadopago.com${path}`, {
      ...init,
      cache: "no-store",
      redirect: "error",
      signal: AbortSignal.timeout(10000),
      headers: {
        Accept: "application/json",
        Authorization: `Bearer ${config.accessToken}`,
        "Content-Type": "application/json",
        ...(init.headers ?? {})
      }
    });
  } catch {
    throw new MercadoPagoApiError(503, "mercado_pago_unavailable");
  }

  if (!response.ok) {
    throw new MercadoPagoApiError(response.status, response.status === 404
      ? "mercado_pago_payment_not_found"
      : "mercado_pago_unavailable");
  }

  const payload = await response.json().catch(() => null);
  if (!payload || typeof payload !== "object") throw new MercadoPagoApiError(502, "mercado_pago_invalid_response");
  return payload as MercadoPagoPayment;
}

function cleanInstrument(input: unknown) {
  const value = input && typeof input === "object" ? input as Record<string, unknown> : {};
  const token = typeof value.token === "string" ? value.token.trim() : "";
  const paymentMethodId = typeof value.payment_method_id === "string"
    ? value.payment_method_id.trim().toLowerCase()
    : "";
  const installments = Number(value.installments ?? 1);
  const issuerRaw = value.issuer_id;
  const issuerId = typeof issuerRaw === "string" || typeof issuerRaw === "number"
    ? String(issuerRaw).trim()
    : "";
  const payerRaw = value.payer && typeof value.payer === "object"
    ? value.payer as Record<string, unknown>
    : {};
  const email = normalizeEmail(payerRaw.email);
  const identificationRaw = payerRaw.identification && typeof payerRaw.identification === "object"
    ? payerRaw.identification as Record<string, unknown>
    : null;
  const identificationType = identificationRaw && typeof identificationRaw.type === "string"
    ? identificationRaw.type.trim()
    : "";
  const identificationNumber = identificationRaw && typeof identificationRaw.number === "string"
    ? identificationRaw.number.trim()
    : "";

  if (token.length < 8 || token.length > 512 || /\s/.test(token)) throw new MercadoPagoApiError(400, "invalid_payment_token");
  if (!/^[a-z0-9_-]{2,80}$/.test(paymentMethodId)) throw new MercadoPagoApiError(400, "invalid_payment_method");
  if (installments !== 1) throw new MercadoPagoApiError(400, "installments_must_be_one");
  if (!email || email.length > 254 || !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
    throw new MercadoPagoApiError(400, "invalid_payer_email");
  }
  if (paymentMethodId === "yape" && issuerId) throw new MercadoPagoApiError(400, "yape_issuer_not_supported");

  const payer: Record<string, unknown> = { email };
  if (identificationType && identificationNumber) {
    if (identificationType.length > 20 || identificationNumber.length > 40) {
      throw new MercadoPagoApiError(400, "invalid_payer_identification");
    }
    payer.identification = { type: identificationType, number: identificationNumber };
  }

  return {
    token,
    paymentMethodId,
    installments,
    issuerId: issuerId || undefined,
    payer,
    email
  };
}

export async function createVerlunePremiumPayment(input: {
  formData: unknown;
  idempotencyKey: string;
  notificationUrl?: string;
}): Promise<VerifiedVerlunePayment> {
  const config = requireProviderConfig();
  if (!UUID_V4.test(input.idempotencyKey)) {
    throw new MercadoPagoApiError(400, "invalid_idempotency_key");
  }

  const instrument = cleanInstrument(input.formData);
  const externalReference = `verlune-premium:${input.idempotencyKey.toLowerCase()}`;
  const body: Record<string, unknown> = {
    transaction_amount: config.pricePenMinor / 100,
    token: instrument.token,
    payment_method_id: instrument.paymentMethodId,
    installments: instrument.installments,
    ...(instrument.issuerId ? { issuer_id: instrument.issuerId } : {}),
    payer: instrument.payer,
    description: VERLUNE_PREMIUM_DESCRIPTION,
    external_reference: externalReference,
    metadata: {
      verlune_product: VERLUNE_PREMIUM_PRODUCT_TAG,
      canonical_price_usd: VERLUNE_PREMIUM_PRICE_USD
    }
  };
  if (input.notificationUrl?.startsWith("https://")) body.notification_url = input.notificationUrl;

  const created = await mpFetch("/v1/payments", {
    method: "POST",
    headers: { "X-Idempotency-Key": input.idempotencyKey.toLowerCase() },
    body: JSON.stringify(body)
  });
  const id = providerId(created.id);
  if (!id) throw new MercadoPagoApiError(502, "mercado_pago_invalid_payment_id");

  const canonical = await readMercadoPagoPayment(id);
  return verifyVerlunePremiumPayment(canonical, instrument.email);
}

export async function readMercadoPagoPayment(paymentId: string): Promise<MercadoPagoPayment> {
  if (!/^[1-9][0-9]{0,29}$/.test(paymentId)) throw new MercadoPagoApiError(400, "invalid_payment_id");
  return mpFetch(`/v1/payments/${paymentId}`);
}

export function verifyVerlunePremiumPayment(
  payment: MercadoPagoPayment,
  expectedEmail?: string
): VerifiedVerlunePayment {
  const config = requireProviderConfig();
  const id = providerId(payment.id);
  const email = normalizeEmail(payment.payer?.email);
  const status = typeof payment.status === "string" ? payment.status : "";
  const method = typeof payment.payment_method_id === "string" ? payment.payment_method_id : "";
  const metadataTag = typeof payment.metadata?.verlune_product === "string"
    ? payment.metadata.verlune_product
    : "";
  const metadataPriceUsd = Number(payment.metadata?.canonical_price_usd);
  const refundedMinor = amountToMinor(payment.transaction_amount_refunded ?? 0);

  const checks: Array<[boolean, string]> = [
    [Boolean(id), "provider_id_mismatch"],
    [typeof payment.external_reference === "string" && VERLUNE_REFERENCE.test(payment.external_reference), "reference_mismatch"],
    [payment.description === VERLUNE_PREMIUM_DESCRIPTION, "description_mismatch"],
    [metadataTag === VERLUNE_PREMIUM_PRODUCT_TAG, "product_mismatch"],
    [metadataPriceUsd === VERLUNE_PREMIUM_PRICE_USD, "metadata_price_mismatch"],
    [amountToMinor(payment.transaction_amount) === config.pricePenMinor, "amount_mismatch"],
    [payment.currency_id === "PEN", "currency_mismatch"],
    [providerId(payment.collector_id) === config.collectorId, "collector_mismatch"],
    [payment.live_mode === config.liveMode, "environment_mismatch"],
    [Boolean(method), "payment_method_missing"],
    [Boolean(email), "payer_email_missing"],
    [!expectedEmail || email === normalizeEmail(expectedEmail), "payer_email_mismatch"],
    [refundedMinor === 0, "payment_refunded"]
  ];
  const failed = checks.find(([ok]) => !ok);

  return {
    paymentId: id ?? "",
    status: status || "unknown",
    paymentMethodId: method || "unknown",
    customerEmail: email,
    entitled: !failed && status === "approved",
    reason: failed?.[1] ?? (status === "approved" ? undefined : `payment_${status || "unknown"}`)
  };
}

export function verifyMercadoPagoWebhook(input: {
  url: string;
  headers: Headers;
  secret: string;
  now?: number;
  toleranceMs?: number;
}): { dataId: string; requestId: string } {
  const now = input.now ?? Date.now();
  const toleranceMs = input.toleranceMs ?? 300000;
  if (input.secret.length < 16) throw new MercadoPagoApiError(503, "mercado_pago_webhook_not_configured");

  try {
    const url = new URL(input.url);
    const ids = url.searchParams.getAll("data.id");
    if (ids.length !== 1 || !/^[a-zA-Z0-9]{1,128}$/.test(ids[0])) throw new Error("id");
    const requestId = input.headers.get("x-request-id") ?? "";
    const signature = input.headers.get("x-signature") ?? "";
    if (!/^[a-zA-Z0-9_-]{1,200}$/.test(requestId) || signature.length >= 512) throw new Error("headers");
    const entries = signature.split(",").map((part) => part.trim().split("="));
    if (entries.length !== 2 || entries.some((entry) => entry.length !== 2)) throw new Error("signature");
    const parts = Object.fromEntries(entries) as Record<string, string>;
    if (!/^\d{10}$|^\d{13}$/.test(parts.ts ?? "") || !/^[a-fA-F0-9]{64}$/.test(parts.v1 ?? "")) throw new Error("parts");
    const timestamp = Number(parts.ts) * (parts.ts.length === 10 ? 1000 : 1);
    if (Math.abs(now - timestamp) > toleranceMs) throw new Error("stale");
    const dataId = ids[0].toLowerCase();
    const manifest = `id:${dataId};request-id:${requestId};ts:${parts.ts};`;
    const expected = createHmac("sha256", input.secret).update(manifest).digest();
    const observed = Buffer.from(parts.v1, "hex");
    if (expected.length !== observed.length || !timingSafeEqual(expected, observed)) throw new Error("hmac");
    return { dataId, requestId };
  } catch {
    throw new MercadoPagoApiError(401, "invalid_signature");
  }
}
