# pq-launch-0 / Post 03 — not observed == unknown

Status: `HOLD_FOR_C5`
Content id: `pq-launch-0-p03-unknown`
Pillar: `evidence-discipline`
Primary CTA: `Developer Starter Pack v1`

## LinkedIn draft

One rule has changed how I want AI to behave in technical work:

**not observed == unknown**

It sounds obvious.

But a lot of AI output quietly crosses that line.

A log wasn't provided, but the answer talks as if it saw the runtime failure.

A dependency version wasn't given, but the explanation assumes one.

A code path wasn't executed, but the response describes its behavior with certainty.

The problem isn't uncertainty.

The problem is hiding uncertainty inside confident prose.

For developer prompts, I increasingly want the output to separate three things:

1. **Observed** — supported directly by the code, logs, requirements, or other evidence provided.
2. **Inferred** — plausible from that evidence, but not directly established.
3. **Unknown** — information that could materially change the answer and has not been observed yet.

That separation is built into the prompts I'm packaging in **Prompt Quarry**.

It also applies to the product itself.

If an artifact has passed static validation, I call it **VALID**.

I don't silently turn that into a claim that its runtime behavior has been demonstrated across every task or provider.

The label should stop where the evidence stops.

The free Developer Starter Pack includes three prompts that use this kind of evidence boundary for Code Review, Bug Diagnosis, and Technical Decisions.

→ Try the Starter Pack on a real task and inspect whether the structure is useful for your workflow.

## Attribution

```text
utm_source=linkedin
utm_medium=organic
utm_campaign=pq-launch-0
utm_content=pq-launch-0-p03-unknown
```

## Claims review

Supported framing:
- `not observed == unknown` is a Prompt Quarry operating rule;
- Starter Pack contains 3 prompts;
- current product labels preserve evidence boundaries;
- static VALID is not presented as runtime behavioral proof.

No behavioral superiority or cross-provider performance claim is made.
