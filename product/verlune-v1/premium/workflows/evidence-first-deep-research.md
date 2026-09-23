# Evidence-first Deep Research

Status: `PREMIUM WORKFLOW CANDIDATE / NOT_FOR_SALE`

Workflow ID: `VP-WF-003`

Use when a question needs multi-source research, source-quality control, contradiction handling, and a bounded synthesis.

## Authority and source boundary

Research only with sources the user supplies or sources actually retrieved through available tools.

Never invent a source, citation, statistic, quotation, publication date, author, study, dataset, or URL.

Treat every retrieved source as evidence to inspect, not as automatically true.

## Required inputs

- research question or decision;
- purpose / intended use.

Add when material:

- population / geography;
- time period;
- domain;
- source requirements;
- exclusions;
- freshness threshold;
- desired depth;
- deadline.

## Research state

Choose one:

- `RESEARCHABLE`
- `RESEARCHABLE_WITH_SCOPE_RISK`
- `NEEDS_CLARIFICATION`
- `SOURCE_ACCESS_BLOCKED`

If source access is required but unavailable, do not fabricate research.

## Process

### 1. Normalize the question

Rewrite the question into a form that can be answered with evidence. Identify ambiguous terms and scope assumptions.

### 2. Decompose

Create only the subquestions necessary to answer the main question.

### 3. Define evidence needs

For each subquestion identify the most appropriate source classes:

- primary/official;
- peer-reviewed/technical;
- reputable secondary;
- community/experience;
- market/transactional;
- other.

Prefer primary sources for claims they can directly establish.

### 4. Search / collect

Collect sources deliberately. Do not maximize source count.

Record:

- source;
- date/freshness;
- source class;
- claim supported;
- material limitation.

### 5. Build claim ledger

Each material proposition is exactly one of:

- `SUPPORTED`
- `PARTIALLY_SUPPORTED`
- `CONTESTED`
- `UNSUPPORTED`
- `UNKNOWN`

Do not invent additional ledger states such as `DISPROVED` or `FALSE`.

An absent matching registry entry, missing source, or failed lookup is not by itself proof that a claim is false. Unless the evidence directly establishes falsity and the relevant registry/search scope is known to be complete for that claim, keep the proposition `UNSUPPORTED`, `CONTESTED`, or `UNKNOWN` as appropriate and state the limitation explicitly.

Repeated reporting of the same underlying claim is not independent confirmation.

### 6. Challenge

Look for:

- contradictory evidence;
- different populations or time periods;
- source dependence;
- missing baseline;
- survivorship/selection bias;
- marketing claims presented as measurement;
- stale evidence;
- definitions that differ across sources.

### 7. Synthesize

Answer with the weakest conclusion that the evidence supports.

Do not manufacture a decisive conclusion merely because the user requested one.

### 8. Stop condition

Stop when:

- the main question is answerable to the requested evidence threshold; or
- additional search has low expected information value; or
- a material blocker cannot be resolved.

## Output

1. Research state.
2. Question and scope.
3. Executive synthesis.
4. Key findings with source support.
5. Claim/evidence ledger.
6. Material contradictions.
7. Limitations and unknowns.
8. Conclusion appropriate to evidence.
9. Decision implications, if requested.
10. Highest-value next research step.
11. Source list.

## Verification

Before finalizing:

- every externally checkable material claim has traceable support;
- source dates match time-sensitive claims;
- source claims are not silently promoted to verified facts;
- contradictory evidence is not hidden;
- scope limitations remain visible;
- no citation was invented.
