# Verlune v1 Candidate

Status: `NOT_FOR_SALE / FORMAL_RUNTIME + BUILDER MATRIX + HUMAN REVIEW PENDING`

Verlune is a library and toolkit for structured AI work.

> **Use ours. Build yours. Work better with AI.**

This folder contains the v1 customer-product candidate. Public website copy must not promise these assets until the release and human-review gates pass.

## Customer model

- **Free** — useful structured prompts and selected workflows.
- **Premium** — deeper prompts and workflows, Prompt Builder, Workflow Builder, adaptation and evaluation tools.
- **Execution** — users run the assets in their own compatible AI assistants.

## Launch categories

1. Development & Tech
2. Study & Learning
3. Research & Analysis
4. Business & Operations
5. Writing & Communication
6. Content & Marketing
7. Planning & Productivity
8. Career & Job Search

## Current folders

- `free/` — launch-core Free candidate surfaces.
- `premium/` — launch-core Premium candidate surfaces.
- `PRODUCT_MODEL.md` — product definition.
- `LAUNCH_SCOPE_V1.md` — bounded v1 scope.
- `BUILDERS_PRODUCT_SPEC.md` — Builder behavior.
- `RELEASE_GATES.md` — promotion requirements.
- `HUMAN_REVIEW_GATE.md` — final gate before landing redesign.
- `LINEAGE_MAP_V1.json` — existing source lineage.
- `evaluation/BEHAVIORAL_SCREENING_EVIDENCE_2026-09-22.md` — 104 manual behavioral screening observations and their evidence boundary.
- `evaluation/BUILDER_FOLLOW_THROUGH_EVIDENCE_2026-09-22.md` — observed Builder and generated-artifact follow-through evidence.

`CANDIDATE != RELEASED != TESTED != CERTIFIED`.


## Current evidence state

```text
STATIC CORE                         PASS
BEHAVIORAL RUNTIME SCREENING        104 PASS / 0 FAIL / 0 INCONCLUSIVE
FORMAL EXACT-ASSET RUNTIME          FROZEN / EXTERNAL EXECUTION REQUIRED
GENERATED WORKFLOW 2ND INSTANCE     PASS
GENERATED PROMPT 2ND INSTANCE       PASS
BUILDER 32 CATEGORY CASES           FROZEN / EXTERNAL EXECUTION REQUIRED
BUILDER 5 STRESS CASES              FROZEN / EXTERNAL EXECUTION REQUIRED
CROSS-MODEL PORTABILITY             FROZEN / EXTERNAL EXECUTION REQUIRED
HUMAN REVIEW H1-H11                 EXTERNAL REVIEWER REQUIRED
ENTITLEMENT E2E                     BLOCKED / ACCESS LAYER NOT IMPLEMENTED
PUBLIC CLAIM AUDIT                  STATIC PASS / LIVE DEPLOYMENT UNOBSERVED
READY_TO_SELL                       NO
```

The 104 screening observations are deliberately **not** represented as the formal 87-case release matrix until every required execution is bound to the exact frozen customer asset/version.


## Formal execution packets now frozen

- `evaluation/EXACT_ASSET_MANIFEST_2026-09-22.json`
- `evaluation/NON_BUILDER_FORMAL_RUNTIME_PACKET_2026-09-22.json` — exact 87-case runtime packet.
- `evaluation/BUILDER_FORMAL_EXECUTION_PACKET_2026-09-22.json` — 37 scenarios / minimum 38 isolated conversations because repeatability requires two runs.
- `evaluation/PORTABILITY_TEST_PACKET_2026-09-22.json`
- `evaluation/HUMAN_REVIEW_EXECUTION_PACKET_2026-09-22.md`
- `evaluation/ACCESS_COMMERCE_STATIC_AUDIT_2026-09-22.md`
- `evaluation/PUBLIC_CLAIM_STATIC_AUDIT_2026-09-22.md`

The remaining formal runtime/model/human gates require evidence from execution environments that are independent of this project-aware chat. The Premium entitlement E2E is additionally blocked because the new Verlune Premium unlock/session layer does not exist yet.
