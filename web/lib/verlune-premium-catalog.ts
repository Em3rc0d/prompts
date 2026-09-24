export type PremiumAssetType = "Prompt" | "Workflow" | "Builder" | "Toolkit";

export type PremiumAssetMeta = {
  id: string;
  name: string;
  type: PremiumAssetType;
  category: string;
  categoryLabel: string;
  relativePath: string;
  sourceBlobSha: string;
  summary: string;
};

export const PREMIUM_ASSETS: readonly PremiumAssetMeta[] = [
  {
    id: "VP-P-DEV-001",
    name: "Requirements Analysis",
    type: "Prompt",
    category: "development-tech",
    categoryLabel: "Development & Tech",
    relativePath: "prompts/requirements-analysis.md",
    sourceBlobSha: "4a401a6c48e6f8af1b922f076775452107dbd15f",
    summary: "Turn incomplete requirements into explicit needs, assumptions, constraints, and open questions."
  },
  {
    id: "VP-P-STUDY-001",
    name: "Exam Preparation",
    type: "Prompt",
    category: "study-learning",
    categoryLabel: "Study & Learning",
    relativePath: "prompts/exam-preparation.md",
    sourceBlobSha: "48f9ca9e2daa10a43bff15b6206278bef2f24ad4",
    summary: "Build an evidence-aware preparation plan around a real exam, scope, and available study time."
  },
  {
    id: "VP-P-RES-002",
    name: "Evidence Synthesis",
    type: "Prompt",
    category: "research-analysis",
    categoryLabel: "Research & Analysis",
    relativePath: "prompts/evidence-synthesis.md",
    sourceBlobSha: "fd7b99e9c2a7f73debb2e68b5b9205f20f5ac6cc",
    summary: "Synthesize supplied evidence without hiding contradictions, weak support, or important unknowns."
  },
  {
    id: "VP-P-BIZ-001",
    name: "SOP Drafting",
    type: "Prompt",
    category: "business-operations",
    categoryLabel: "Business & Operations",
    relativePath: "prompts/sop-drafting.md",
    sourceBlobSha: "4e766cab2870f001a98affbaf468f4a8e28b5a2e",
    summary: "Turn a real recurring process into a usable SOP without inventing policy or authority."
  },
  {
    id: "VP-P-WRITE-001",
    name: "Rewrite for Audience and Intent",
    type: "Prompt",
    category: "writing-communication",
    categoryLabel: "Writing & Communication",
    relativePath: "prompts/rewrite-for-audience-and-intent.md",
    sourceBlobSha: "867911106e6463c15ea8b3a575e10b4e41786f36",
    summary: "Rewrite for a specific reader and purpose while preserving factual and terminology boundaries."
  },
  {
    id: "VP-P-CONTENT-001",
    name: "Content Strategy Brief",
    type: "Prompt",
    category: "content-marketing",
    categoryLabel: "Content & Marketing",
    relativePath: "prompts/content-strategy-brief.md",
    sourceBlobSha: "bd1e26acc3f3237562b3a3e765bd6efb0b8f9f1d",
    summary: "Create a bounded strategy brief from real audience, offer, channel, and evidence inputs."
  },
  {
    id: "VP-P-PLAN-001",
    name: "Risk-Aware Project Plan",
    type: "Prompt",
    category: "planning-productivity",
    categoryLabel: "Planning & Productivity",
    relativePath: "prompts/risk-aware-project-plan.md",
    sourceBlobSha: "50dec50962b97ef525384de532494792fcbd3043",
    summary: "Plan a project with explicit dependencies, uncertainty, risks, validation, and stop conditions."
  },
  {
    id: "VP-P-CAREER-001",
    name: "Tailor a Resume to a Role",
    type: "Prompt",
    category: "career-job-search",
    categoryLabel: "Career & Job Search",
    relativePath: "prompts/tailor-a-resume-to-a-role.md",
    sourceBlobSha: "533174c537546642cdf082d59d91dececa297f0f",
    summary: "Adapt a resume to a real role without inventing experience, credentials, or achievements."
  },
  {
    id: "VP-P-DEV-002",
    name: "Design an Implementation Plan",
    type: "Prompt",
    category: "development-tech",
    categoryLabel: "Development & Tech",
    relativePath: "prompts/design-an-implementation-plan.md",
    sourceBlobSha: "ddffab9ed2e644a8b53a74d4c781f2cd6487eafd",
    summary: "Turn understood requirements into a dependency-aware implementation sequence with verification and readiness states."
  },
  {
    id: "VP-P-DEV-003",
    name: "Investigate a Production Failure",
    type: "Prompt",
    category: "development-tech",
    categoryLabel: "Development & Tech",
    relativePath: "prompts/investigate-a-production-failure.md",
    sourceBlobSha: "c1036f597bca734fe5a9925525ef1349182644e1",
    summary: "Investigate a live-system failure with factual timelines, falsifiable hypotheses, safe mitigation, and recovery evidence."
  },
  {
    id: "VP-P-DEV-004",
    name: "Review a Technical Design",
    type: "Prompt",
    category: "development-tech",
    categoryLabel: "Development & Tech",
    relativePath: "prompts/review-a-technical-design.md",
    sourceBlobSha: "c5f89de54567595e7a47ffc8a456fbbc196170b5",
    summary: "Review a proposed technical design against requirements, failure paths, assumptions, and requested quality attributes."
  },
  {
    id: "VP-P-STUDY-002",
    name: "Build a Learning Plan",
    type: "Prompt",
    category: "study-learning",
    categoryLabel: "Study & Learning",
    relativePath: "prompts/build-a-learning-plan.md",
    sourceBlobSha: "23344f01e6186fa71e39826be7d4cd65c3c39059",
    summary: "Build a learning path around demonstrated capability, prerequisites, practice, and observable milestones."
  },
  {
    id: "VP-P-STUDY-003",
    name: "Diagnose Knowledge Gaps",
    type: "Prompt",
    category: "study-learning",
    categoryLabel: "Study & Learning",
    relativePath: "prompts/diagnose-knowledge-gaps.md",
    sourceBlobSha: "ea8e86359a829bd05b96b71d435b8521eb5a254d",
    summary: "Locate specific knowledge, misconception, retrieval, or application gaps from observed performance."
  },
  {
    id: "VP-P-STUDY-004",
    name: "Learn From Source Material",
    type: "Prompt",
    category: "study-learning",
    categoryLabel: "Study & Learning",
    relativePath: "prompts/learn-from-source-material.md",
    sourceBlobSha: "a46b6330477c9857f2249d26869fcc5b3442f792",
    summary: "Learn from a supplied source while preserving its terminology, boundaries, ambiguity, and evidentiary scope."
  },
  {
    id: "VP-P-RES-003",
    name: "Competitive Landscape Analysis",
    type: "Prompt",
    category: "research-analysis",
    categoryLabel: "Research & Analysis",
    relativePath: "prompts/competitive-landscape-analysis.md",
    sourceBlobSha: "aa90c33efe669cd65442b14fe9c6df4262a65f26",
    summary: "Map competitors and substitutes using comparable evidence without inventing traction, strategy, or market certainty."
  },
  {
    id: "VP-P-RES-004",
    name: "Challenge a Conclusion",
    type: "Prompt",
    category: "research-analysis",
    categoryLabel: "Research & Analysis",
    relativePath: "prompts/challenge-a-conclusion.md",
    sourceBlobSha: "bd49d4a7da8c3a2b538bd51d07fe73ddce0c5f3e",
    summary: "Adversarially test a conclusion for unsupported premises, alternative explanations, and missing decisive evidence."
  },
  {
    id: "VP-P-RES-005",
    name: "Research Decision Brief",
    type: "Prompt",
    category: "research-analysis",
    categoryLabel: "Research & Analysis",
    relativePath: "prompts/research-decision-brief.md",
    sourceBlobSha: "9b0e3e1d7e64b9ac5b44afafc90835d9e1558ee7",
    summary: "Convert research into a concise decision input while preserving tradeoffs, disagreement, and uncertainty."
  },
  {
    id: "VP-P-BIZ-002",
    name: "Design an Operational Process",
    type: "Prompt",
    category: "business-operations",
    categoryLabel: "Business & Operations",
    relativePath: "prompts/design-an-operational-process.md",
    sourceBlobSha: "70fbd9a3571cdd30c2e199ec5294ca2bf6ee29bb",
    summary: "Design a recurring operational process with roles, states, handoffs, exceptions, and verification."
  },
  {
    id: "VP-P-BIZ-003",
    name: "Root-Cause an Operational Failure",
    type: "Prompt",
    category: "business-operations",
    categoryLabel: "Business & Operations",
    relativePath: "prompts/root-cause-an-operational-failure.md",
    sourceBlobSha: "54f0962b71de33ae4e3aa7995b2ffe236b6ef59e",
    summary: "Distinguish symptoms, contributing conditions, and supported causes in recurring operational failures."
  },
  {
    id: "VP-P-BIZ-004",
    name: "Evaluate a Business Decision",
    type: "Prompt",
    category: "business-operations",
    categoryLabel: "Business & Operations",
    relativePath: "prompts/evaluate-a-business-decision.md",
    sourceBlobSha: "cbf60f6cb3d59ed1c55eebae56a9c92d2779c4c9",
    summary: "Evaluate options against hard constraints, explicit criteria, tradeoffs, evidence, and reversibility."
  },
  {
    id: "VP-P-WRITE-002",
    name: "Produce an Executive Brief",
    type: "Prompt",
    category: "writing-communication",
    categoryLabel: "Writing & Communication",
    relativePath: "prompts/produce-an-executive-brief.md",
    sourceBlobSha: "db04de5a31995330bbb104d49b7467372c683904",
    summary: "Compress complex material into a decision-ready executive brief without factual drift or hidden uncertainty."
  },
  {
    id: "VP-P-WRITE-003",
    name: "Adapt One Message Across Audiences",
    type: "Prompt",
    category: "writing-communication",
    categoryLabel: "Writing & Communication",
    relativePath: "prompts/adapt-one-message-across-audiences.md",
    sourceBlobSha: "e26cafc4cea9761fa725ee3fa90c42348fc0acf3",
    summary: "Adapt one factual core across audiences and channels while preserving claims, caveats, and commitments."
  },
  {
    id: "VP-P-WRITE-004",
    name: "Review a Draft for Clarity and Risk",
    type: "Prompt",
    category: "writing-communication",
    categoryLabel: "Writing & Communication",
    relativePath: "prompts/review-a-draft-for-clarity-and-risk.md",
    sourceBlobSha: "c10f8b28997033a4366ba513d3d575f61a0f594c",
    summary: "Review a draft for ambiguity, unsupported certainty, accidental commitments, and material clarity problems."
  },
  {
    id: "VP-P-CONTENT-002",
    name: "Analyze Audience Signals",
    type: "Prompt",
    category: "content-marketing",
    categoryLabel: "Content & Marketing",
    relativePath: "prompts/analyze-audience-signals.md",
    sourceBlobSha: "aa7f440561f1c17800366d715d3b6cabbaa555da",
    summary: "Turn comments, metrics, interviews, and other signals into bounded audience hypotheses and tests."
  },
  {
    id: "VP-P-CONTENT-003",
    name: "Design a Campaign Brief",
    type: "Prompt",
    category: "content-marketing",
    categoryLabel: "Content & Marketing",
    relativePath: "prompts/design-a-campaign-brief.md",
    sourceBlobSha: "5205a8674017125564d68ef12f4fc635435a0c2c",
    summary: "Create a campaign brief grounded in a real offer, audience evidence, channel roles, and claim boundaries."
  },
  {
    id: "VP-P-CONTENT-004",
    name: "Repurpose Source Material Across Channels",
    type: "Prompt",
    category: "content-marketing",
    categoryLabel: "Content & Marketing",
    relativePath: "prompts/repurpose-source-material-across-channels.md",
    sourceBlobSha: "f2df56a4c81aa62495a485206dc664cbde2943f6",
    summary: "Turn one authoritative source into distinct channel-native content without factual drift or duplicate angles."
  },
  {
    id: "VP-P-PLAN-002",
    name: "Prioritize a Portfolio of Work",
    type: "Prompt",
    category: "planning-productivity",
    categoryLabel: "Planning & Productivity",
    relativePath: "prompts/prioritize-a-portfolio-of-work.md",
    sourceBlobSha: "5650eafe7968154e951a6d7dc44c356d0d5ac041",
    summary: "Prioritize competing initiatives using constraints, dependencies, capacity, evidence, and explicit hold/stop states."
  },
  {
    id: "VP-P-PLAN-003",
    name: "Pre-Mortem a Plan",
    type: "Prompt",
    category: "planning-productivity",
    categoryLabel: "Planning & Productivity",
    relativePath: "prompts/pre-mortem-a-plan.md",
    sourceBlobSha: "0a1bfc82637553a1c42890827b3ccd11e2a9ee38",
    summary: "Stress-test a real plan through plausible failure mechanisms, early-warning signals, and preventive controls."
  },
  {
    id: "VP-P-PLAN-004",
    name: "Recover a Stalled Project",
    type: "Prompt",
    category: "planning-productivity",
    categoryLabel: "Planning & Productivity",
    relativePath: "prompts/recover-a-stalled-project.md",
    sourceBlobSha: "4f6ba1723dbf73b5f4c8c7368fafc0dd42134935",
    summary: "Recover a stalled project by isolating blockers, reducing work in progress, and restarting with observable milestones."
  },
  {
    id: "VP-P-CAREER-002",
    name: "Build an Interview Preparation Pack",
    type: "Prompt",
    category: "career-job-search",
    categoryLabel: "Career & Job Search",
    relativePath: "prompts/build-an-interview-preparation-pack.md",
    sourceBlobSha: "5f86582c3510f9b28bfe90fab2216d09c95e5f1b",
    summary: "Build role-specific interview preparation from a real job description and truthful candidate evidence."
  },
  {
    id: "VP-P-CAREER-003",
    name: "Identify Evidence Gaps in a Resume",
    type: "Prompt",
    category: "career-job-search",
    categoryLabel: "Career & Job Search",
    relativePath: "prompts/identify-evidence-gaps-in-a-resume.md",
    sourceBlobSha: "1759f1db8933fe99c74a1eb1c6d785d4502b12cb",
    summary: "Audit resume claims against supporting evidence and target-role requirements without fabricating stronger proof."
  },
  {
    id: "VP-P-CAREER-004",
    name: "Prepare a Career Decision Brief",
    type: "Prompt",
    category: "career-job-search",
    categoryLabel: "Career & Job Search",
    relativePath: "prompts/prepare-a-career-decision-brief.md",
    sourceBlobSha: "2cb3cde886baa1702c3de2d8a80820b92940a7f3",
    summary: "Compare career options against explicit personal criteria, facts, uncertainty, and reversibility."
  },
  {
    id: "VP-WF-001",
    name: "Evidence-first Code Review",
    type: "Workflow",
    category: "development-tech",
    categoryLabel: "Development & Tech",
    relativePath: "workflows/evidence-first-code-review.md",
    sourceBlobSha: "beb62117c24bb7fde552397b89e1e159e294449a",
    summary: "Review a software change for evidence-backed material risks before a human ship decision."
  },
  {
    id: "VP-WF-003",
    name: "Evidence-first Deep Research",
    type: "Workflow",
    category: "research-analysis",
    categoryLabel: "Research & Analysis",
    relativePath: "workflows/evidence-first-deep-research.md",
    sourceBlobSha: "afa65c9cdccff26d6fe92cee800818f3066d4220",
    summary: "Research across multiple sources while enforcing scope, traceability, contradiction handling, and bounded conclusions."
  },
  {
    id: "VP-WF-004",
    name: "Decision Analysis",
    type: "Workflow",
    category: "business-operations",
    categoryLabel: "Business & Operations",
    relativePath: "workflows/decision-analysis.md",
    sourceBlobSha: "1cc57576c91af09054b32d932bb0fe55e42c2bf6",
    summary: "Compare consequential options against explicit constraints, evidence, tradeoffs, and reversal triggers."
  },
  {
    id: "VP-WF-006",
    name: "Master a Topic",
    type: "Workflow",
    category: "study-learning",
    categoryLabel: "Study & Learning",
    relativePath: "workflows/master-a-topic.md",
    sourceBlobSha: "b2d98d24db14b2369d62709a330e95e3e9ec31b4",
    summary: "Move from explanation to retrieval, application, and transfer without falsely marking mastery."
  },
  {
    id: "VP-WF-007",
    name: "Content Strategy System",
    type: "Workflow",
    category: "content-marketing",
    categoryLabel: "Content & Marketing",
    relativePath: "workflows/content-strategy-system.md",
    sourceBlobSha: "d7142fce26e6e303028d77f0134212267d2393a5",
    summary: "Build a repeatable content strategy from observed evidence, explicit hypotheses, experiments, and review loops."
  },
  {
    id: "VP-BUILDER-001",
    name: "Prompt Builder",
    type: "Builder",
    category: "builders",
    categoryLabel: "Build Yours",
    relativePath: "builders/prompt-builder.md",
    sourceBlobSha: "9e89741f2802d2d49816acc74abd84a5d3178d9e",
    summary: "Turn a recurring plain-language task into a reusable prompt without requiring prompt-engineering vocabulary."
  },
  {
    id: "VP-BUILDER-002",
    name: "Workflow Builder",
    type: "Builder",
    category: "builders",
    categoryLabel: "Build Yours",
    relativePath: "builders/workflow-builder.md",
    sourceBlobSha: "3a479f0cc5411383b813394685b91649a1b603fc",
    summary: "Turn a recurring process into a reusable workflow with stages, decisions, fallback, and verification."
  },
  {
    id: "VP-TK-001",
    name: "Adaptation Guide",
    type: "Toolkit",
    category: "toolkit",
    categoryLabel: "Adapt & Evaluate",
    relativePath: "toolkit/adaptation-guide.md",
    sourceBlobSha: "7d963d4138249e2443ef9ee417a5ce32e09d7f1e",
    summary: "Adapt an existing Verlune asset to your context while preserving its important boundaries."
  },
  {
    id: "VP-TK-002",
    name: "Evaluation Toolkit",
    type: "Toolkit",
    category: "toolkit",
    categoryLabel: "Adapt & Evaluate",
    relativePath: "toolkit/evaluation-toolkit.md",
    sourceBlobSha: "77832d31e0f32b2bd7d281527ecfa8345a10d4c9",
    summary: "Evaluate generated prompts and workflows with explicit checks instead of trusting polished output."
  }
] as const;

export function getPremiumAssetMeta(id: string): PremiumAssetMeta | undefined {
  return PREMIUM_ASSETS.find((asset) => asset.id === id);
}

export const PREMIUM_CATEGORY_ORDER = [
  "builders",
  "development-tech",
  "study-learning",
  "research-analysis",
  "business-operations",
  "writing-communication",
  "content-marketing",
  "planning-productivity",
  "career-job-search",
  "toolkit"
] as const;
