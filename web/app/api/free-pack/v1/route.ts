import { createHash } from "node:crypto";
import {
  FREE_PACK_ARCHIVE_SHA256,
  FREE_PACK_ARCHIVE_SIZE,
  FREE_PACK_FILENAME,
  FREE_PACK_FILES,
  FREE_PACK_VERSION,
} from "@/generated/free-developer-starter-v1";
import { buildStoredZip } from "@/lib/deterministic-zip";

export const runtime = "nodejs";

const ATTRIBUTION_FIELDS = ["source", "medium", "campaign", "content"] as const;

function clean(value: string | null): string | undefined {
  if (!value) return undefined;
  const normalized = value.trim().slice(0, 120);
  if (!normalized) return undefined;
  return normalized.replace(/[^a-zA-Z0-9._:/-]/g, "-");
}

export async function GET(request: Request) {
  const archive = buildStoredZip(FREE_PACK_FILES);
  const observedHash = createHash("sha256").update(archive).digest("hex");

  if (
    observedHash !== FREE_PACK_ARCHIVE_SHA256 ||
    archive.length !== FREE_PACK_ARCHIVE_SIZE
  ) {
    return Response.json(
      {
        error: "free_pack_integrity_failure",
        expected_sha256: FREE_PACK_ARCHIVE_SHA256,
        observed_sha256: observedHash,
      },
      { status: 500 },
    );
  }

  const url = new URL(request.url);
  const attribution: Record<string, string> = {};
  for (const field of ATTRIBUTION_FIELDS) {
    const value = clean(url.searchParams.get(field));
    if (value) attribution[field] = value;
  }

  console.info("PQ_FUNNEL_EVENT", JSON.stringify({
    event: "free_pack_acquired",
    product_id: "pq-developer-starter",
    product_version: FREE_PACK_VERSION,
    archive_sha256: observedHash,
    timestamp: new Date().toISOString(),
    ...attribution,
  }));

  return new Response(new Uint8Array(archive), {
    headers: {
      "Content-Type": "application/zip",
      "Content-Disposition": `attachment; filename="${FREE_PACK_FILENAME}"`,
      "Content-Length": String(archive.length),
      "Cache-Control": "public, max-age=31536000, immutable",
      ETag: `"sha256-${observedHash}"`,
      "X-Prompt-Quarry-Version": FREE_PACK_VERSION,
      "X-Prompt-Quarry-SHA256": observedHash,
    },
  });
}
