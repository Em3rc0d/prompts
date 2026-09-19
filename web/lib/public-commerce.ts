// Server-only availability projection. Never pass provider configuration to clients.
import { currentStarterCodeReviewCommerceMode } from "./commerce-mode";

export function isCodeReviewPurchaseAvailable(): boolean {
  if (currentStarterCodeReviewCommerceMode() !== "live" ||
      process.env.NEXT_PUBLIC_STARTER_CODE_REVIEW_SALE_STATUS !== "LIVE") return false;
  const checkoutUrl = process.env.LEMONSQUEEZY_STARTER_CODE_REVIEW_LIVE_CHECKOUT_URL;
  if (!checkoutUrl) return false;
  try { return new URL(checkoutUrl).protocol === "https:"; }
  catch { return false; }
}
