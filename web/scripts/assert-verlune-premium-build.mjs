import fs from "node:fs";
import path from "node:path";

const cwd = process.cwd();
const nextRoot = path.join(cwd, ".next");
const privateRoot = path.join(cwd, ".verlune-private", "premium");

const requiredPrivateFiles = [
  "prompts/requirements-analysis.md",
  "prompts/exam-preparation.md",
  "prompts/evidence-synthesis.md",
  "prompts/sop-drafting.md",
  "prompts/rewrite-for-audience-and-intent.md",
  "prompts/content-strategy-brief.md",
  "prompts/risk-aware-project-plan.md",
  "prompts/tailor-a-resume-to-a-role.md",
  "workflows/evidence-first-code-review.md",
  "workflows/evidence-first-deep-research.md",
  "workflows/decision-analysis.md",
  "workflows/master-a-topic.md",
  "workflows/content-strategy-system.md",
  "builders/prompt-builder.md",
  "builders/workflow-builder.md",
  "toolkit/adaptation-guide.md",
  "toolkit/evaluation-toolkit.md"
];

const requiredRouteFragments = [
  "unlock/page",
  "app/page",
  "app/asset/[assetId]/page",
  "app/access/page",
  "api/verlune/unlock",
  "api/verlune/session/revalidate",
  "api/verlune/logout",
  "api/verlune/deactivate"
];

const protectedMarkers = [
  "Your job is to help me turn a recurring task into a clear, reusable prompt",
  "Your job is to turn a recurring AI-assisted process into a reusable workflow",
  "An absent matching registry entry, missing source, or failed lookup is not by itself proof"
];

function walk(dir, predicate = () => true, out = []) {
  if (!fs.existsSync(dir)) return out;
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(full, predicate, out);
    else if (entry.isFile() && predicate(full)) out.push(full);
  }
  return out;
}

function fail(message) {
  console.error("VERLUNE PREMIUM BUILD AUDIT: FAIL");
  console.error(message);
  process.exit(1);
}

if (!fs.existsSync(nextRoot)) fail(".next does not exist");
if (!fs.existsSync(privateRoot)) fail("private Premium materialization does not exist");

const missingPrivate = requiredPrivateFiles.filter((rel) => !fs.existsSync(path.join(privateRoot, rel)));
if (missingPrivate.length) fail(`missing_private_assets=${missingPrivate.join(",")}`);

const manifestFiles = walk(nextRoot, (file) => file.endsWith(".json") && file.includes("manifest"));
let manifestCorpus = "";
for (const file of manifestFiles) {
  try {
    manifestCorpus += "\n" + fs.readFileSync(file, "utf8").replaceAll("\\", "/");
  } catch {}
}
const missingRoutes = requiredRouteFragments.filter((fragment) => !manifestCorpus.includes(fragment));
if (missingRoutes.length) fail(`missing_routes=${missingRoutes.join(",")}`);

const publicRoots = [path.join(cwd, "public"), path.join(nextRoot, "static")];
const publicFiles = publicRoots.flatMap((root) =>
  walk(root, (file) => /\.(?:js|css|json|html|txt|map)$/i.test(file))
);

for (const file of publicFiles) {
  let raw;
  try { raw = fs.readFileSync(file, "utf8"); } catch { continue; }
  for (const marker of protectedMarkers) {
    if (raw.includes(marker)) {
      fail(`premium_content_leaked_to_public_bundle=${path.relative(cwd, file)}`);
    }
  }
}

console.log("VERLUNE PREMIUM BUILD AUDIT: PASS");
console.log(`private_launch_core_assets=${requiredPrivateFiles.length}`);
console.log(`protected_routes=${requiredRouteFragments.length}`);
console.log(`public_files_scanned=${publicFiles.length}`);
console.log("boundary=build/materialization/public-bundle audit only; entitlement provider behavior not implied");
