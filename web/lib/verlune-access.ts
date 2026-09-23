import { randomUUID } from "node:crypto";

export type VerluneAccessConfig = {
  apiKey: string;
  storeId: string;
  productId: string;
  variantId: string;
  activationLimit: number;
};

export type LicenseMeta = {
  store_id: number;
  order_id?: number;
  order_item_id?: number;
  product_id: number;
  product_name?: string;
  variant_id: number;
  variant_name?: string;
  customer_id?: number;
  customer_name?: string;
  customer_email: string;
};

export type LicenseKeyState = {
  id: number;
  status: "inactive" | "active" | "expired" | "disabled" | string;
  key?: string;
  activation_limit?: number | null;
  activation_usage?: number;
  expires_at?: string | null;
};

export type LicenseInstance = {
  id: string;
  name?: string;
  created_at?: string;
};

export type LicenseValidationResponse = {
  valid: boolean;
  error?: string | null;
  license_key?: LicenseKeyState;
  instance?: LicenseInstance | null;
  meta?: LicenseMeta;
};

export type LicenseActivationResponse = {
  activated: boolean;
  error?: string | null;
  license_key?: LicenseKeyState;
  instance?: LicenseInstance | null;
  meta?: LicenseMeta;
};

export type LicenseDeactivationResponse = {
  deactivated: boolean;
  error?: string | null;
  license_key?: LicenseKeyState;
  meta?: LicenseMeta;
};

type AdminLicenseKeyResponse = {
  data?: {
    id?: string;
    attributes?: {
      key?: string;
      store_id?: number;
      product_id?: number;
      user_email?: string;
      status?: string;
      disabled?: boolean | number;
      expires_at?: string | null;
    };
  };
};

const LICENSE_API = "https://api.lemonsqueezy.com/v1/licenses";
const ADMIN_API = "https://api.lemonsqueezy.com/v1";

export function normalizeEmail(value: string): string {
  return value.trim().toLowerCase();
}

export function getVerluneAccessConfig(): VerluneAccessConfig {
  const values = {
    apiKey: process.env.LEMONSQUEEZY_API_KEY?.trim() ?? "",
    storeId: process.env.VERLUNE_PREMIUM_STORE_ID?.trim() ?? "",
    productId: process.env.VERLUNE_PREMIUM_PRODUCT_ID?.trim() ?? "",
    variantId: process.env.VERLUNE_PREMIUM_VARIANT_ID?.trim() ?? "",
    activationLimit: Number(process.env.VERLUNE_PREMIUM_ACTIVATION_LIMIT ?? "3")
  };
  const missing = [
    ["apiKey", values.apiKey],
    ["storeId", values.storeId],
    ["productId", values.productId],
    ["variantId", values.variantId]
  ].filter(([, value]) => !value).map(([key]) => key);
  if (missing.length) throw new Error(`verlune_access_not_configured:${missing.join(",")}`);
  if (!Number.isInteger(values.activationLimit) || values.activationLimit < 1 || values.activationLimit > 20) {
    throw new Error("verlune_access_invalid_activation_limit");
  }
  return values;
}

export function getVerluneAccessConfigState(): { ready: boolean; missing: string[] } {
  const required: Array<[string, string | undefined]> = [
    ["LEMONSQUEEZY_API_KEY", process.env.LEMONSQUEEZY_API_KEY],
    ["VERLUNE_PREMIUM_STORE_ID", process.env.VERLUNE_PREMIUM_STORE_ID],
    ["VERLUNE_PREMIUM_PRODUCT_ID", process.env.VERLUNE_PREMIUM_PRODUCT_ID],
    ["VERLUNE_PREMIUM_VARIANT_ID", process.env.VERLUNE_PREMIUM_VARIANT_ID]
  ];
  const missing = required.filter(([, value]) => !value?.trim()).map(([name]) => name);
  if ((process.env.VERLUNE_SESSION_SECRET?.trim().length ?? 0) < 32) missing.push("VERLUNE_SESSION_SECRET");
  if ((process.env.VERLUNE_LICENSE_FINGERPRINT_SECRET?.trim().length ?? 0) < 32) missing.push("VERLUNE_LICENSE_FINGERPRINT_SECRET");
  const activationLimit = Number(process.env.VERLUNE_PREMIUM_ACTIVATION_LIMIT ?? "3");
  if (!Number.isInteger(activationLimit) || activationLimit < 1 || activationLimit > 20) {
    missing.push("VERLUNE_PREMIUM_ACTIVATION_LIMIT");
  }
  return { ready: missing.length === 0, missing };
}

function formBody(values: Record<string, string>): URLSearchParams {
  const body = new URLSearchParams();
  for (const [key, value] of Object.entries(values)) body.set(key, value);
  return body;
}

export class LemonLicenseApiError extends Error {
  constructor(
    public readonly operation: "activate" | "validate" | "deactivate",
    public readonly status: number,
    public readonly providerReason: string
  ) {
    super(`lemonsqueezy_license_${operation}_failed:${providerReason}`);
    this.name = "LemonLicenseApiError";
  }
}

async function licensePost<T>(path: "activate" | "validate" | "deactivate", values: Record<string, string>): Promise<T> {
  const response = await fetch(`${LICENSE_API}/${path}`, {
    method: "POST",
    headers: {
      Accept: "application/json",
      "Content-Type": "application/x-www-form-urlencoded"
    },
    body: formBody(values),
    cache: "no-store"
  });

  const payload = await response.json().catch(() => ({ error: "invalid_provider_response" }));
  if (!response.ok) {
    const reason = typeof payload?.error === "string" ? payload.error : `provider_http_${response.status}`;
    throw new LemonLicenseApiError(path, response.status, reason);
  }
  return payload as T;
}

export async function validateLicenseKey(licenseKey: string, instanceId?: string): Promise<LicenseValidationResponse> {
  const values: Record<string, string> = { license_key: licenseKey };
  if (instanceId) values.instance_id = instanceId;
  return licensePost<LicenseValidationResponse>("validate", values);
}

export async function activateLicenseKey(licenseKey: string): Promise<LicenseActivationResponse> {
  const suffix = randomUUID().slice(0, 8);
  return licensePost<LicenseActivationResponse>("activate", {
    license_key: licenseKey,
    instance_name: `Verlune Web ${suffix}`
  });
}

export async function deactivateLicenseKey(licenseKey: string, instanceId: string): Promise<LicenseDeactivationResponse> {
  return licensePost<LicenseDeactivationResponse>("deactivate", {
    license_key: licenseKey,
    instance_id: instanceId
  });
}

export function entitlementMatches(
  response: { valid?: boolean; activated?: boolean; meta?: LicenseMeta; license_key?: LicenseKeyState },
  email: string,
  config = getVerluneAccessConfig()
): { ok: boolean; reason?: string } {
  const meta = response.meta;
  const key = response.license_key;
  if (!meta || !key) return { ok: false, reason: "missing_license_metadata" };
  if ("valid" in response && response.valid !== true) return { ok: false, reason: "license_not_valid" };
  if ("activated" in response && response.activated !== true) return { ok: false, reason: "license_not_activated" };
  if (String(meta.store_id) !== config.storeId) return { ok: false, reason: "store_mismatch" };
  if (String(meta.product_id) !== config.productId) return { ok: false, reason: "product_mismatch" };
  if (String(meta.variant_id) !== config.variantId) return { ok: false, reason: "variant_mismatch" };
  if (normalizeEmail(meta.customer_email) !== normalizeEmail(email)) return { ok: false, reason: "email_mismatch" };
  if (key.status === "expired" || key.status === "disabled") return { ok: false, reason: `license_${key.status}` };
  if (key.activation_limit !== config.activationLimit) return { ok: false, reason: "activation_limit_mismatch" };
  return { ok: true };
}

export async function retrieveRawLicenseKey(licenseKeyId: string, config = getVerluneAccessConfig()): Promise<string> {
  if (!/^\d+$/.test(licenseKeyId)) throw new Error("invalid_license_key_id");
  const response = await fetch(`${ADMIN_API}/license-keys/${licenseKeyId}`, {
    method: "GET",
    headers: {
      Accept: "application/vnd.api+json",
      "Content-Type": "application/vnd.api+json",
      Authorization: `Bearer ${config.apiKey}`
    },
    cache: "no-store"
  });
  const payload = (await response.json().catch(() => ({}))) as AdminLicenseKeyResponse;
  if (!response.ok) throw new Error(`lemonsqueezy_license_retrieve_failed:${response.status}`);
  const raw = payload.data?.attributes?.key;
  if (!raw) throw new Error("lemonsqueezy_license_retrieve_missing_key");
  return raw;
}
