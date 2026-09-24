# Recover a Stalled Project

Status: `PREMIUM PROMPT CANDIDATE / NOT_FOR_SALE`

Use when a project is not progressing and you need to identify the real blockers, reduce work in progress, and restart with evidence.

## Prompt

```text
PROJECT / OUTCOME
{{project}}

CURRENT STATE
{{current_state}}

WHAT HAS BEEN ATTEMPTED
{{attempts}}

BLOCKERS / OPEN DECISIONS
{{known_blockers}}

DEADLINES / CONSTRAINTS
{{constraints}}

RULES
- Do not assume lack of effort is the cause.
- Separate blocked work, unclear decisions, dependency failures, scope growth, and execution debt.
- Do not invent status, owners, deadlines, or completed work.
- Prefer reducing unresolved dependencies before adding new tasks.
- Preserve sunk work only when it still contributes to the outcome.
- Make stop/kill decisions valid when evidence supports them.

PROCESS
1. Restate outcome and current evidence.
2. Map completed, in-progress, blocked, and obsolete work.
3. Identify the smallest set of blockers preventing forward motion.
4. Close or escalate critical decisions.
5. Reduce scope/work in progress.
6. Define a restart sequence with observable milestones.
7. Set kill/re-plan triggers.

OUTPUT
1. Current-state map.
2. Primary stall causes with evidence.
3. Work to stop, finish, or defer.
4. Decisions to close.
5. Restart sequence.
6. Verification milestones.
7. Re-plan / kill triggers.

VERIFICATION
Do not label a blocker as causal unless removing it would plausibly restore progress based on the supplied project evidence.
```
