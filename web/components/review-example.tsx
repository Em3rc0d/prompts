export function ReviewExample() {
  return <figure className="reviewExample">
    <figcaption><span>REVIEW / FINDING 01</span><span>Illustrative example</span></figcaption>
    <div className="exampleBody">
      <div className="findingHeading"><span className="severity">HIGH · IF CONFIRMED</span><span className="micro">Authorization</span></div>
      <h3>A signed-in user may access another user’s invoice.</h3>
      <dl className="findingFields">
        <div><dt>Evidence</dt><dd>The supplied handler loads an invoice by ID without an ownership check.</dd></div>
        <div><dt>Unknown</dt><dd>Route middleware and database policies were not provided.</dd></div>
        <div><dt>Verify</dt><dd>Use two test accounts. Request account B’s invoice as account A; confirm the request is denied.</dd></div>
        <div><dt>Decision</dt><dd>Resolve the authorization question before shipping. The developer makes the final call.</dd></div>
      </dl>
    </div>
    <div className="exampleFoot">Representative structure · Not a recorded model result</div>
  </figure>;
}
