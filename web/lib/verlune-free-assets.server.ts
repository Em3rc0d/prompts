import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import path from "node:path";

import { getFreeAssetMeta, type FreeAssetMeta } from "./verlune-free-catalog";

const FREE_ROOT = path.join(process.cwd(), ".verlune-public", "free");

export async function readFreeAsset(assetId: string): Promise<{ meta: FreeAssetMeta; content: string }> {
  const meta = getFreeAssetMeta(assetId);
  if (!meta) throw new Error("free_asset_not_found");

  const absolute = path.join(FREE_ROOT, meta.relativePath);
  if (!absolute.startsWith(FREE_ROOT + path.sep)) throw new Error("free_asset_path_escape");

  const content = await readFile(absolute, "utf8");
  const digest = createHash("sha1").update(`blob ${Buffer.byteLength(content, "utf8")}\0`).update(content).digest("hex");
  if (digest !== meta.sourceBlobSha) {
    throw new Error(`free_asset_identity_mismatch:${assetId}:${digest}`);
  }

  return { meta, content };
}
