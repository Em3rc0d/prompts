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

export async function GET() {
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
