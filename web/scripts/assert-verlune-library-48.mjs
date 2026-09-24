import fs from "node:fs";
import path from "node:path";
import { createHash } from "node:crypto";

const root = process.cwd();
const productRoot = path.resolve(root, "../product/verlune-v1");

function fail(message) {
  console.error("VERLUNE LIBRARY 48 AUDIT: FAIL");
  console.error(message);
  process.exit(1);
}

function read(rel) {
  const p = path.resolve(root, rel);
  if (!fs.existsSync(p)) fail(`missing ${rel}`);
  return fs.readFileSync(p, "utf8");
}

function parseCatalog(source, prefix) {
  const out = [];
  const pattern = /\{\s*id:\s*"([^"]+)",\s*name:\s*"([^"]+)",\s*type:\s*"Prompt",\s*category:\s*"([^"]+)",\s*categoryLabel:\s*"([^"]+)",\s*relativePath:\s*"([^"]+)",\s*sourceBlobSha:\s*"([^"]+)",\s*summary:\s*"([^"]+)"\s*\}/g;
  for (const m of source.matchAll(pattern)) {
    if (m[1].startsWith(prefix)) out.push({id:m[1],name:m[2],category:m[3],relativePath:m[5],sha:m[6],summary:m[7]});
  }
  return out;
}

function gitBlobSha(bytes) {
  return createHash("sha1").update(`blob ${bytes.length}\0`).update(bytes).digest("hex");
}

const freeCatalogSource = read("lib/verlune-free-catalog.ts");
const premiumCatalogSource = read("lib/verlune-premium-catalog.ts");
const free = parseCatalog(freeCatalogSource, "VF-P-");
const premium = parseCatalog(premiumCatalogSource, "VP-P-");

if (free.length !== 16) fail(`expected 16 Free prompts, got ${free.length}`);
if (premium.length !== 32) fail(`expected 32 Premium prompts, got ${premium.length}`);

const categories = [
  "development-tech",
  "study-learning",
  "research-analysis",
  "business-operations",
  "writing-communication",
  "content-marketing",
  "planning-productivity",
  "career-job-search"
];

for (const category of categories) {
  const fc = free.filter(x => x.category === category).length;
  const pc = premium.filter(x => x.category === category).length;
  if (fc !== 2) fail(`${category}: expected 2 Free prompts, got ${fc}`);
  if (pc !== 4) fail(`${category}: expected 4 Premium prompts, got ${pc}`);
}

const ids = [...free, ...premium].map(x => x.id);
if (new Set(ids).size !== ids.length) fail("duplicate prompt IDs");

const names = [...free, ...premium].map(x => x.name.toLowerCase().trim());
if (new Set(names).size !== names.length) fail("duplicate prompt names");

const normalizedBodies = new Map();

const newIds = new Set([
  "VF-P-DEV-002","VF-P-STUDY-002","VF-P-RES-002","VF-P-BIZ-002",
  "VF-P-WRITE-002","VF-P-CONTENT-002","VF-P-PLAN-002","VF-P-CAREER-002",
  "VP-P-DEV-002","VP-P-DEV-003","VP-P-DEV-004",
  "VP-P-STUDY-002","VP-P-STUDY-003","VP-P-STUDY-004",
  "VP-P-RES-003","VP-P-RES-004","VP-P-RES-005",
  "VP-P-BIZ-002","VP-P-BIZ-003","VP-P-BIZ-004",
  "VP-P-WRITE-002","VP-P-WRITE-003","VP-P-WRITE-004",
  "VP-P-CONTENT-002","VP-P-CONTENT-003","VP-P-CONTENT-004",
  "VP-P-PLAN-002","VP-P-PLAN-003","VP-P-PLAN-004",
  "VP-P-CAREER-002","VP-P-CAREER-003","VP-P-CAREER-004"
]);

for (const [tier, assets] of [["free", free], ["premium", premium]]) {
  for (const asset of assets) {
    const file = path.join(productRoot, tier, asset.relativePath);
    if (!fs.existsSync(file)) fail(`${asset.id}: missing source ${tier}/${asset.relativePath}`);
    const raw = fs.readFileSync(file);
    const normalized = Buffer.from(raw.toString("utf8").replace(/\r\n?/g, "\n"), "utf8");
    const actualSha = gitBlobSha(normalized);
    if (actualSha !== asset.sha) fail(`${asset.id}: sourceBlobSha mismatch expected=${asset.sha} actual=${actualSha}`);

    const body = normalized.toString("utf8");
    if (!body.startsWith(`# ${asset.name}\n`)) fail(`${asset.id}: title does not match catalog name`);

    for (const marker of ["## Prompt", "RULES", "OUTPUT"]) {
      if (!body.includes(marker)) fail(`${asset.id}: missing baseline structural marker ${marker}`);
    }

    if (newIds.has(asset.id)) {
      if (!body.includes("VERIFICATION")) fail(`${asset.id}: new prompt missing explicit VERIFICATION`);
      if (tier === "premium" && !body.includes("PROCESS")) fail(`${asset.id}: new Premium prompt missing explicit PROCESS`);
    }

    const normalizedPrompt = body
      .replace(/^# .*$/m, "")
      .replace(/Status:.*$/m, "")
      .replace(/\s+/g, " ")
      .trim()
      .toLowerCase();

    const previous = normalizedBodies.get(normalizedPrompt);
    if (previous) fail(`exact normalized duplicate: ${previous} and ${asset.id}`);
    normalizedBodies.set(normalizedPrompt, asset.id);
  }
}

console.log("VERLUNE LIBRARY 48 AUDIT: PASS");
console.log("free_prompts=16");
console.log("premium_prompts=32");
console.log("total_prompts=48");
console.log("free_distribution=2_per_category");
console.log("premium_distribution=4_per_category");
console.log("source_identity=git_blob_sha_verified");
console.log("structure=static_contract_checked");
console.log("runtime_execution=NOT_RUN_BY_THIS_AUDIT");
console.log("behavioral_certification=NOT_IMPLIED");
