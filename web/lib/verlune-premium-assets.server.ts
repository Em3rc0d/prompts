import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import path from "node:path";

import { getPremiumAssetMeta, type PremiumAssetMeta } from "./verlune-premium-catalog";

const PRIVATE_ROOT = path.join(process.cwd(), ".verlune-private", "premium");

export async function readPremiumAsset(assetId: string): Promise<{ meta: PremiumAssetMeta; content: string }> {
  const meta = getPremiumAssetMeta(assetId);
  if (!meta) throw new Error("premium_asset_not_found");

  const absolute = path.join(PRIVATE_ROOT, meta.relativePath);
  if (!absolute.startsWith(PRIVATE_ROOT + path.sep)) throw new Error("premium_asset_path_escape");

  const content = await readFile(absolute, "utf8");
  const digest = createHash("sha1").update(`blob ${Buffer.byteLength(content, "utf8")}\0`).update(content).digest("hex");
  if (digest !== meta.sourceBlobSha) {
    throw new Error(`premium_asset_identity_mismatch:${assetId}:${digest}`);
  }
  return { meta, content };
}
