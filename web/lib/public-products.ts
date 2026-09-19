// Safe customer-facing data only. Release and provider identities stay separate.
export const CODE_REVIEW = {
  slug: "code-review",
  name: "Verlune Code Review",
  version: "1.0.0",
  price: 9,
  currency: "USD",
  billingModel: "one-time",
  summary: "An evidence-first AI workflow for reviewing software changes.",
  outcome: "Turn a code change into structured findings you can verify before shipping.",
  contents: [
    "Evidence-first Code Review workflow",
    "Quickstart / START HERE",
    "Operating guidance",
    "Evidence and scope disclosure",
    "Customer license",
    "Product-specific terms",
    "Release information",
    "Integrity manifest",
  ],
  evidenceSummary: {
    packQA: "77/77",
    regression: "4/4 human-review passes",
    model: "Gemini 3.5 Flash",
    workflowBytes: 25295,
    workflowSha256: "6739f9c3a54e77fc94fee1879f963982feaddf62151c791c48adc6a655959977",
  },
  availability: "configuration-controlled",
} as const;

export const FREE_WORKFLOWS = {
  slug: "free",
  name: "Verlune Free Workflows",
  price: 0,
  currency: "USD",
  workflows: [
    { name: "Code Review", summary: "Review a change with evidence-ranked findings, severity, and verification guidance." },
    { name: "Bug Diagnosis", summary: "Separate observations from hypotheses and choose checks that narrow down the cause." },
    { name: "Technical Decision", summary: "Compare constraints, tradeoffs, reversibility, and the evidence behind a decision." },
  ],
} as const;

export const codeReviewPrice = `$${CODE_REVIEW.price}`;
