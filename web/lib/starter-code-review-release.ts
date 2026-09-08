import {
  releaseCheckoutCustomData as buildReleaseCheckoutCustomData,
  type CommerceGate,
  type CommerceReleaseIdentity,
} from "./commerce-release";

export const STARTER_CODE_REVIEW_RELEASE = Object.freeze({
  productId: "prompt-machine-starter-code-review-edition",
  version: "1.0.0",
  archiveName: "prompt-machine-starter-code-review-edition-v1.0.0.zip",
  archiveSize: 18955,
  archiveSha256: "9c313e5b71f4bcc2d48d32507c677e6f09f7cda6d7fe1b2fae16cb7386ecdcc3",
  sourceCommit: "04b8bceb4349bf79d8125f55592bbb6973edb3c1",
} as const satisfies CommerceReleaseIdentity);

export type { CommerceGate };

export function starterCodeReviewCheckoutCustomData(gate: CommerceGate): Record<string, string> {
  return buildReleaseCheckoutCustomData(STARTER_CODE_REVIEW_RELEASE, gate);
}
