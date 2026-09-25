import "server-only";

import { createHmac, timingSafeEqual } from "node:crypto";

export const VERLUNE_PREMIUM_TEST_SESSION_COOKIE = "verlune-premium-provider-test";
export const VERLUNE_PREMIUM_TEST_SESSION_MAX_AGE_SECONDS = 15 * 60;

const PURPOSE = "verlune-premium-provider-test:v1";

function safeEqual(expected: string | undefined, observed: string | null | undefined): boolean {
  if (!expected || !observed) return false;
  const expectedBytes = Buffer.from(expected, "utf8");
  const observedBytes = Buffer.from(observed, "utf8");
  return expectedBytes.length === observedBytes.length && timingSafeEqual(expectedBytes, observedBytes);
}

export function providerTestTokenMatches(observed: string | null | undefined): boolean {
  return safeEqual(process.env.VERLUNE_PREMIUM_PROVIDER_TEST_TOKEN?.trim(), observed?.trim());
}

export function premiumTestSessionValue(): string | null {
  const providerToken = process.env.VERLUNE_PREMIUM_PROVIDER_TEST_TOKEN?.trim();
  const sessionSecret = process.env.VERLUNE_SESSION_SECRET?.trim();
  if (!providerToken || !sessionSecret || sessionSecret.length < 32) return null;
  return createHmac("sha256", sessionSecret)
    .update(`${PURPOSE}:${providerToken}`)
    .digest("hex");
}

export function premiumTestSessionMatches(observed: string | null | undefined): boolean {
  return safeEqual(premiumTestSessionValue() ?? undefined, observed);
}
