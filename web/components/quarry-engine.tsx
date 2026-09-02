const stages = [
  { id: "01", name: "GOAL", meta: "what you need done" },
  { id: "02", name: "WORKFLOW", meta: "inputs + process" },
  { id: "03", name: "VERIFY", meta: "evidence + limits" },
  { id: "04", name: "REUSE", meta: "repeatable result" },
];

export function QuarryEngine() {
  return (
    <div className="engineShell" aria-label="Prompt Machine workflow visualization">
      <div className="engineChrome">
        <div className="engineTitle">
          <span className="engineMark" aria-hidden="true">PM</span>
          <div>
            <strong>WORKFLOW ENGINE</strong>
            <span>goal → workflow → verified output</span>
          </div>
        </div>
        <div className="engineLive"><span /> READY TO USE</div>
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
          <div className="enginePanelLabel">YOUR TASK</div>
          <p>“Review this service and tell me what actually matters.”</p>
          <div className="engineSignalRow">
            <span>context <b>✓</b></span>
            <span>constraints <b>✓</b></span>
            <span>output <b>✓</b></span>
          </div>
        </div>

        <div className="engineTransform" aria-hidden="true">
          <span className="engineBeam" />
          <span className="engineCore">→</span>
        </div>

        <div className="engineOutput">
          <div className="enginePanelLabel">REUSABLE WORKFLOW</div>
          <div className="engineCode">
            <span><i>01</i><b>INPUT</b> what the workflow needs</span>
            <span><i>02</i><b>PROCESS</b> repeatable steps</span>
            <span><i>03</i><b>BOUNDARY</b> evidence before inference</span>
            <span><i>04</i><b>OUTPUT</b> structured deliverable</span>
            <span><i>05</i><b>VERIFY</b> how to check the result</span>
          </div>
        </div>
      </div>

      <div className="engineFooter">
        <span>powered by Prompt Quarry</span>
        <span className="engineHash">versioned · governed · inspectable</span>
      </div>
    </div>
  );
}
