import { HeroSceneFallback } from "./HeroSceneFallback";
import { HeroCanvasGate } from "./HeroCanvasGate.client";
import { HeroSemanticCards } from "./HeroSemanticCards";

export function VerluneHeroScene() {
  return <div className="vHero3" role="group" aria-label="Verlune structure with prompts, workflows, Builders and verification">
    <HeroCanvasGate />
    <HeroSceneFallback />
    <HeroSemanticCards />
  </div>;
}
