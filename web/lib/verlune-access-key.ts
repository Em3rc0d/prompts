import { createHmac, timingSafeEqual } from "node:crypto";

export const VERLUNE_ACCESS_KEY_VERSION = "VLK1";
export const VERLUNE_ENTITLEMENT_ID_PATTERN = /^vpe1_[A-Za-z0-9_-]{20,32}$/;
export const VERLUNE_ACCESS_KEY_PATTERN = /^VLK1_[A-Za-z0-9_-]{20,32}_[A-Za-z0-9_-]{32}$/;

function requireSecret(secret: string): string {
  const value = secret.trim();
  if (value.length < 32) throw new Error("access_key_secret_too_short");
  return value;
}

export function normalizeVerluneEmail(value: unknown): string {
  return typeof value === "string" ? value.trim().toLowerCase() : "";
}

export function isValidVerluneEmail(value: string): boolean {
  return Boolean(value) && value.length <= 254 && /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value);
}

export function signVerluneAccessValue(value: string, secret: string): string {
  return createHmac("sha256", requireSecret(secret)).update(value).digest("base64url");
}

function safeEqual(leftValue: string, rightValue: string): boolean {
  const left = Buffer.from(leftValue, "utf8");
  const right = Buffer.from(rightValue, "utf8");
  return left.length === right.length && timingSafeEqual(left, right);
}

export function deriveVerluneEntitlementIdWithSecret(
  emailInput: string,
  secret: string,
  productTag: string
): string {
  const email = normalizeVerluneEmail(emailInput);
  if (!isValidVerluneEmail(email)) throw new Error("invalid_access_email");
  return `vpe1_${signVerluneAccessValue(`entitlement:v1:${productTag}:${email}`, secret).slice(0, 24)}`;
}

export function createVerluneAccessKeyWithSecret(
  emailInput: string,
  secret: string,
  productTag: string
): string {
  const email = normalizeVerluneEmail(emailInput);
  const entitlementId = deriveVerluneEntitlementIdWithSecret(email, secret, productTag);
  const signature = signVerluneAccessValue(
    `access:v1:${productTag}:${entitlementId}:${email}`,
    secret
  ).slice(0, 32);
  return `${VERLUNE_ACCESS_KEY_VERSION}_${entitlementId.slice(5)}_${signature}`;
}

export function verifyVerluneAccessKeyWithSecret(
  emailInput: string,
  observed: string,
  secret: string,
  productTag: string
): boolean {
  const email = normalizeVerluneEmail(emailInput);
  if (!isValidVerluneEmail(email) || !VERLUNE_ACCESS_KEY_PATTERN.test(observed)) return false;
  try {
    return safeEqual(
      createVerluneAccessKeyWithSecret(email, secret, productTag),
      observed
    );
  } catch {
    return false;
  }
}
