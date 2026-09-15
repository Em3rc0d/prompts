# pq-launch-0 / Post 02 — Code review before / after

Status: `HOLD_FOR_C5`
Content id: `pq-launch-0-p02-code-review`
Pillar: `before-after`
Primary CTA: `Free Code Review prompt`

## LinkedIn draft

“Review this code and tell me what’s wrong.”

That is a request.

It is not much of a review contract.

For a technical review, I want the prompt to make several things explicit before the model starts producing findings:

**Context**
What language/framework is this? What is the expected behavior? What constraints matter?

**Priorities**
Correctness, security, operational risk, maintainability — and in what order?

**Evidence boundary**
Which findings are confirmed by the supplied code? Which are likely? Which need more context?

**Finding contract**
For each issue: location → evidence → impact → recommended fix → confidence.

**Failure behavior**
If the evidence does not support a material issue, say so instead of inventing one to complete a checklist.

So the useful difference isn't “make the prompt longer.”

It is making the review criteria and uncertainty visible.

That is the structure behind the Code Review prompt in the free **Prompt Quarry Developer Starter Pack v1**.

I am not claiming this structure automatically outperforms every shorter prompt on every model. That would require separate behavioral evidence.

What I can show is exactly what the structured version asks the model to make explicit.

→ The Code Review prompt is included in the free Starter Pack.

## Attribution

```text
utm_source=linkedin
utm_medium=organic
utm_campaign=pq-launch-0
utm_content=pq-launch-0-p02-code-review
```

## Claims review

Safe comparison:
`The structured version makes context, priorities, evidence state, output contract, and failure behavior explicit.`

Not claimed:
- better model performance;
- fewer bugs in production;
- superior accuracy;
- TESTED / IMPROVED / CERTIFIED / PORTABLE.
