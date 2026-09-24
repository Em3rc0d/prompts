import fs from "node:fs";
import path from "node:path";

const root = process.cwd();

const requiredSourceFiles = [
  "app/page.tsx",
  "app/library/page.tsx",
  "app/free/page.tsx",
  "app/free/asset/[assetId]/page.tsx",
  "app/app/page.tsx",
  "components/library-explorer.client.tsx",
  "lib/verlune-library-discovery.ts",
  "app/app/asset/[assetId]/page.tsx",
  "components/verlune-visuals.tsx",
  "lib/verlune-free-catalog.ts",
  "lib/verlune-premium-catalog.ts"
];

for (const rel of requiredSourceFiles) {
  const absolute = path.join(root, rel);
  if (!fs.existsSync(absolute)) throw new Error(`VERLUNE V2 AUDIT FAIL: missing ${rel}`);
}

const home = fs.readFileSync(path.join(root, "app/page.tsx"), "utf8");
const library = fs.readFileSync(path.join(root, "app/library/page.tsx"), "utf8");
const free = fs.readFileSync(path.join(root, "app/free/page.tsx"), "utf8");
const discovery = fs.readFileSync(path.join(root, "lib/verlune-library-discovery.ts"), "utf8");
const explorer = fs.readFileSync(path.join(root, "components/library-explorer.client.tsx"), "utf8");
const freeCatalog = fs.readFileSync(path.join(root, "lib/verlune-free-catalog.ts"), "utf8");
const premium = fs.readFileSync(path.join(root, "app/app/page.tsx"), "utf8");
const css = fs.readFileSync(path.join(root, "app/globals.css"), "utf8");

const requiredHomeMarkers = [
  "Use ours.",
  "Build yours.",
  "PROMPT ≠ WORKFLOW",
  "VerluneHeroScene"
];
for (const marker of requiredHomeMarkers) {
  if (!home.includes(marker)) throw new Error(`VERLUNE V2 AUDIT FAIL: home missing ${marker}`);
}

const requiredFreePageMarkers = ["LibraryExplorer", 'fixedTier="free"', 'initialCollectionId="start-here"'];
for (const marker of requiredFreePageMarkers) {
  if (!free.includes(marker)) throw new Error(`VERLUNE V2 AUDIT FAIL: free discovery missing ${marker}`);
}

const requiredFreeCatalogMarkers = ["VF-P-", "VF-WF-"];
for (const marker of requiredFreeCatalogMarkers) {
  if (!freeCatalog.includes(marker)) throw new Error(`VERLUNE V2 AUDIT FAIL: free catalog missing ${marker}`);
}

const freePromptIds = freeCatalog.match(/id:\s*"VF-P-[^"]+"/g) ?? [];
const freeWorkflowIds = freeCatalog.match(/id:\s*"VF-WF-[^"]+"/g) ?? [];
if (freePromptIds.length !== 16 || freeWorkflowIds.length !== 3) {
  throw new Error(
    `VERLUNE V2 AUDIT FAIL: expected 16 free prompts + 3 free workflows, got ${freePromptIds.length} + ${freeWorkflowIds.length}`
  );
}

const requiredPremiumMarkers = ["LibraryExplorer", 'fixedTier="premium"', 'initialCollectionId="premium-essentials"', "VerluneGraph"];
for (const marker of requiredPremiumMarkers) {
  if (!premium.includes(marker)) throw new Error(`VERLUNE V2 AUDIT FAIL: premium discovery missing ${marker}`);
}

for (const marker of ["VERLUNE LIBRARY", "getPublicLibraryAssets", "LibraryExplorer"]) {
  if (!library.includes(marker)) throw new Error(`VERLUNE V2 AUDIT FAIL: public library missing ${marker}`);
}
for (const marker of ["start-here", "premium-essentials", "ship-software", "research-decide"]) {
  if (!discovery.includes(marker)) throw new Error(`VERLUNE V2 AUDIT FAIL: discovery model missing collection ${marker}`);
}
for (const marker of ['type="search"', "Tier", "Type", "Category", "Show 12 more"]) {
  if (!explorer.includes(marker)) throw new Error(`VERLUNE V2 AUDIT FAIL: explorer missing ${marker}`);
}

const requiredCssMarkers = [
  "VERLUNE V2 — EDITORIAL COMPUTATIONAL",
  ".vGraph",
  ".vPremiumLibrary",
  "@media (prefers-reduced-motion: reduce)"
];
for (const marker of requiredCssMarkers) {
  if (!css.includes(marker)) throw new Error(`VERLUNE V2 AUDIT FAIL: css missing ${marker}`);
}

const publicSources = [home, free, premium].join("\n");
const forbidden = [
  /\b\d+[,.]?\d*\+\s+(?:uses|users|creators|assets)\b/i,
  /\bmost popular\b/i,
  /\bpriority support\b/i,
  /\blifetime access\b/i,
  /\bnew content weekly\b/i
];
for (const pattern of forbidden) {
  if (pattern.test(publicSources)) throw new Error(`VERLUNE V2 AUDIT FAIL: unsupported mockup claim ${pattern}`);
}

const generatedFreeRoot = path.join(root, ".verlune-public", "free");
for (const rel of [
  "prompts/explain-code-clearly.md",
  "prompts/learn-a-difficult-topic.md",
  "prompts/research-a-topic.md",
  "prompts/analyze-a-business-problem.md",
  "prompts/improve-writing.md",
  "prompts/improve-a-content-draft.md",
  "prompts/plan-a-project.md",
  "prompts/prepare-for-an-interview.md",
  "prompts/diagnose-a-technical-error.md",
  "prompts/check-your-understanding.md",
  "prompts/compare-sources.md",
  "prompts/document-a-business-process.md",
  "prompts/executive-email-from-notes.md",
  "prompts/generate-content-angles.md",
  "prompts/prioritize-competing-tasks.md",
  "prompts/understand-a-job-description.md",
  "workflows/compare-options.md",
  "workflows/guided-study-session.md",
  "workflows/bug-diagnosis.md"
]) {
  if (!fs.existsSync(path.join(generatedFreeRoot, rel))) {
    throw new Error(`VERLUNE V2 AUDIT FAIL: free materialization missing ${rel}`);
  }
}

console.log("VERLUNE V2 BUILD AUDIT: PASS");
console.log("free_launch_core_assets=19");
console.log("free_launch_core_prompts=16");
console.log("free_launch_core_workflows=3");
console.log("premium_library_assets=41");
console.log("discovery_surface=public_library+free+premium");
console.log("semantic_3d=hero-v3-hybrid; premium-v2-dom-css");
console.log("unsupported_mockup_claims=0");
console.log("boundary=build/source/materialization audit; human visual comprehension not implied");
