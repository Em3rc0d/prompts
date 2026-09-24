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

Treat supplied population, geography, time period, source requirements, exclusions, and freshness thresholds as evidence-scope constraints, not decorative context.

A source outside the requested evidence scope may be used only as clearly labeled background when it materially helps interpretation. Do not use it as direct support for an in-scope conclusion unless the user explicitly allows the scope to expand.

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

For every source used to support a material claim, record:

- traceable source identity or locator;
- date/freshness;
- source class;
- population / setting when material;
- claim supported;
- material limitation;
- whether it is inside the requested evidence scope.

Do not write vague support such as "other studies confirm" or "recent meta-analyses show" without identifying the actual source.

Do not generalize evidence from a mixed or different population to the requested target population as if it were direct evidence. Label it as indirect or broader-context evidence unless the target subgroup is actually established.

### 5. Build claim ledger

Each material proposition is exactly one of:

- `SUPPORTED`
- `PARTIALLY_SUPPORTED`
- `CONTESTED`
- `UNSUPPORTED`
- `UNKNOWN`

Do not invent additional ledger states such as `DISPROVED` or `FALSE`.

An absent matching registry entry, missing source, or failed lookup is not by itself proof that a claim is false. Unless the evidence directly establishes falsity and the relevant registry/search scope is known to be complete for that claim, keep the proposition `UNSUPPORTED`, `CONTESTED`, or `UNKNOWN` as appropriate and state the limitation explicitly.

Likewise, do not describe a missing registry match as a direct contradiction of the underlying certification claim unless registry completeness, identifier matching, and search scope make that inference defensible. Otherwise describe it as an unresolved verification gap or evidentiary tension.

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
- every source cited in the answer appears in the source list or ledger with enough identity to trace it;
- source dates and populations fit the requested evidence scope, or any out-of-scope use is clearly labeled as background/indirect evidence;
- no vague unnamed source class is used as proof for a material claim;
- source claims are not silently promoted to verified facts;
- contradictory evidence is not hidden;
- scope limitations remain visible;
- no citation was invented.
