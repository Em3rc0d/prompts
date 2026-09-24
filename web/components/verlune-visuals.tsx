type VerluneGraphProps = {
  variant?: "hero" | "library" | "compact";
  label?: string;
};

export function VerluneGraph({ variant = "hero", label = "Structured AI work" }: VerluneGraphProps) {
  return <div className={`vGraph vGraph--${variant}`} role="img" aria-label={label}>
    <div className="vGraphGrid" aria-hidden="true" />
    <div className="vGraphOrbit vGraphOrbitA" aria-hidden="true" />
    <div className="vGraphOrbit vGraphOrbitB" aria-hidden="true" />

    <div className="vGraphStack" aria-hidden="true">
      <span className="vGraphSlab vGraphSlabBottom" />
      <span className="vGraphSlab vGraphSlabMid" />
      <span className="vGraphSlab vGraphSlabTop" />
      <span className="vGraphCore"><b>V</b></span>
    </div>

    <div className="vGraphBlock vGraphBlockPrompt" aria-hidden="true">
      <span className="vGraphKicker">PROMPT</span>
      <strong>Structured input</strong>
      <i />
      <i />
    </div>
    <div className="vGraphBlock vGraphBlockWorkflow" aria-hidden="true">
      <span className="vGraphKicker">WORKFLOW</span>
      <strong>Stages + decisions</strong>
      <span className="vMiniFlow"><i /><i /><i /></span>
    </div>
    <div className="vGraphBlock vGraphBlockBuilder" aria-hidden="true">
      <span className="vGraphKicker">BUILDER</span>
      <strong>Build yours</strong>
      <i />
    </div>
    <div className="vGraphBlock vGraphBlockVerify" aria-hidden="true">
      <span className="vVerifyMark">✓</span>
      <strong>Verify</strong>
    </div>

    <span className="vGraphNode vGraphNodeA" aria-hidden="true" />
    <span className="vGraphNode vGraphNodeB" aria-hidden="true" />
    <span className="vGraphNode vGraphNodeC" aria-hidden="true" />
  </div>;
}

export function ArtifactMiniObject({ type }: { type: "Prompt" | "Workflow" | "Builder" | "Toolkit" }) {
  return <div className={`vMiniObject vMiniObject--${type.toLowerCase()}`} aria-hidden="true">
    <span className="vMiniObjectBack" />
    <span className="vMiniObjectMid" />
    <span className="vMiniObjectFront">
      {type === "Workflow"
        ? <span className="vMiniObjectFlow"><i /><i /><i /></span>
        : type === "Builder"
          ? <span className="vMiniObjectCube">◇</span>
          : type === "Toolkit"
            ? <span className="vMiniObjectCheck">✓</span>
            : <span className="vMiniObjectLines"><i /><i /><i /></span>}
    </span>
  </div>;
}

export function AssetStructureMap({ type }: { type: "Prompt" | "Workflow" | "Builder" | "Toolkit" }) {
  const maps = {
    Prompt: ["Input", "Rules", "Output", "Verify"],
    Workflow: ["Trigger", "Stages", "Decision", "Verify", "Output"],
    Builder: ["Need", "Guided intake", "Artifact", "Quick test"],
    Toolkit: ["Input", "Method", "Check", "Adapt"]
  } as const;

  return <div className="vStructureMap" aria-label={`${type} structure`}>
    {maps[type].map((step, index) => <div className="vStructureStep" key={step}>
      <span className="vStructureNode">{String(index + 1).padStart(2, "0")}</span>
      <strong>{step}</strong>
      {index < maps[type].length - 1 ? <span className="vStructureArrow" aria-hidden="true">→</span> : null}
    </div>)}
  </div>;
}
