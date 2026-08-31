export const DEVELOPER_PACK_RELEASE = Object.freeze({
  productId: "pq-developer-pack",
  version: "1.1.0",
  archiveName: "prompt-quarry-developer-pack-v1.1.0.zip",
  archiveSize: 86763,
  archiveSha256: "546a7568abb0c546034740ee1418d76b1496e1cf9f6b31ab30d5e509eacc5009",
  sourceFingerprintSha256: "dd61138ef8f8fee811c6437e05eabcd8742f8787746736213525731e934fdffa",
  sourceCommit: "f0accde4aa12ecf4eae530249cb56175e5a28b66",
} as const);

export type CommerceGate = "provider_test" | "live";

export function releaseCheckoutCustomData(gate: CommerceGate): Record<string, string> {
  return {
    pq_product_id: DEVELOPER_PACK_RELEASE.productId,
    pq_product_version: DEVELOPER_PACK_RELEASE.version,
    pq_archive_sha256: DEVELOPER_PACK_RELEASE.archiveSha256,
    pq_archive_size: String(DEVELOPER_PACK_RELEASE.archiveSize),
    pq_gate: gate,
  };
}
