import {
  releaseCheckoutCustomData as buildReleaseCheckoutCustomData,
  type CommerceGate,
  type CommerceReleaseIdentity,
} from "./commerce-release";

export const STARTER_CODE_REVIEW_RELEASE = Object.freeze({
  productId: "prompt-machine-starter-code-review-edition",
  version: "1.0.0-rc2",
  archiveName: "prompt-machine-starter-code-review-edition-v1.0.0-rc2.zip",
  archiveSize: 19161,
  archiveSha256: "1f141d705d8bc26d469cc84f68b7a0612bb6db2eaa744c3f5d68c08dd533eb88",
  sourceCommit: "c2e9667f4382e589d1430db609215d369486bbfe",
} as const satisfies CommerceReleaseIdentity);

export type { CommerceGate };

export function starterCodeReviewCheckoutCustomData(gate: CommerceGate): Record<string, string> {
  return buildReleaseCheckoutCustomData(STARTER_CODE_REVIEW_RELEASE, gate);
}
