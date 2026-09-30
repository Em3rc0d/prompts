import { currentCommerceMode, type CommerceMode } from "./commerce-mode";
import { getVerluneAccessConfigState } from "./verlune-access";
import {
  getVerluneMercadoPagoConfigState,
  VERLUNE_PREMIUM_PRICE_USD
} from "./verlune-mercado-pago";

export const VERLUNE_PREMIUM_CANDIDATE_PRICE_USD = VERLUNE_PREMIUM_PRICE_USD;

export type VerlunePremiumCommerceState = {
  mode: CommerceMode;
  publicSaleLive: boolean;
  checkoutConfigured: boolean;
  accessConfigured: boolean;
  purchaseAvailable: boolean;
  provider: "mercado_pago";
  pricePenMinor: number;
};

export function getVerlunePremiumCommerceState(): VerlunePremiumCommerceState {
  const mode = currentCommerceMode("VERLUNE_PREMIUM_COMMERCE_MODE");
  const publicSaleLive = process.env.VERLUNE_PREMIUM_PUBLIC_SALE_STATUS === "LIVE";
  const mercadoPago = getVerluneMercadoPagoConfigState();
  const access = getVerluneAccessConfigState();
  const environmentMatches = mode === "test"
    ? mercadoPago.environment === "test"
    : mode === "live"
      ? mercadoPago.environment === "live"
      : false;

  const checkoutConfigured = mercadoPago.ready && environmentMatches && access.ready;
  return {
    mode,
    publicSaleLive,
    checkoutConfigured,
    accessConfigured: access.ready,
    purchaseAvailable: mode === "live" && publicSaleLive && checkoutConfigured,
    provider: "mercado_pago",
    pricePenMinor: mercadoPago.pricePenMinor
  };
}
