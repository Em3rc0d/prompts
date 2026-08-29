import { createHash } from "node:crypto";

export const runtime = "nodejs";

const RELEASE_ORIGIN = "https://prompt-quarry-mx9ioitln-faridmerinos-projects.vercel.app/api/free-pack/v1.1.0";
const EXPECTED_SHA256 = "55455f134da0486ca43c6b09dcff722a4295a1fc9ed3b1caf2c046902e76ea32";
const EXPECTED_SIZE = 23498;
const VERSION = "1.1.0";
const FILENAME = "prompt-quarry-developer-starter-v1.1.0.zip";
const ATTRIBUTION_FIELDS = ["source", "medium", "campaign", "content"] as const;

function clean(value: string | null): string | undefined {
  if (!value) return undefined;
  const normalized = value.trim().slice(0, 120);
  if (!normalized) return undefined;
  return normalized.replace(/[^a-zA-Z0-9._:/-]/g, "-");
}

export async function GET(request: Request) {
  let upstream: Response;
  try {
    upstream = await fetch(RELEASE_ORIGIN, { cache: "force-cache" });
  } catch {
    return Response.json({ ok: false, error: "release_origin_unavailable" }, { status: 503 });
  }

  if (!upstream.ok) {
    return Response.json({ ok: false, error: "release_origin_bad_status", status: upstream.status }, { status: 503 });
  }

  const archive = Buffer.from(await upstream.arrayBuffer());
  const observedHash = createHash("sha256").update(archive).digest("hex");
  if (archive.length !== EXPECTED_SIZE || observedHash !== EXPECTED_SHA256) {
    return Response.json({ ok: false, error: "free_pack_integrity_failure", expected_size: EXPECTED_SIZE, observed_size: archive.length, expected_sha256: EXPECTED_SHA256, observed_sha256: observedHash }, { status: 500 });
  }

  const url = new URL(request.url);
  const attribution: Record<string, string> = {};
  for (const field of ATTRIBUTION_FIELDS) {
    const value = clean(url.searchParams.get(field));
    if (value) attribution[field] = value;
  }

  console.info("PQ_FUNNEL_EVENT", JSON.stringify({ event: "free_pack_acquired", product_id: "pq-developer-starter", product_version: VERSION, archive_sha256: observedHash, timestamp: new Date().toISOString(), ...attribution }));

  return new Response(new Uint8Array(archive), { headers: {
    "Content-Type": "application/zip",
    "Content-Disposition": `attachment; filename="${FILENAME}"`,
    "Content-Length": String(archive.length),
    "Cache-Control": "public, max-age=31536000, immutable",
    ETag: `"sha256-${observedHash}"`,
    "X-Prompt-Quarry-Version": VERSION,
    "X-Prompt-Quarry-SHA256": observedHash,
    "X-Prompt-Quarry-Origin": "immutable-release",
  }});
}
