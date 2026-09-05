import { currentStarterCommerceMode } from "./commerce-mode";
import type { LemonSqueezyConfig } from "./lemonsqueezy";
import { STARTER_COLLECTION_RELEASE, type CommerceGate } from "./starter-collection-release";

export type StarterCommerceRuntime = {
  config: LemonSqueezyConfig;
  checkoutUrl: string;
  commerceGate: CommerceGate;
  publicSaleLive: boolean;
};

export function loadStarterCommerceRuntime(): StarterCommerceRuntime | null {
  const commerceMode = currentStarterCommerceMode();
  if (commerceMode === "off") return null;

  const publicSaleLive = process.env.NEXT_PUBLIC_STARTER_COLLECTION_SALE_STATUS === "LIVE";
  if (commerceMode === "test" && publicSaleLive) return null;

  const webhookSecret = process.env.LEMONSQUEEZY_WEBHOOK_SECRET;
  const storeId = process.env.LEMONSQUEEZY_STORE_ID;
  const productId = process.env.LEMONSQUEEZY_STARTER_PRODUCT_ID;
  const variantId = process.env.LEMONSQUEEZY_STARTER_VARIANT_ID;
  if (!webhookSecret || !storeId || !productId || !variantId) return null;

  const commerceGate: CommerceGate = commerceMode === "test"
    ? "provider_test"
    : publicSaleLive
      ? "live"
      : "live_canary";

  const checkoutUrl = commerceMode === "test"
    ? process.env.LEMONSQUEEZY_STARTER_TEST_CHECKOUT_URL
    : process.env.LEMONSQUEEZY_STARTER_LIVE_CHECKOUT_URL;
  if (!checkoutUrl) return null;

  let parsed: URL;
  try {
    parsed = new URL(checkoutUrl);
  } catch {
    return null;
  }
  if (parsed.protocol !== "https:") return null;

  return {
    config: {
      webhookSecret,
      storeId,
      productId,
      variantId,
      commerceMode,
      commerceGate,
      release: STARTER_COLLECTION_RELEASE,
    },
    checkoutUrl: parsed.toString(),
    commerceGate,
    publicSaleLive,
  };
}
