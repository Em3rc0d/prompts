import "server-only";

import { createHmac, randomUUID, timingSafeEqual } from "node:crypto";

import {
  VERLUNE_PREMIUM_PRODUCT_TAG,
  type VerifiedVerlunePayment
} from "./verlune-mercado-pago";

export const VERLUNE_ACCESS_KEY_VERSION = "VLK1";
const ENTITLEMENT_VERSION = "1";
const ENTITLEMENT_ID_PATTERN = /^vpe1_[A-Za-z0-9_-]{20,32}$/;
const ACCESS_KEY_PATTERN = /^VLK1_[A-Za-z0-9_-]{20,32}_[A-Za-z0-9_-]{32}$/;

export type VerlunePremiumEntitlement = {
  v: 1;
  product: typeof VERLUNE_PREMIUM_PRODUCT_TAG;
  entitlementId: string;
  emailHash: string;
  provider: "mercado_pago";
  paymentId: string;
  status: "active" | "blocked";
  providerStatus: string;
  createdAt: string;
  updatedAt: string;
};

export type VerluneConfigState = {
  ready: boolean;
  missing: string[];
};

export class VerluneAccessError extends Error {
  constructor(public readonly status: number, public readonly code: string) {
    super(code);
    this.name = "VerluneAccessError";
  }
}

function secretV1(): string {
  const value = process.env.VERLUNE_ACCESS_KEY_SECRET_V1?.trim() ?? "";
  if (value.length < 32) throw new VerluneAccessError(503, "verlune_access_secret_not_configured");
  return value;
}

function hmac(label: string): string {
  return createHmac("sha256", secretV1()).update(label).digest("base64url");
}

function safeEqual(leftValue: string, rightValue: string): boolean {
  const left = Buffer.from(leftValue, "utf8");
  const right = Buffer.from(rightValue, "utf8");
  return left.length === right.length && timingSafeEqual(left, right);
}

export function normalizeVerluneEmail(value: unknown): string {
  return typeof value === "string" ? value.trim().toLowerCase() : "";
}

export function isValidVerluneEmail(value: string): boolean {
  return Boolean(value) && value.length <= 254 && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
}

export function deriveVerluneEntitlementId(emailInput: string): string {
  const email = normalizeVerluneEmail(emailInput);
  if (!isValidVerluneEmail(email)) throw new VerluneAccessError(400, "invalid_access_email");
  return `vpe1_${hmac(`entitlement:v1:${VERLUNE_PREMIUM_PRODUCT_TAG}:${email}`).slice(0, 24)}`;
}

function entitlementEmailHash(emailInput: string): string {
  const email = normalizeVerluneEmail(emailInput);
  return hmac(`email:v1:${VERLUNE_PREMIUM_PRODUCT_TAG}:${email}`);
}

export function createVerluneAccessKey(emailInput: string): string {
  const email = normalizeVerluneEmail(emailInput);
  const entitlementId = deriveVerluneEntitlementId(email);
  const signature = hmac(`access:v1:${VERLUNE_PREMIUM_PRODUCT_TAG}:${entitlementId}:${email}`).slice(0, 32);
  return `${VERLUNE_ACCESS_KEY_VERSION}_${entitlementId.slice(5)}_${signature}`;
}

export function verifyVerluneAccessKey(emailInput: string, observed: string): boolean {
  const email = normalizeVerluneEmail(emailInput);
  if (!isValidVerluneEmail(email) || !ACCESS_KEY_PATTERN.test(observed)) return false;
  try {
    return safeEqual(createVerluneAccessKey(email), observed);
  } catch {
    return false;
  }
}

export function getVerluneEntitlementConfigState(): VerluneConfigState {
  const missing: string[] = [];
  const secret = process.env.VERLUNE_ACCESS_KEY_SECRET_V1?.trim() ?? "";
  const kvUrl = process.env.VERLUNE_ENTITLEMENT_KV_REST_URL?.trim() ?? "";
  const kvToken = process.env.VERLUNE_ENTITLEMENT_KV_REST_TOKEN?.trim() ?? "";

  if (secret.length < 32) missing.push("VERLUNE_ACCESS_KEY_SECRET_V1");
  if (!kvUrl.startsWith("https://")) missing.push("VERLUNE_ENTITLEMENT_KV_REST_URL");
  if (kvToken.length < 16) missing.push("VERLUNE_ENTITLEMENT_KV_REST_TOKEN");
  return { ready: missing.length === 0, missing };
}

export function getVerluneAccessEmailConfigState(): VerluneConfigState {
  const missing: string[] = [];
  const resendKey = process.env.RESEND_API_KEY?.trim() ?? "";
  const from = process.env.VERLUNE_ACCESS_FROM_EMAIL?.trim() ?? "";
  const siteUrl = process.env.NEXT_PUBLIC_SITE_URL?.trim() ?? "";

  if (resendKey.length < 16) missing.push("RESEND_API_KEY");
  if (!from || !from.includes("@")) missing.push("VERLUNE_ACCESS_FROM_EMAIL");
  if (!siteUrl.startsWith("https://")) missing.push("NEXT_PUBLIC_SITE_URL");
  return { ready: missing.length === 0, missing };
}

export function getVerluneAccessConfigState(): VerluneConfigState {
  const entitlement = getVerluneEntitlementConfigState();
  const email = getVerluneAccessEmailConfigState();
  const missing = [...new Set([...entitlement.missing, ...email.missing])];
  return { ready: missing.length === 0, missing };
}

function requireKvConfig() {
  const state = getVerluneEntitlementConfigState();
  if (!state.ready) throw new VerluneAccessError(503, `verlune_entitlement_not_configured:${state.missing.join(",")}`);
  return {
    url: process.env.VERLUNE_ENTITLEMENT_KV_REST_URL!.trim().replace(/\/$/, ""),
    token: process.env.VERLUNE_ENTITLEMENT_KV_REST_TOKEN!.trim()
  };
}

async function kvCommand<T = unknown>(command: Array<string | number>): Promise<T> {
  const config = requireKvConfig();
  let response: Response;
  try {
    response = await fetch(config.url, {
      method: "POST",
      cache: "no-store",
      redirect: "error",
      signal: AbortSignal.timeout(8000),
      headers: {
        Authorization: `Bearer ${config.token}`,
        "Content-Type": "application/json"
      },
      body: JSON.stringify(command)
    });
  } catch {
    throw new VerluneAccessError(503, "verlune_entitlement_store_unavailable");
  }

  const payload = await response.json().catch(() => null) as { result?: unknown; error?: unknown } | null;
  if (!response.ok || !payload || typeof payload !== "object" || payload.error) {
    throw new VerluneAccessError(503, "verlune_entitlement_store_unavailable");
  }
  return payload.result as T;
}

function entitlementRedisKey(entitlementId: string): string {
  if (!ENTITLEMENT_ID_PATTERN.test(entitlementId)) throw new VerluneAccessError(400, "invalid_entitlement_id");
  return `verlune:premium:entitlement:v1:${entitlementId}`;
}

function hashPairs(input: unknown): Record<string, string> {
  if (Array.isArray(input)) {
    const result: Record<string, string> = {};
    for (let i = 0; i + 1 < input.length; i += 2) {
      result[String(input[i])] = String(input[i + 1]);
    }
    return result;
  }
  if (input && typeof input === "object") {
    return Object.fromEntries(Object.entries(input as Record<string, unknown>).map(([key, value]) => [key, String(value)]));
  }
  return {};
}

function parseEntitlement(input: unknown): VerlunePremiumEntitlement | null {
  const value = hashPairs(input);
  if (
    value.v !== ENTITLEMENT_VERSION ||
    value.product !== VERLUNE_PREMIUM_PRODUCT_TAG ||
    !ENTITLEMENT_ID_PATTERN.test(value.entitlementId ?? "") ||
    !value.emailHash ||
    value.provider !== "mercado_pago" ||
    !/^[1-9][0-9]{0,29}$/.test(value.paymentId ?? "") ||
    (value.status !== "active" && value.status !== "blocked") ||
    !value.createdAt ||
    !value.updatedAt
  ) return null;

  return {
    v: 1,
    product: VERLUNE_PREMIUM_PRODUCT_TAG,
    entitlementId: value.entitlementId,
    emailHash: value.emailHash,
    provider: "mercado_pago",
    paymentId: value.paymentId,
    status: value.status,
    providerStatus: value.providerStatus ?? "unknown",
    createdAt: value.createdAt,
    updatedAt: value.updatedAt
  };
}

const SYNC_ENTITLEMENT_SCRIPT = `
local exists = redis.call("EXISTS", KEYS[1])
local currentPayment = redis.call("HGET", KEYS[1], "paymentId")

if ARGV[1] == "activate" then
  if exists == 0 then
    redis.call("HSET", KEYS[1], "createdAt", ARGV[5])
  end
  redis.call("HSET", KEYS[1],
    "v", "1",
    "product", ARGV[6],
    "entitlementId", ARGV[7],
    "emailHash", ARGV[8],
    "provider", "mercado_pago",
    "paymentId", ARGV[2],
    "status", "active",
    "providerStatus", ARGV[3],
    "updatedAt", ARGV[4])
elseif exists == 1 and currentPayment == ARGV[2] then
  redis.call("HSET", KEYS[1],
    "status", "blocked",
    "providerStatus", ARGV[3],
    "updatedAt", ARGV[4])
end

return redis.call("HGETALL", KEYS[1])
`;

export async function getVerlunePremiumEntitlementById(entitlementId: string): Promise<VerlunePremiumEntitlement | null> {
  const result = await kvCommand<unknown>(["HGETALL", entitlementRedisKey(entitlementId)]);
  return parseEntitlement(result);
}

export async function getVerlunePremiumEntitlementByEmail(emailInput: string): Promise<VerlunePremiumEntitlement | null> {
  return getVerlunePremiumEntitlementById(deriveVerluneEntitlementId(emailInput));
}

export function entitlementMatchesEmail(entitlement: VerlunePremiumEntitlement, emailInput: string): boolean {
  const email = normalizeVerluneEmail(emailInput);
  if (!isValidVerluneEmail(email)) return false;
  try {
    return safeEqual(entitlement.emailHash, entitlementEmailHash(email));
  } catch {
    return false;
  }
}

export async function syncVerlunePremiumEntitlement(
  verification: VerifiedVerlunePayment
): Promise<VerlunePremiumEntitlement | null> {
  const email = normalizeVerluneEmail(verification.customerEmail);
  if (!isValidVerluneEmail(email)) {
    if (verification.entitled) throw new VerluneAccessError(502, "provider_email_invalid");
    return null;
  }

  const entitlementId = deriveVerluneEntitlementId(email);
  const now = new Date().toISOString();
  const providerStatus = verification.reason
    ? `${verification.status}:${verification.reason}`
    : verification.status;

  const result = await kvCommand<unknown>([
    "EVAL",
    SYNC_ENTITLEMENT_SCRIPT,
    1,
    entitlementRedisKey(entitlementId),
    verification.entitled ? "activate" : "block",
    verification.paymentId,
    providerStatus,
    now,
    now,
    VERLUNE_PREMIUM_PRODUCT_TAG,
    entitlementId,
    entitlementEmailHash(email)
  ]);

  return parseEntitlement(result);
}

export async function allowVerluneRecoveryEmail(entitlementId: string): Promise<boolean> {
  const result = await kvCommand<unknown>([
    "SET",
    `verlune:premium:recovery:v1:${entitlementId}`,
    "1",
    "NX",
    "EX",
    60
  ]);
  return result === "OK";
}

function requireEmailConfig() {
  const state = getVerluneAccessEmailConfigState();
  if (!state.ready) throw new VerluneAccessError(503, `verlune_access_email_not_configured:${state.missing.join(",")}`);
  return {
    apiKey: process.env.RESEND_API_KEY!.trim(),
    from: process.env.VERLUNE_ACCESS_FROM_EMAIL!.trim(),
    siteUrl: process.env.NEXT_PUBLIC_SITE_URL!.trim().replace(/\/$/, "")
  };
}

function escapeHtml(value: string): string {
  return value.replace(/[&<>"']/g, (character) => ({
    "&": "&amp;",
    "<": "&lt;",
    ">": "&gt;",
    '"': "&quot;",
    "'": "&#39;"
  }[character] ?? character));
}

export async function sendVerluneAccessEmail(input: {
  email: string;
  accessKey: string;
  entitlementId: string;
  reason: "purchase" | "recovery";
  idempotencyKey?: string;
}): Promise<void> {
  const config = requireEmailConfig();
  const email = normalizeVerluneEmail(input.email);
  if (!isValidVerluneEmail(email) || !ACCESS_KEY_PATTERN.test(input.accessKey)) {
    throw new VerluneAccessError(400, "invalid_access_delivery");
  }

  const unlockUrl = `${config.siteUrl}/unlock`;
  const subject = input.reason === "purchase"
    ? "Your Verlune Premium Access Key"
    : "Your Verlune Premium Access Key — recovery";
  const text = [
    "Verlune Premium",
    "",
    `Email: ${email}`,
    `Access Key: ${input.accessKey}`,
    "",
    "This is your one canonical Verlune Access Key. Keep it: the same key can be used whenever you need to unlock Premium.",
    `Unlock: ${unlockUrl}`
  ].join("\n");
  const html = `<div style="font-family:Arial,sans-serif;max-width:640px;margin:auto;color:#111827">
    <h1 style="font-size:24px">Verlune Premium</h1>
    <p>Your payment is linked to one reusable Access Key.</p>
    <p><strong>Email</strong><br>${escapeHtml(email)}</p>
    <p><strong>Access Key</strong><br><code style="font-size:15px">${escapeHtml(input.accessKey)}</code></p>
    <p>Keep this key. Verlune will return the same key for this email if you request recovery later.</p>
    <p><a href="${escapeHtml(unlockUrl)}">Unlock Verlune Premium</a></p>
  </div>`;

  const idempotencyKey = input.idempotencyKey
    ?? (input.reason === "purchase"
      ? `verlune-access-grant/${input.entitlementId}/v1`
      : `verlune-access-recovery/${input.entitlementId}/${randomUUID()}`);

  let response: Response;
  try {
    response = await fetch("https://api.resend.com/emails", {
      method: "POST",
      cache: "no-store",
      redirect: "error",
      signal: AbortSignal.timeout(8000),
      headers: {
        Authorization: `Bearer ${config.apiKey}`,
        "Content-Type": "application/json",
        "Idempotency-Key": idempotencyKey
      },
      body: JSON.stringify({
        from: config.from,
        to: [email],
        subject,
        text,
        html,
        tags: [
          { name: "product", value: "verlune-premium" },
          { name: "purpose", value: input.reason === "purchase" ? "access-grant" : "access-recovery" }
        ]
      })
    });
  } catch {
    throw new VerluneAccessError(503, "resend_unavailable");
  }

  if (!response.ok) throw new VerluneAccessError(503, "resend_unavailable");
}

export async function provisionVerlunePremiumAccess(
  verification: VerifiedVerlunePayment
): Promise<{
  entitlement: VerlunePremiumEntitlement | null;
  accessKey: string | null;
  emailSent: boolean;
}> {
  const entitlement = await syncVerlunePremiumEntitlement(verification);
  if (!verification.entitled || !entitlement || entitlement.status !== "active") {
    return { entitlement, accessKey: null, emailSent: false };
  }

  const accessKey = createVerluneAccessKey(verification.customerEmail);
  let emailSent = false;
  try {
    await sendVerluneAccessEmail({
      email: verification.customerEmail,
      accessKey,
      entitlementId: entitlement.entitlementId,
      reason: "purchase"
    });
    emailSent = true;
  } catch (error) {
    console.error("VERLUNE_ACCESS_EMAIL_DEFERRED", error instanceof VerluneAccessError ? error.code : "unknown");
  }

  return { entitlement, accessKey, emailSent };
}
