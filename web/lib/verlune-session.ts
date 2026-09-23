import { createHmac, timingSafeEqual } from "node:crypto";

export const VERLUNE_SESSION_COOKIE = "verlune_premium_session";

export type PremiumSession = {
  v: 1;
  licenseKeyId: string;
  instanceId: string;
  licenseFingerprint: string;
  emailHash: string;
  issuedAt: number;
  validatedAt: number;
  expiresAt: number;
};

function secret(name: "VERLUNE_SESSION_SECRET" | "VERLUNE_LICENSE_FINGERPRINT_SECRET"): string {
  const value = process.env[name]?.trim() ?? "";
  if (value.length < 32) throw new Error(`${name.toLowerCase()}_missing_or_too_short`);
  return value;
}

function hmac(value: string, key: string): string {
  return createHmac("sha256", key).update(value).digest("base64url");
}

function encode(payload: PremiumSession): string {
  return Buffer.from(JSON.stringify(payload), "utf8").toString("base64url");
}

function safeEqual(a: string, b: string): boolean {
  const left = Buffer.from(a, "utf8");
  const right = Buffer.from(b, "utf8");
  return left.length === right.length && timingSafeEqual(left, right);
}

export function fingerprintLicense(licenseKey: string): string {
  return hmac(licenseKey.trim(), secret("VERLUNE_LICENSE_FINGERPRINT_SECRET"));
}

export function hashCustomerEmail(email: string): string {
  return hmac(email.trim().toLowerCase(), secret("VERLUNE_LICENSE_FINGERPRINT_SECRET"));
}

export function signPremiumSession(payload: PremiumSession): string {
  const body = encode(payload);
  const signature = hmac(body, secret("VERLUNE_SESSION_SECRET"));
  return `${body}.${signature}`;
}

export function parsePremiumSession(token: string | undefined): PremiumSession | null {
  if (!token) return null;
  const [body, signature, extra] = token.split(".");
  if (!body || !signature || extra) return null;

  let expected: string;
  try {
    expected = hmac(body, secret("VERLUNE_SESSION_SECRET"));
  } catch {
    return null;
  }
  if (!safeEqual(signature, expected)) return null;

  try {
    const payload = JSON.parse(Buffer.from(body, "base64url").toString("utf8")) as PremiumSession;
    if (
      payload.v !== 1 ||
      !/^\d+$/.test(payload.licenseKeyId) ||
      !payload.instanceId ||
      !payload.licenseFingerprint ||
      !payload.emailHash ||
      !Number.isFinite(payload.issuedAt) ||
      !Number.isFinite(payload.validatedAt) ||
      !Number.isFinite(payload.expiresAt)
    ) return null;
    if (payload.expiresAt <= Math.floor(Date.now() / 1000)) return null;
    return payload;
  } catch {
    return null;
  }
}

export function sessionMaxAgeSeconds(): number {
  const parsed = Number(process.env.VERLUNE_SESSION_MAX_AGE_SECONDS ?? "604800");
  return Number.isFinite(parsed) && parsed >= 3600 && parsed <= 2592000 ? Math.floor(parsed) : 604800;
}

export function revalidateAfterSeconds(): number {
  const parsed = Number(process.env.VERLUNE_SESSION_REVALIDATE_SECONDS ?? "86400");
  return Number.isFinite(parsed) && parsed >= 900 && parsed <= 604800 ? Math.floor(parsed) : 86400;
}

export function newPremiumSession(input: {
  licenseKeyId: string;
  instanceId: string;
  licenseKey: string;
  customerEmail: string;
}): PremiumSession {
  const now = Math.floor(Date.now() / 1000);
  return {
    v: 1,
    licenseKeyId: input.licenseKeyId,
    instanceId: input.instanceId,
    licenseFingerprint: fingerprintLicense(input.licenseKey),
    emailHash: hashCustomerEmail(input.customerEmail),
    issuedAt: now,
    validatedAt: now,
    expiresAt: now + sessionMaxAgeSeconds()
  };
}

export function refreshedPremiumSession(session: PremiumSession): PremiumSession {
  return { ...session, validatedAt: Math.floor(Date.now() / 1000) };
}

export function sessionNeedsRevalidation(session: PremiumSession): boolean {
  return Math.floor(Date.now() / 1000) - session.validatedAt >= revalidateAfterSeconds();
}

export function premiumCookieOptions(session: PremiumSession) {
  const now = Math.floor(Date.now() / 1000);
  return {
    httpOnly: true,
    secure: process.env.NODE_ENV === "production",
    sameSite: "lax" as const,
    path: "/",
    maxAge: Math.max(0, session.expiresAt - now)
  };
}

export const clearPremiumCookieOptions = {
  httpOnly: true,
  secure: process.env.NODE_ENV === "production",
  sameSite: "lax" as const,
  path: "/",
  maxAge: 0
};
