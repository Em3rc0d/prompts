---
name: design-ai-workflows
description: Turn a recurring AI-assisted technical task into an explicit operating contract with input, evidence, authority, decision, output, verification, and fallback semantics. Use when designing or standardizing an AI workflow, not when directly reviewing code, debugging, or choosing a technical option.
---

# AI Workflow Contract Designer

State: `STRUCTURAL_CANDIDATE / UNTESTED`  
Skill ID: `PQ-SKILL-0004`  
Workflow: `PQ-WF-0004`  
Prompt lineage: `PQ-PROMPT-0005` with v1.2 successor `product/developer-workflow-kit-v1.2/prompts/general-operating-contract-v1.2.md`

## Required intake

Identify the recurring task, consumer, primary outcome, required inputs, allowed context, authority boundary, decision states, and integration surface. Ask only for missing information that can materially change the contract.

## Workflow

1. Define workflow identity and outcome.
2. Separate required, optional, and forbidden inputs/context.
3. Define evidence labels and the strongest conclusion each evidence state permits.
4. Define `MUST`, `MUST NOT`, and `PRESERVE` invariants.
5. Define the minimal execution process required for repeatability.
6. Define stable decision/escalation states.
7. Define an output contract that the actual consumer can inspect or parse.
8. Define verification and fallback behavior.
9. Check that representation changes do not weaken semantics.

## Blocked behavior

If required information is missing, do not design a completed workflow. Return `BLOCKED`, preserve only safe partial evidence already established, and list the smallest information set needed to continue. A partial domain conclusion is not allowed in `BLOCKED` state.

## Output

Return:

- `Workflow identity`
- `Input/context contract`
- `Evidence policy`
- `Operating constraints`
- `Execution process`
- `Decision states`
- `Output contract`
- `Verification contract`
- `Fallback contract`
- `Adaptation/integration map`

## Boundaries

Do not claim that the resulting workflow is tested, improved, certified, portable, or production-ready without matching receipts. Do not silently expand the workflow's authority beyond what the user supplied.
