export type CommerceGate = "provider_test" | "live_canary" | "live";

export type CommerceReleaseIdentity = Readonly<{
  productId: string;
  version: string;
  archiveName: string;
  archiveSize: number;
  archiveSha256: string;
  sourceCommit: string;
}>;

export function releaseCheckoutCustomData(
  release: CommerceReleaseIdentity,
  gate: CommerceGate,
): Record<string, string> {
  return {
    pq_product_id: release.productId,
    pq_product_version: release.version,
    pq_archive_sha256: release.archiveSha256,
    pq_archive_size: String(release.archiveSize),
    pq_gate: gate,
  };
}
