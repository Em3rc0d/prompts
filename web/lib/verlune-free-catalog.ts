export type FreeAssetType = "Prompt" | "Workflow";

export type FreeAssetMeta = {
  id: string;
  name: string;
  type: FreeAssetType;
  category: string;
  categoryLabel: string;
  relativePath: string;
  sourceBlobSha: string;
  summary: string;
};

export const FREE_ASSETS: readonly FreeAssetMeta[] = [
  {
    id: "VF-P-DEV-001",
    name: "Explain Code Clearly",
    type: "Prompt",
    category: "development-tech",
    categoryLabel: "Development & Tech",
    relativePath: "prompts/explain-code-clearly.md",
    sourceBlobSha: "19b6eed105f9680fd567c7fb5fe5a6f8a51fc74d",
    summary: "Understand what code does, how its important parts work together, and what to notice."
  },
  {
    id: "VF-P-STUDY-001",
    name: "Learn a Difficult Topic",
    type: "Prompt",
    category: "study-learning",
    categoryLabel: "Study & Learning",
    relativePath: "prompts/learn-a-difficult-topic.md",
    sourceBlobSha: "09486bc7800f22df95ab5f3c407c4787afbc8848",
    summary: "Learn a topic from your current level and test whether you can explain it back."
  },
  {
    id: "VF-P-RES-001",
    name: "Research a Topic",
    type: "Prompt",
    category: "research-analysis",
    categoryLabel: "Research & Analysis",
    relativePath: "prompts/research-a-topic.md",
    sourceBlobSha: "5f1d47194825385c3ef0188648954e92fa41db5c",
    summary: "Research a bounded question with explicit source requirements, dates, and uncertainty."
  },
  {
    id: "VF-P-BIZ-001",
    name: "Analyze a Business Problem",
    type: "Prompt",
    category: "business-operations",
    categoryLabel: "Business & Operations",
    relativePath: "prompts/analyze-a-business-problem.md",
    sourceBlobSha: "4151af09710f32fb2661d77598a57ae3a14e05f6",
    summary: "Separate business observations from assumptions before choosing an action."
  },
  {
    id: "VF-P-WRITE-001",
    name: "Improve Writing",
    type: "Prompt",
    category: "writing-communication",
    categoryLabel: "Writing & Communication",
    relativePath: "prompts/improve-writing.md",
    sourceBlobSha: "c81edeb65c8e395138c2946605323b19df6e7ece",
    summary: "Make an existing draft clearer without changing its factual meaning."
  },
  {
    id: "VF-P-CONTENT-001",
    name: "Improve a Content Draft",
    type: "Prompt",
    category: "content-marketing",
    categoryLabel: "Content & Marketing",
    relativePath: "prompts/improve-a-content-draft.md",
    sourceBlobSha: "9a2015048dc36c08c251b707d73f134153990103",
    summary: "Improve content for a real audience without manufacturing authority or hype."
  },
  {
    id: "VF-P-PLAN-001",
    name: "Plan a Project",
    type: "Prompt",
    category: "planning-productivity",
    categoryLabel: "Planning & Productivity",
    relativePath: "prompts/plan-a-project.md",
    sourceBlobSha: "ea6cbbbd176d929c07f49c1ce5d65c8c63305a11",
    summary: "Turn an outcome into a realistic path with dependencies, unknowns, and verifiable milestones."
  },
  {
    id: "VF-P-CAREER-001",
    name: "Prepare for an Interview",
    type: "Prompt",
    category: "career-job-search",
    categoryLabel: "Career & Job Search",
    relativePath: "prompts/prepare-for-an-interview.md",
    sourceBlobSha: "b58dcd6c130f45c83b7e8c323e97160cfbe5d510",
    summary: "Prepare for a real role using only experience and evidence you actually have."
  },
  {
    id: "VF-WF-001",
    name: "Compare Options",
    type: "Workflow",
    category: "business-operations",
    categoryLabel: "Business, Research & Planning",
    relativePath: "workflows/compare-options.md",
    sourceBlobSha: "09036b5521e82c6422f7afa41c2359a91025e7c8",
    summary: "Compare alternatives against hard constraints, evidence, tradeoffs, and reversibility."
  },
  {
    id: "VF-WF-002",
    name: "Guided Study Session",
    type: "Workflow",
    category: "study-learning",
    categoryLabel: "Study & Learning",
    relativePath: "workflows/guided-study-session.md",
    sourceBlobSha: "f0c07bd11550514dc5d04d38089fdc6ea3136219",
    summary: "Run a study session that adapts to what you can actually retrieve and apply."
  },
  {
    id: "VF-WF-003",
    name: "Evidence-first Bug Diagnosis",
    type: "Workflow",
    category: "development-tech",
    categoryLabel: "Development & Tech",
    relativePath: "workflows/bug-diagnosis.md",
    sourceBlobSha: "47418dec37f63cea58e083ccd4e3f3e42bb944d3",
    summary: "Diagnose defects from supplied evidence without collapsing observations and hypotheses."
  }
] as const;

export function getFreeAssetMeta(id: string): FreeAssetMeta | undefined {
  return FREE_ASSETS.find((asset) => asset.id === id);
}
