import { cp, mkdir, readdir, readFile, rm, writeFile } from "node:fs/promises";
import { createHash } from "node:crypto";
import { fileURLToPath } from "node:url";
import path from "node:path";

const source = fileURLToPath(new URL("../../product/verlune-v1/premium/", import.meta.url));
const target = fileURLToPath(new URL("../.verlune-private/premium/", import.meta.url));

await rm(target, { recursive: true, force: true });
await mkdir(path.dirname(target), { recursive: true });
await cp(source, target, { recursive: true, force: true });

async function walk(dir, prefix = "") {
  const entries = await readdir(dir, { withFileTypes: true });
  const out = [];
  for (const entry of entries) {
    const rel = path.posix.join(prefix, entry.name);
    const absolute = path.join(dir, entry.name);
    if (entry.isDirectory()) out.push(...await walk(absolute, rel));
    else if (entry.isFile() && entry.name.endsWith(".md")) out.push({ rel, absolute });
  }
  return out;
}

const files = await walk(target);
const manifest = [];
for (const file of files) {
  const bytes = await readFile(file.absolute);
  const sha = createHash("sha1")
    .update(`blob ${bytes.length}\0`)
    .update(bytes)
    .digest("hex");
  manifest.push({ path: file.rel, bytes: bytes.length, git_blob_sha: sha });
}

manifest.sort((a, b) => a.path.localeCompare(b.path));
await writeFile(
  path.join(path.dirname(target), "manifest.json"),
  JSON.stringify({ schema: "verlune-private-materialization-v1", files: manifest }, null, 2) + "\n",
  "utf8"
);

console.log(`VERLUNE_PRIVATE_MATERIALIZED files=${manifest.length}`);
