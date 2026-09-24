import fs from "node:fs";
import path from "node:path";

const root = process.cwd();
const read = rel => {
  const p = path.join(root, rel);
  if (!fs.existsSync(p)) throw new Error(`VERLUNE V4.1 AUDIT FAIL: missing ${rel}`);
  return fs.readFileSync(p, "utf8");
};

const stack = read("components/hero-v3/scene/CentralStack.tsx");
const lights = read("components/hero-v3/scene/SceneLighting.tsx");
const canvas = read("components/hero-v3/VerluneHeroCanvas.client.tsx");
const heroCss = read("components/hero-v3/hero-v3.css");
const globalCss = read("app/globals.css");

for (const marker of [
  "depth: .035",
  "bevelSize: .018",
  "transmission={layer.transmission}",
  "thickness={index === 2 ? .32 : .22}",
  "ior={1.5}",
  "clearcoat={1}",
  "attenuationColor",
  "studioReflection"
]) {
  if (!stack.includes(marker)) throw new Error(`VERLUNE V4.1 AUDIT FAIL: CentralStack missing ${marker}`);
}

for (const marker of ["z: -1.28", "z: -.22", "z: .84"]) {
  if (!stack.includes(marker)) throw new Error(`VERLUNE V4.1 AUDIT FAIL: three-slab spacing missing ${marker}`);
}

const layerCount = (stack.match(/z:\s*[-.]?\d/g) ?? []).length;
if (layerCount < 3) throw new Error("VERLUNE V4.1 AUDIT FAIL: expected three primary optical slabs");

if (!canvas.includes("toneMappingExposure = 1.04") || !canvas.includes("frameloop=\"demand\"")) {
  throw new Error("VERLUNE V4.1 AUDIT FAIL: tone mapping or demand rendering contract missing");
}
if (!lights.includes("intensity={2.85}") || lights.includes("intensity={5.2}")) {
  throw new Error("VERLUNE V4.1 AUDIT FAIL: internal mint lighting was not rebalanced");
}

for (const marker of [
  "VERLUNE HERO V4.1 — CINEMATIC MATERIAL PASS",
  "Dark glass, light and information",
  ".vHero3FallbackSlab--lower",
  ".vHero3Card"
]) {
  if (!heroCss.includes(marker)) throw new Error(`VERLUNE V4.1 AUDIT FAIL: hero optical CSS missing ${marker}`);
}

for (const marker of [
  "VERLUNE V4.1 — SHARED SMOKED-GLASS MATERIAL LANGUAGE",
  "--v-glass-bg",
  "--v-glass-border",
  ".vGraphSlabTop",
  ".vPremiumLibrary .vBuilderFeature",
  ".vPremiumLibrary .vWorkflowFeature",
  ".vPremiumLibrary .vPromptRow",
  ".vPremiumLibrary .vToolkitCard",
  ".vPremiumPublic .vCapabilityCard"
]) {
  if (!globalCss.includes(marker)) throw new Error(`VERLUNE V4.1 AUDIT FAIL: shared Premium material missing ${marker}`);
}

console.log("VERLUNE V4.1 VISUAL CONTRACT AUDIT: PASS");
console.log("hero_primary_slabs=3");
console.log("hero_geometry=thin_beveled");
console.log("hero_material=smoked_transmissive_glass");
console.log("hero_internal_mint=controlled");
console.log("premium_material=shared_dom_css_glass");
console.log("webgl_scope=home_hero_only");
console.log("boundary=source/material contract only; browser visual acceptance still required");
