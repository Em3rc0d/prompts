import { mkdir, readdir, readFile, rm, writeFile } from "node:fs/promises";
import { fileURLToPath } from "node:url";
import path from "node:path";

const source = fileURLToPath(new URL("../../product/verlune-v1/free/", import.meta.url));
const target = fileURLToPath(new URL("../.verlune-public/free/", import.meta.url));

await rm(target, { recursive: true, force: true });
await mkdir(target, { recursive: true });

function normalizeTextBytes(bytes) {
  const text = bytes.toString("utf8").replace(/\r\n?/g, "\n");
  return Buffer.from(text, "utf8");
}

async function materializeTree(sourceDir, targetDir) {
  const entries = await readdir(sourceDir, { withFileTypes: true });
  let files = 0;

  for (const entry of entries) {
    const sourcePath = path.join(sourceDir, entry.name);
    const targetPath = path.join(targetDir, entry.name);

    if (entry.isDirectory()) {
      await mkdir(targetPath, { recursive: true });
      files += await materializeTree(sourcePath, targetPath);
      continue;
    }

    if (!entry.isFile() || !entry.name.endsWith(".md")) continue;
    const sourceBytes = await readFile(sourcePath);
    await writeFile(targetPath, normalizeTextBytes(sourceBytes));
    files += 1;
  }

  return files;
}

const files = await materializeTree(source, target);
console.log(`VERLUNE_FREE_MATERIALIZED files=${files}`);
console.log("text_normalization=CRLF/CR-to-LF-for-markdown");
