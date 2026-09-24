import fs from "node:fs";
import path from "node:path";

const read = rel => fs.readFileSync(path.join(process.cwd(), rel), "utf8");
const home = read("app/page.tsx");
const shell = read("components/hero-v3/VerluneHeroScene.tsx");
const gate = read("components/hero-v3/HeroCanvasGate.client.tsx");
const canvas = read("components/hero-v3/VerluneHeroCanvas.client.tsx");
const cards = read("components/hero-v3/HeroSemanticCards.tsx");
const css = read("components/hero-v3/hero-v3.css");

const checks = [
  [!home.startsWith('"use client"'), "homepage must remain a server component"],
  [home.includes("<VerluneHeroScene />") && home.includes("href=\"/free\"") && home.includes("href=\"/unlock\""), "server hero/CTAs missing"],
  [shell.includes("<HeroSceneFallback />") && shell.includes("<HeroSemanticCards />"), "server fallback or semantic cards missing"],
  [gate.includes('dynamic(() => import("./VerluneHeroCanvas.client")') && gate.includes("ssr: false"), "WebGL runtime must be lazy"],
  [gate.includes('min-width: 900px') && gate.includes('prefers-reduced-motion: reduce') && gate.includes('getContext("webgl2")'), "responsive/reduced-motion/WebGL gate missing"],
  [gate.includes("CanvasBoundary") && gate.includes("setReady(false)"), "runtime failure must restore fallback"],
  [canvas.includes('frameloop="demand"') && canvas.includes("<CentralStack />"), "demand rendering or central object missing"],
  [cards.includes("Structured input") && cards.includes("Stages + decisions") && cards.includes("Build yours") && cards.includes("Verify"), "DOM product concepts missing"],
  [css.includes("@media (max-width: 599px)") && css.includes("@media (prefers-reduced-motion: reduce)"), "mobile/reduced motion CSS missing"],
];
for (const [passes, message] of checks) if (!passes) throw new Error(`VERLUNE HERO V3 AUDIT FAIL: ${message}`);
console.log("VERLUNE HERO V3 BUILD AUDIT: PASS");
console.log("boundary=source architecture only; WebGL visual fidelity and runtime behavior need browser review");
