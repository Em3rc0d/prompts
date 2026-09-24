# Example — Build a Hotel Shift Handoff Workflow

Status: `ILLUSTRATIVE BUILDER EXAMPLE / NOT RUNTIME EVIDENCE`

This deliberately uses a non-technical domain to test whether the Workflow Builder is genuinely general-purpose.

## User starts with

> At the end of every hotel shift, the next team needs to know unresolved guest issues, maintenance problems and important follow-ups.

## Builder should discover

- What starts the handoff?
- What information must always be captured?
- Which issues require escalation?
- Who receives the handoff?
- What should never be guessed?
- What counts as complete?

Assume:

- workflow starts 30 minutes before shift end;
- required fields: issue, room/area when appropriate, observed facts, actions already taken, owner, next action;
- urgent safety/security issues follow existing hotel escalation policy;
- the next shift supervisor consumes the output;
- guest facts and resolution status must never be invented;
- completion means all open items have an owner or explicit escalation state.

## Expected workflow shape

```text
SHIFT HANDOFF WORKFLOW

TRIGGER
30 minutes before shift end.

OUTCOME
Next shift receives a complete, factual list of unresolved operational items with ownership and next actions.

REQUIRED INPUTS
For each open item:
- category
- observed issue
- room/area when appropriate
- actions already taken
- current status
- owner / escalation state
- next action

BOUNDARIES
- do not invent guest statements or resolution status
- do not expose unnecessary sensitive guest information
- follow existing hotel policy for safety/security escalation
- AI organizes and checks the handoff; staff retain operational authority

STAGES
1. Collect open items.
2. Separate observed facts from assumptions.
3. Detect missing owner/next action.
4. Classify status.
5. Escalate according to supplied policy where applicable.
6. Produce handoff.
7. Supervisor verifies before shift transfer.

STATES
READY_FOR_HANDOFF
NEEDS_OWNER
NEEDS_INFORMATION
ESCALATION_REQUIRED

OUTPUT
- concise shift summary
- open-items table
- unresolved missing information
- escalations
- owners
- next actions

VERIFICATION
No open item is marked ready without a current status and owner/escalation state.
```

## Why this matters

A successful result demonstrates that Workflow Builder is not merely a software-engineering template with nouns replaced.
