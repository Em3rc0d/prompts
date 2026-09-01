const stages = [
  { id: "01", name: "RAW", meta: "intent + context" },
  { id: "02", name: "STRUCTURE", meta: "constraints + contract" },
  { id: "03", name: "VALIDATE", meta: "quality + evidence" },
  { id: "04", name: "PRODUCT", meta: "versioned artifact" },
];

export function QuarryEngine() {
  return (
    <div className="engineShell" aria-label="Prompt Quarry pipeline visualization">
      <div className="engineChrome">
        <div className="engineTitle">
          <span className="engineMark" aria-hidden="true">PQ</span>
          <div>
            <strong>QUARRY ENGINE</strong>
            <span>developer pipeline / build 01</span>
          </div>
        </div>
        <div className="engineLive"><span /> SYSTEM READY</div>
      </div>

      <div className="engineStageRail">
        {stages.map((stage, index) => (
          <div className="engineStage" key={stage.id}>
            <span className="engineStageIndex">{stage.id}</span>
            <div>
              <strong>{stage.name}</strong>
              <small>{stage.meta}</small>
            </div>
            {index < stages.length - 1 && <span className="engineConnector" aria-hidden="true" />}
          </div>
        ))}
      </div>

      <div className="engineWorkspace">
        <div className="engineInput">
          <div className="enginePanelLabel">RAW REQUEST</div>
          <p>“Review this service and tell me what&apos;s wrong.”</p>
          <div className="engineSignalRow">
            <span>context <b>?</b></span>
            <span>constraints <b>?</b></span>
            <span>output <b>?</b></span>
          </div>
        </div>

        <div className="engineTransform" aria-hidden="true">
          <span className="engineBeam" />
          <span className="engineCore">→</span>
        </div>

        <div className="engineOutput">
          <div className="enginePanelLabel">STRUCTURED ASSET</div>
          <div className="engineCode">
            <span><i>01</i><b>PURPOSE</b> review reliability + risk</span>
            <span><i>02</i><b>CONTEXT</b> service role + boundaries</span>
            <span><i>03</i><b>CONSTRAINTS</b> evidence before inference</span>
            <span><i>04</i><b>OUTPUT</b> findings → severity → fix</span>
            <span><i>05</i><b>UNKNOWN</b> not observed = unknown</span>
          </div>
        </div>
      </div>

      <div className="engineFooter">
        <span>artifact / pq-dev-review</span>
        <span className="engineHash">sha256 · governed · VALID</span>
      </div>
    </div>
  );
}
