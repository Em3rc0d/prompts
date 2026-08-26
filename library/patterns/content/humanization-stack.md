# Humanization Stack Pattern

**Artifact type:** pattern  
**Status:** derived-analysis

## Observation

The Alpacka humanization collection is more useful when treated as a **stack of distinct editorial passes** than as six unrelated prompts.

The generalized stack is:

```text
MEANING LOCK
   ↓
MECHANICAL-PATTERN DETECTION
   ↓
RHYTHM REPAIR
   ↓
VOICE ALIGNMENT
   ↓
READER-CENTERED REWRITE
   ↓
FINAL QUALITY AUDIT
```

## Why the pattern matters

A single instruction such as “make this sound human” mixes several objectives and gives the model no way to expose trade-offs. Splitting the work into passes makes each transformation inspectable and gives the user a chance to preserve facts before stylistic rewriting.

## Pattern contract

### Input

- draft
- immutable facts
- intended audience
- intended voice

### Transformations

1. Preserve factual meaning.
2. Detect formulaic structure.
3. Repair rhythm and repetition.
4. Align voice to audience/context.
5. Optimize reader experience.
6. Audit the final result against the original facts.

### Output

- revised draft
- changes made
- facts preserved
- unresolved ambiguity

## Failure modes

- treating “human” as permission to add errors
- fabricating anecdotes or lived experience
- changing facts for stylistic reasons
- optimizing for detector evasion rather than communication quality
- making every sentence artificially irregular

## Source family

Primary inspiration: https://www.threads.com/@alpacka.ai/post/DURUbidDrA5

The pattern is a repository-level abstraction and does not reproduce the original prompt wording.
