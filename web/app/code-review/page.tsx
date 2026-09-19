import type { Metadata } from "next";
import Link from "next/link";
import { ProductActions } from "@/components/product-actions";
import { ReviewExample } from "@/components/review-example";
import { CODE_REVIEW as product, codeReviewPrice } from "@/lib/public-products";
import { STARTER_CODE_REVIEW_RELEASE } from "@/lib/starter-code-review-release";

// Availability follows server configuration at request time, never a stale static CTA.
export const dynamic = "force-dynamic";
export const metadata: Metadata = {
  title: product.name,
  description: `${product.summary} ${codeReviewPrice} USD ${product.billingModel}. A downloadable workflow with operating guidance and explicit evidence boundaries.`,
  alternates: { canonical: "/code-review" },
};

const steps = [
  ["Change", "Start with the code or diff."],
  ["Context", "State intent and constraints."],
  ["Evidence", "Separate observations from inference."],
  ["Findings", "Make each issue traceable."],
  ["Severity", "Rank impact, with uncertainty visible."],
  ["Verification", "Identify checks that resolve the risk."],
  ["Human decision", "Decide what is ready to ship."],
];
const faqs = [
  ["Is this just a prompt?", "The core is a text-based workflow you add to an AI session. The package also provides a quickstart, operating guidance, evidence disclosure, and release information. Its value is a repeatable review process with a defined output structure and verification guidance."],
  ["What do I receive?", `Version ${product.version} of the digital package: the workflow and ${product.contents.length - 1} supporting files. See the full contents above.`],
  ["How do I use it?", "Add the workflow to your AI session, provide the code or diff and relevant context, run the review, and verify findings before acting. Start with the included quickstart. An AI-provider account and any provider usage fees are separate."],
  ["Which AI systems can I use it with?", `The declared behavioral evidence covers ${product.evidenceSummary.model}. You may experiment with other compatible systems, but those models are outside the tested scope; equivalent behavior is not established.`],
  ["What has actually been tested?", `Pack QA passed ${product.evidenceSummary.packQA}. The exact declared four-case final regression has ${product.evidenceSummary.regression} on ${product.evidenceSummary.model}. These results cover that workflow and test scope, not every codebase or model.`],
  ["Does it automatically approve code?", "No. It is advisory. Findings, unknowns, and verification guidance support a human decision. It does not guarantee correctness, security, compliance, or detection of every defect."],
  ["Can I adapt it?", "Yes, the paid license permits adaptation for your own internal use and use on personal, commercial, and client software projects. It does not permit redistribution of the workflow itself. The packaged customer license defines the full terms."],
  ["Is it a subscription?", `No. ${codeReviewPrice} USD is a ${product.billingModel} purchase of the delivered version. AI access, future versions, consulting, and ongoing support are not included. Taxes and the final payable amount are shown at checkout.`],
  ["How is it delivered?", "When purchasing is available, an authorized successful purchase is delivered through Lemon Squeezy’s digital-product delivery mechanism as a ZIP download. The package includes a quickstart and an integrity manifest."],
];

export default function CodeReviewPage() {
  return <main>
    <section className="pageHero"><div className="wrap productHero"><div>
      <div className="eyebrow">A WORKFLOW FOR THE CHANGE IN FRONT OF YOU</div>
      <h1>{product.name}</h1><p className="lead">{product.summary}</p><p className="productOutcome">{product.outcome}</p>
      <div className="productMeta"><span><strong>{codeReviewPrice}</strong> USD {product.billingModel}</span><span>Version {product.version}</span><span>Digital product</span></div>
      <ProductActions />
    </div><aside className="reviewPromise"><span className="eyebrow">A BETTER REVIEW STARTS WITH</span><h2>Show the evidence.<br />Name the unknowns.</h2><ul className="checkList"><li>Consistent review structure</li><li>Evidence-ranked findings</li><li>Severity with context</li><li>Practical verification guidance</li><li>A human-controlled ship decision</li></ul></aside></div></section>

    <section className="section"><div className="wrap splitHeader"><div><div className="eyebrow">LESS SETUP. MORE SIGNAL.</div><h2>“Review this” leaves too much unsaid.</h2></div><div><p className="sectionIntro">A blank chat makes you rebuild the review every time. One answer focuses on style; another sounds confident without showing its evidence.</p><p>This workflow gives the review a consistent structure: what changed, what supports a finding, what is still unknown, and what you should verify. Missing context stays visible instead of disappearing into a polished answer.</p></div></div></section>

    <section className="section"><div className="wrap"><div className="splitHeader"><div><div className="eyebrow">THE REVIEW PROCESS</div><h2>From a change<br />to an informed decision.</h2></div><p className="sectionIntro">Each step gives the next one something concrete to work with. A finding is a claim to investigate, not permission to ship.</p></div><ol className="reviewFlow">{steps.map(([title, body], i) => <li key={title}><span className="stepNumber">0{i + 1}</span><div><h3>{title}</h3><p>{body}</p></div>{i < steps.length - 1 && <span className="flowArrow" aria-hidden="true">↓</span>}</li>)}</ol></div></section>

    <section className="section" id="inside"><div className="wrap"><div className="splitHeader"><div><div className="eyebrow">WHAT YOU RECEIVE</div><h2>One download.<br />A complete starting point.</h2></div><p className="sectionIntro">A real digital package you can keep, inspect, and use in your own AI session. No hosted code-review service or model subscription is included.</p></div><ol className="contentsGrid">{product.contents.map((name, i) => <li key={name}><span className="stepNumber">{String(i + 1).padStart(2, "0")}</span><span>{name}</span></li>)}</ol><p className="micro">ZIP archive · {product.contents.length} files · Version {product.version}</p></div></section>

    <section className="section"><div className="wrap"><div className="eyebrow">HOW TO USE IT</div><h2>Bring your own code.<br />Keep your own judgment.</h2><ol className="workflowRail fourSteps">{[
      ["Add the workflow", "Load it into your AI session using the quickstart."],
      ["Provide the context", "Include the code, diff, intended behavior, and relevant constraints."],
      ["Run the review", "Work through the structured findings and explicit unknowns."],
      ["Verify before shipping", "Check the evidence and run the suggested checks. You decide."],
    ].map(([title, text], i) => <li key={title}><span className="stepNumber">0{i + 1}</span><h3>{title}</h3><p>{text}</p></li>)}</ol></div></section>

    <section className="section"><div className="wrap exampleSection"><div><div className="eyebrow">THE SHAPE OF A USEFUL FINDING</div><h2>Specific enough<br />to check.</h2><p className="sectionIntro">Evidence, uncertainty, and a concrete next check belong together. This illustrative example shows the structure; it is not a testimonial or a recorded execution.</p></div><ReviewExample /></div></section>

    <section className="section" id="evidence"><div className="wrap"><div className="splitHeader"><div><div className="eyebrow">EVIDENCE WITH BOUNDARIES</div><h2>Know what was tested.</h2></div><p className="sectionIntro">Model-specific evidence is not universal portability. Workflow evidence is not a guarantee of correctness, security, or compliance.</p></div><div className="evidenceStats"><div><strong>{product.evidenceSummary.packQA}</strong><span>Pack QA</span></div><div><strong>4/4</strong><span>Human-review passes · exact declared final regression</span></div><div><strong>{product.evidenceSummary.model}</strong><span>Tested declared model scope</span></div></div>
      <details className="disclosure"><summary>Release identity and exact workflow scope</summary><div className="disclosureBody"><p>The recorded evidence applies to the exact workflow bytes and declared test matrix. Running a modified workflow or using another model does not inherit that evidence.</p><dl className="releaseFacts"><div><dt>Archive</dt><dd><code>{STARTER_CODE_REVIEW_RELEASE.archiveName}</code></dd></div><div><dt>Archive SHA-256</dt><dd><code>{STARTER_CODE_REVIEW_RELEASE.archiveSha256}</code></dd></div><div><dt>Certified workflow</dt><dd>{product.evidenceSummary.workflowBytes.toLocaleString("en-US")} bytes</dd></div><div><dt>Workflow SHA-256</dt><dd><code>{product.evidenceSummary.workflowSha256}</code></dd></div></dl><p>Read the packaged evidence disclosure and integrity manifest for the release scope.</p></div></details>
    </div></section>

    <section className="section"><div className="wrap purchaseSummary"><div><div className="eyebrow">A FOCUSED TOOL FOR YOUR REVIEW PROCESS</div><h2>{product.name}</h2><p>{product.contents.length} files. A reusable workflow. No subscription.</p><Link className="textLink" href="/license">Read the license summary →</Link></div><div><div className="price">{codeReviewPrice}<span>USD {product.billingModel}</span></div><p className="micro">Version {product.version} · Provider fees separate · Taxes shown at checkout</p><ProductActions /></div></div></section>

    <section className="section"><div className="wrap faqLayout"><div><div className="eyebrow">BEFORE YOU START</div><h2>Good questions.</h2></div><div>{faqs.map(([question, answer]) => <details className="disclosure" key={question}><summary>{question}</summary><div className="disclosureBody"><p>{answer}</p></div></details>)}</div></div></section>
  </main>;
}
