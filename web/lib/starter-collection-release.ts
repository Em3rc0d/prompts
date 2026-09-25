import {
  releaseCheckoutCustomData as buildReleaseCheckoutCustomData,
  type CommerceGate,
  type CommerceReleaseIdentity,
} from "./commerce-release";

export const STARTER_COLLECTION_RELEASE = Object.freeze({
  productId: "prompt-machine-starter-collection",
  version: "1.0.0-candidate",
  archiveName: "prompt-machine-starter-collection-v1.zip",
  archiveSize: 50918,
  archiveSha256: "4eceb1ee567b43760902da2787139ea897165ff97bb69ecbe56f35432f220b97",
  sourceCommit: "167faad0758b3e746b48ac7c898f876525d30ee3",
} as const satisfies CommerceReleaseIdentity);

export type { CommerceGate };

export function starterReleaseCheckoutCustomData(gate: CommerceGate): Record<string, string> {
  return buildReleaseCheckoutCustomData(STARTER_COLLECTION_RELEASE, gate);
}
