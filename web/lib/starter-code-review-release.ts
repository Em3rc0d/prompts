import {
  releaseCheckoutCustomData as buildReleaseCheckoutCustomData,
  type CommerceGate,
  type CommerceReleaseIdentity,
} from "./commerce-release";

export const STARTER_CODE_REVIEW_RELEASE = Object.freeze({
  productId: "prompt-machine-starter-code-review-edition",
  version: "1.0.0-rc1",
  archiveName: "prompt-machine-starter-code-review-edition-v1.0.0-rc1.zip",
  archiveSize: 14667,
  archiveSha256: "7ec282ea1766679f425fd5aad526d6382e6a3c5af2caab9ded07e55b9a773cde",
  sourceCommit: "010bc9400c7804160644d7f60ee9134c8546f63b",
} as const satisfies CommerceReleaseIdentity);

export type { CommerceGate };

export function starterCodeReviewCheckoutCustomData(gate: CommerceGate): Record<string, string> {
  return buildReleaseCheckoutCustomData(STARTER_CODE_REVIEW_RELEASE, gate);
}
