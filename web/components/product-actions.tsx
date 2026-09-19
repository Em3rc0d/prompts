import Link from "next/link";
import { CommerceLink } from "./commerce-link";
import { isCodeReviewPurchaseAvailable } from "@/lib/public-commerce";
import { CODE_REVIEW, codeReviewPrice } from "@/lib/public-products";

export function ProductActions() {
  const available = isCodeReviewPurchaseAvailable();
  return <div className="productActions">
    <div className="actions">
      {available
        ? <CommerceLink kind="code-review">Get Code Review — {codeReviewPrice}</CommerceLink>
        : <Link className="btn btnPrimary" href="/free">Try free workflows <span aria-hidden="true">↗</span></Link>}
      <a className="btn btnSecondary" href="#inside">See what’s inside</a>
    </div>
    <p className="micro">{available
      ? `${CODE_REVIEW.billingModel} purchase · Digital download · AI access sold separately.`
      : "Public purchasing is not open yet. Explore the full product below or start with the free workflows."}</p>
  </div>;
}
