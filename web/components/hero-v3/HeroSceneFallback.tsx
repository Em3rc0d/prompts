export function HeroSceneFallback() {
  return <div className="vHero3Fallback" aria-hidden="true">
    <div className="vHero3FallbackField" />
    <span className="vHero3FallbackOrbit vHero3FallbackOrbit--outer" />
    <span className="vHero3FallbackOrbit vHero3FallbackOrbit--inner" />
    <div className="vHero3FallbackStack">
      <span className="vHero3FallbackSlab vHero3FallbackSlab--base" />
      <span className="vHero3FallbackSlab vHero3FallbackSlab--lower" />
      <span className="vHero3FallbackSlab vHero3FallbackSlab--middle" />
      <span className="vHero3FallbackSlab vHero3FallbackSlab--top" />
      <span className="vHero3FallbackSeal">V</span>
    </div>
  </div>;
}
