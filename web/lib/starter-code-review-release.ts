import {
  releaseCheckoutCustomData as buildReleaseCheckoutCustomData,
  type CommerceGate,
  type CommerceReleaseIdentity,
} from "./commerce-release";

// Internal machine id remains stable for historical/provider continuity.
// Buyer-facing brand/product name is Verlune Code Review.
export const STARTER_CODE_REVIEW_RELEASE = Object.freeze({
  productId: "prompt-machine-starter-code-review-edition",
  version: "1.0.0",
  archiveName: "verlune-code-review-v1.0.0.zip",
  archiveSize: 18859,
  archiveSha256: "4d7def57143c53fd0b99cf26b57a36b12215f671c52a12f0564a34aa239f9649",
  sourceCommit: "a6c6b4c79606bdc1b386980da34675a66feb4b4a",
} as const satisfies CommerceReleaseIdentity);

export type { CommerceGate };

export function starterCodeReviewCheckoutCustomData(gate: CommerceGate): Record<string, string> {
  return buildReleaseCheckoutCustomData(STARTER_CODE_REVIEW_RELEASE, gate);
}
