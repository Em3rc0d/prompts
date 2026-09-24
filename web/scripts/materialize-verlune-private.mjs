import { mkdir, readdir, readFile, rm, writeFile } from "node:fs/promises";
import { createHash } from "node:crypto";
import { fileURLToPath } from "node:url";
import path from "node:path";

const source = fileURLToPath(new URL("../../product/verlune-v1/premium/", import.meta.url));
const target = fileURLToPath(new URL("../.verlune-private/premium/", import.meta.url));

await rm(target, { recursive: true, force: true });
await mkdir(target, { recursive: true });

function normalizeTextBytes(bytes) {
  const text = bytes.toString("utf8").replace(/\r\n?/g, "\n");
  return Buffer.from(text, "utf8");
}

async function materializeTree(sourceDir, targetDir, prefix = "") {
  const entries = await readdir(sourceDir, { withFileTypes: true });
  const manifest = [];

  for (const entry of entries) {
    const sourcePath = path.join(sourceDir, entry.name);
    const targetPath = path.join(targetDir, entry.name);
    const rel = path.posix.join(prefix, entry.name);

    if (entry.isDirectory()) {
      await mkdir(targetPath, { recursive: true });
      manifest.push(...await materializeTree(sourcePath, targetPath, rel));
      continue;
    }

    if (!entry.isFile()) continue;

    const sourceBytes = await readFile(sourcePath);
    const bytes = entry.name.endsWith(".md") ? normalizeTextBytes(sourceBytes) : sourceBytes;
    await writeFile(targetPath, bytes);

    if (entry.name.endsWith(".md")) {
      const sha = createHash("sha1")
        .update(`blob ${bytes.length}\0`)
        .update(bytes)
        .digest("hex");
      manifest.push({ path: rel, bytes: bytes.length, git_blob_sha: sha });
    }
  }

  return manifest;
}

const manifest = await materializeTree(source, target);
manifest.sort((a, b) => a.path < b.path ? -1 : a.path > b.path ? 1 : 0);

await writeFile(
  path.join(path.dirname(target), "manifest.json"),
  JSON.stringify({
    schema: "verlune-private-materialization-v1",
    text_normalization: "CRLF/CR-to-LF-for-markdown",
    files: manifest
  }, null, 2) + "\n",
  "utf8"
);

console.log(`VERLUNE_PRIVATE_MATERIALIZED files=${manifest.length}`);
console.log("text_normalization=CRLF/CR-to-LF-for-markdown");
