import fs from "node:fs";
import path from "node:path";

const nextRoot = path.resolve(process.cwd(), ".next");
const requiredFragments = [
  "free/developer-starter-pack",
  "developer-pack",
  "license",
  "api/free-pack/v1",
  "api/free-pack/v1.1.0",
  "api/commerce/developer-pack/checkout",
  "api/commerce/lemonsqueezy/webhook",
];

function walk(dir, out = []) {
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) walk(full, out);
    else if (entry.isFile() && entry.name.includes("manifest") && entry.name.endsWith(".json")) out.push(full);
  }
  return out;
}

if (!fs.existsSync(nextRoot)) {
  console.error("GOLDEN PATH BUILD PARITY: FAIL — .next does not exist");
  process.exit(1);
}

const manifests = walk(nextRoot);
if (!manifests.length) {
  console.error("GOLDEN PATH BUILD PARITY: FAIL — no Next.js manifests found");
  process.exit(1);
}

let corpus = "";
const inspected = [];
for (const file of manifests) {
  try {
    const raw = fs.readFileSync(file, "utf8");
    JSON.parse(raw);
    corpus += `\n${raw.replaceAll("\\\\", "/")}`;
    inspected.push(path.relative(process.cwd(), file));
  } catch {
    // Ignore non-JSON or partially generated files; only valid JSON manifests count.
  }
}

const missing = requiredFragments.filter((fragment) => !corpus.includes(fragment));
if (missing.length) {
  console.error("GOLDEN PATH BUILD PARITY: FAIL");
  console.error(`missing=${missing.join(",")}`);
  console.error(`manifests_inspected=${inspected.length}`);
  process.exit(1);
}

console.log("GOLDEN PATH BUILD PARITY: PASS");
console.log(`required_routes=${requiredFragments.length}`);
console.log(`manifests_inspected=${inspected.length}`);
console.log("boundary=build route presence only; runtime/provider behavior not implied");
