import { createHash } from "node:crypto";
import {
  FREE_PACK_ARCHIVE_SHA256,
  FREE_PACK_ARCHIVE_SIZE,
  FREE_PACK_FILENAME,
  FREE_PACK_FILES,
  FREE_PACK_VERSION,
} from "@/generated/free-developer-starter-v1";

export const runtime = "nodejs";

const ATTRIBUTION_FIELDS = ["source", "medium", "campaign", "content"] as const;
const ZIP_ROOT = "prompt-quarry-developer-starter-v1";
const UTF8_FLAG = 0x0800;
const DOS_TIME = 0;
const DOS_DATE = 0x21;
const VERSION_NEEDED = 20;
const VERSION_MADE_BY = (3 << 8) | 20;
const UNIX_FILE_MODE = 0o100644;

function clean(value: string | null): string | undefined {
  if (!value) return undefined;
  const normalized = value.trim().slice(0, 120);
  return normalized ? normalized.replace(/[^a-zA-Z0-9._:/-]/g, "-") : undefined;
}

function crc32(data: Buffer): number {
  let crc = 0xffffffff;
  for (const byte of data) {
    crc ^= byte;
    for (let bit = 0; bit < 8; bit += 1) {
      crc = (crc >>> 1) ^ ((crc & 1) ? 0xedb88320 : 0);
    }
  }
  return (crc ^ 0xffffffff) >>> 0;
}

export function buildStoredZip(entries: ReadonlyArray<{ path: string; content: string }>): Buffer {
  const localChunks: Buffer[] = [];
  const centralChunks: Buffer[] = [];
  let offset = 0;

  for (const entry of [...entries].sort((a, b) => a.path.localeCompare(b.path))) {
    const data = Buffer.from(entry.content, "utf8");
    const archiveName = Buffer.from(`${ZIP_ROOT}/${entry.path}`, "utf8");
    const crc = crc32(data);

    const localHeader = Buffer.alloc(30);
    localHeader.writeUInt32LE(0x04034b50, 0);
    localHeader.writeUInt16LE(VERSION_NEEDED, 4);
    localHeader.writeUInt16LE(UTF8_FLAG, 6);
    localHeader.writeUInt16LE(0, 8);
    localHeader.writeUInt16LE(DOS_TIME, 10);
    localHeader.writeUInt16LE(DOS_DATE, 12);
    localHeader.writeUInt32LE(crc, 14);
    localHeader.writeUInt32LE(data.length, 18);
    localHeader.writeUInt32LE(data.length, 22);
    localHeader.writeUInt16LE(archiveName.length, 26);
    localHeader.writeUInt16LE(0, 28);

    const localRecord = Buffer.concat([localHeader, archiveName, data]);
    localChunks.push(localRecord);

    const centralHeader = Buffer.alloc(46);
    centralHeader.writeUInt32LE(0x02014b50, 0);
    centralHeader.writeUInt16LE(VERSION_MADE_BY, 4);
    centralHeader.writeUInt16LE(VERSION_NEEDED, 6);
    centralHeader.writeUInt16LE(UTF8_FLAG, 8);
    centralHeader.writeUInt16LE(0, 10);
    centralHeader.writeUInt16LE(DOS_TIME, 12);
    centralHeader.writeUInt16LE(DOS_DATE, 14);
    centralHeader.writeUInt32LE(crc, 16);
    centralHeader.writeUInt32LE(data.length, 20);
    centralHeader.writeUInt32LE(data.length, 24);
    centralHeader.writeUInt16LE(archiveName.length, 28);
    centralHeader.writeUInt16LE(0, 30);
    centralHeader.writeUInt16LE(0, 32);
    centralHeader.writeUInt16LE(0, 34);
    centralHeader.writeUInt16LE(0, 36);
    centralHeader.writeUInt32LE((UNIX_FILE_MODE << 16) >>> 0, 38);
    centralHeader.writeUInt32LE(offset, 42);
    centralChunks.push(Buffer.concat([centralHeader, archiveName]));

    offset += localRecord.length;
  }

  const localBlob = Buffer.concat(localChunks);
  const centralBlob = Buffer.concat(centralChunks);
  const endRecord = Buffer.alloc(22);
  endRecord.writeUInt32LE(0x06054b50, 0);
  endRecord.writeUInt16LE(0, 4);
  endRecord.writeUInt16LE(0, 6);
  endRecord.writeUInt16LE(entries.length, 8);
  endRecord.writeUInt16LE(entries.length, 10);
  endRecord.writeUInt32LE(centralBlob.length, 12);
  endRecord.writeUInt32LE(localBlob.length, 16);
  endRecord.writeUInt16LE(0, 20);

  return Buffer.concat([localBlob, centralBlob, endRecord]);
}

export async function GET(request: Request) {
  const archive = buildStoredZip(FREE_PACK_FILES);
  const observedHash = createHash("sha256").update(archive).digest("hex");

  if (archive.length !== FREE_PACK_ARCHIVE_SIZE || observedHash !== FREE_PACK_ARCHIVE_SHA256) {
    return Response.json({
      ok: false,
      error: "free_pack_integrity_failure",
      observed_size: archive.length,
      observed_sha256: observedHash,
    }, { status: 500 });
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

  return new Response(new Uint8Array(archive), { headers: {
    "Content-Type": "application/zip",
    "Content-Disposition": `attachment; filename="${FREE_PACK_FILENAME}"`,
    "Content-Length": String(archive.length),
    "Cache-Control": "public, max-age=31536000, immutable",
    ETag: `"sha256-${observedHash}"`,
    "X-Prompt-Quarry-Version": FREE_PACK_VERSION,
    "X-Prompt-Quarry-SHA256": observedHash,
    "X-Prompt-Quarry-Origin": "deterministic-governed-payload",
  }});
}
