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
