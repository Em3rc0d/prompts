# MK1 — ChatGPT Plus manual-observed execution

ChatGPT Plus is a supported **manual-observed** runtime lane for MK1 evidence collection. It does not require an OpenAI API key.

## Product boundary

ChatGPT subscriptions and OpenAI API billing are separate products. This lane therefore never assumes that a ChatGPT Plus subscription provides `OPENAI_API_KEY` access.

## Evidence semantics

The quality gates do not change:

```text
VALID
  ↓ F4 manual-observed
TESTED
  ↓ F5 manual-observed blind benchmark
CANDIDATE / IMPROVED
  ↓ F6 repeated manual-observed benchmarks on same declared ChatGPT configuration
CERTIFIED
```

`manual-observed` is already a real execution mode in the F4/F5 contracts. It is not synthetic and it is not an exemption from review/evidence requirements.

## Declared runtime identity

For ChatGPT Plus, record only what is actually observable in the UI. Do not invent a hidden backend model id.

Recommended identity:

```text
provider = openai-chatgpt
model    = <exact visible model/configuration label selected in ChatGPT>
family   = chatgpt-plus
```

If the UI exposes only a routing/configuration label such as `Instant`, `Thinking`, or another product label, record that exact visible label. The resulting certification claim is scoped to that declared ChatGPT configuration, not to an unobserved internal API model.

F6 requires the same normalized provider + model/configuration label + family across its independent certification receipts.

## Clean-run protocol

Every observed prompt execution used as evidence must:

1. use a fresh ChatGPT conversation with no task-specific prior context;
2. use the same declared visible ChatGPT model/configuration for the whole benchmark;
3. paste the frozen rendered prompt exactly as prepared by the repository;
4. record the full observed answer without rewriting it;
5. retain an evidence reference for that observation;
6. never reuse an answer between fixtures or repeats;
7. preserve blind A/B identity separation during F5 human review.

A project/chat containing prior Prompt Quarry discussion is not a clean evaluation context unless the fixture explicitly requires that context.

## Observation evidence

Manual observation evidence must be durable enough to audit later. Each raw observation record should bind:

- execution id;
- observation id;
- declared ChatGPT product/runtime identity;
- rendered prompt SHA-256;
- full observed output;
- output SHA-256;
- observed-at timestamp;
- a human-supplied source reference such as an exported transcript path, repository evidence note, or other retained record.

Screenshots may supplement evidence but should not replace text output when text can be preserved directly.

## F4

F4 uses the same behavioral fixtures and human checks as API execution. A real ChatGPT Plus observation may promote `VALID → TESTED` only if the normal F4 runner produces `BEHAVIORAL_PASS`.

## F5

F5 still requires at least three repeats. Candidate and baseline outputs must be presented to the reviewer as randomized `A` / `B` pairs. The blind mapping remains private until review completion.

No baseline win, unresolved blocking human check, regression, or engineered blocking failure is waived for ChatGPT Plus.

## F6

F6 still requires at least three independent real F5 `IMPROVEMENT_PASS` receipts on the same declared ChatGPT Plus runtime identity. Each benchmark also retains its own internal repeats.

Therefore API access is **not** a certification requirement. Reproducible observed evidence is the requirement.

## Automation boundary

`.github/workflows/run-mk1-observed-experiment.yml` remains the automated API lane because it executes provider HTTP APIs and requires provider secrets.

ChatGPT Plus uses a separate manual-observed collection lane. Do not add browser/session scraping, cookie extraction, private ChatGPT endpoints, or other attempts to turn a Plus web session into an unofficial API.
