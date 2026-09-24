import { currentCommerceMode, type CommerceMode } from "./commerce-mode";
import { getVerluneAccessConfigState } from "./verlune-access";

export const VERLUNE_PREMIUM_CANDIDATE_PRICE_USD = 9;

export type VerlunePremiumCommerceState = {
  mode: CommerceMode;
  publicSaleLive: boolean;
  checkoutConfigured: boolean;
  accessConfigured: boolean;
  purchaseAvailable: boolean;
};

export function getVerlunePremiumCommerceState(): VerlunePremiumCommerceState {
  const mode = currentCommerceMode("VERLUNE_PREMIUM_COMMERCE_MODE");
  const publicSaleLive = process.env.VERLUNE_PREMIUM_PUBLIC_SALE_STATUS === "LIVE";
  const checkoutUrl = mode === "test"
    ? process.env.LEMONSQUEEZY_VERLUNE_PREMIUM_TEST_CHECKOUT_URL
    : mode === "live"
      ? process.env.LEMONSQUEEZY_VERLUNE_PREMIUM_LIVE_CHECKOUT_URL
      : undefined;
  const accessConfigured = getVerluneAccessConfigState().ready;
  const checkoutConfigured = Boolean(checkoutUrl?.trim());

  return {
    mode,
    publicSaleLive,
    checkoutConfigured,
    accessConfigured,
    purchaseAvailable: mode === "live" && publicSaleLive && checkoutConfigured && accessConfigured
  };
}
