const concepts = [
  { key: "prompt", label: "PROMPT", detail: "Structured input", mark: "≡" },
  { key: "workflow", label: "WORKFLOW", detail: "Stages + decisions", mark: "◇" },
  { key: "builder", label: "BUILDER", detail: "Build yours", mark: "▱" },
  { key: "verify", label: "VERIFY", detail: "Verify", mark: "✓" }
] as const;

export function HeroSemanticCards() {
  return <ul className="vHero3Cards" aria-label="Elements of structured AI work">
    {concepts.map(({ key, label, detail, mark }) => <li className={`vHero3Card vHero3Card--${key}`} key={key}>
      <span className="vHero3CardMark" aria-hidden="true">{mark}</span>
      <span className="vHero3CardCopy"><span className="vHero3CardLabel">{label}</span><strong>{detail}</strong></span>
    </li>)}
  </ul>;
}
