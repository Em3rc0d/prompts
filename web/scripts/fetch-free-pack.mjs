import fs from "node:fs";
import path from "node:path";
import { createHash } from "node:crypto";

const EXPECTED_SHA256 = "55455f134da0486ca43c6b09dcff722a4295a1fc9ed3b1caf2c046902e76ea32";
const EXPECTED_SIZE = 23498;
const ZIP_ROOT = "prompt-quarry-developer-starter-v1";
const UTF8_FLAG = 0x0800;
const DOS_TIME = 0;
const DOS_DATE = 0x21;
const VERSION_NEEDED = 20;
const VERSION_MADE_BY = (3 << 8) | 20;
const UNIX_FILE_MODE = 0o100644;

const productRoot = path.resolve(process.cwd(), "..", "product", "free-developer-starter-v1");
const manifestPath = path.join(productRoot, "MANIFEST.release.json");

function sha256(buffer) {
  return createHash("sha256").update(buffer).digest("hex");
}

function gitBlobSha1(buffer) {
  return createHash("sha1")
    .update(`blob ${buffer.length}\0`)
    .update(buffer)
    .digest("hex");
}

function crc32(data) {
  let crc = 0xffffffff;
  for (const byte of data) {
    crc ^= byte;
    for (let bit = 0; bit < 8; bit += 1) {
      crc = (crc >>> 1) ^ ((crc & 1) ? 0xedb88320 : 0);
    }
  }
  return (crc ^ 0xffffffff) >>> 0;
}

function buildStoredZip(entries) {
  const localChunks = [];
  const centralChunks = [];
  let offset = 0;

  const sorted = [...entries].sort((a, b) => a.path < b.path ? -1 : a.path > b.path ? 1 : 0);

  for (const entry of sorted) {
    const archiveName = Buffer.from(`${ZIP_ROOT}/${entry.path}`, "utf8");
    const data = entry.data;
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

const manifest = JSON.parse(fs.readFileSync(manifestPath, "utf8"));
if (manifest.schema !== "prompt-quarry-free-pack-release-v1") {
  throw new Error("FREE PACK MATERIALIZE FAIL: unexpected manifest schema");
}

const assets = Array.isArray(manifest.assets) ? manifest.assets : [];
if (assets.length !== 7) {
  throw new Error(`FREE PACK MATERIALIZE FAIL: expected 7 assets, observed ${assets.length}`);
}

const manifestPaths = assets.map((asset) => asset.path);
const sortedPaths = [...manifestPaths].sort((a, b) => a < b ? -1 : a > b ? 1 : 0);
if (JSON.stringify(manifestPaths) !== JSON.stringify(sortedPaths)) {
  throw new Error("FREE PACK MATERIALIZE FAIL: manifest asset paths are not lexicographically sorted");
}

const entries = assets.map((asset) => {
  const absolute = path.join(productRoot, asset.path);
  const data = fs.readFileSync(absolute);
  const observedSha256 = sha256(data);
  const observedGitBlob = gitBlobSha1(data);

  if (data.length !== asset.size_bytes) {
    throw new Error(`FREE PACK MATERIALIZE FAIL: size mismatch ${asset.path}`);
  }
  if (observedGitBlob !== asset.git_blob_sha1) {
    throw new Error(`FREE PACK MATERIALIZE FAIL: git blob mismatch ${asset.path}`);
  }
  if (`sha256:${observedSha256}` !== asset.sha256) {
    throw new Error(`FREE PACK MATERIALIZE FAIL: sha256 mismatch ${asset.path}`);
  }
  return { path: asset.path, data };
});

const archive = buildStoredZip(entries);
const observed = sha256(archive);
if (archive.length !== EXPECTED_SIZE || observed !== EXPECTED_SHA256) {
  throw new Error(`FREE PACK MATERIALIZE FAIL: size=${archive.length} sha256=${observed}`);
}

const remoteSource = process.env.PQ_FREE_PACK_RELEASE_SOURCE?.trim();
if (remoteSource) {
  const response = await fetch(remoteSource, { redirect: "error", cache: "no-store" });
  if (!response.ok) throw new Error(`FREE PACK REMOTE VERIFY FAIL: HTTP ${response.status}`);
  const remote = Buffer.from(await response.arrayBuffer());
  const remoteHash = sha256(remote);
  if (remote.length !== archive.length || remoteHash !== observed || !remote.equals(archive)) {
    throw new Error(`FREE PACK REMOTE VERIFY FAIL: size=${remote.length} sha256=${remoteHash}`);
  }
  console.log(`remote_verified=${remoteSource}`);
}

const dir = path.resolve(process.cwd(), "generated");
fs.mkdirSync(dir, { recursive: true });
const output = `// Generated by scripts/fetch-free-pack.mjs from governed local release bytes. Do not hand-edit.\nexport const FREE_PACK_BASE64 = ${JSON.stringify(archive.toString("base64"))};\n`;
fs.writeFileSync(path.join(dir, "free-pack-archive.ts"), output, "utf8");

console.log("FREE PACK MATERIALIZE: PASS");
console.log("source=local-governed-manifest");
console.log(`assets=${entries.length}`);
console.log(`size=${archive.length}`);
console.log(`sha256=${observed}`);
