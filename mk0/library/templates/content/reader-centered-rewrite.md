# Reader-Centered Rewrite Template

**Artifact type:** template  
**Status:** derived-analysis  
**Source inspiration:** Alpacka AI humanization/editing collection `DURUbidDrA5`

## Template

```text
You are revising a draft for a real reader, not optimizing it for an abstract writing score.

INPUT
Draft: {{draft}}
Audience: {{audience}}
Purpose: {{purpose}}
Voice: {{voice}}
Facts/phrases that must remain accurate: {{constraints}}

TASK
Rewrite the draft so the reading experience is clear, natural and direct.

While rewriting:
- preserve all factual meaning and required terminology;
- remove repetition, generic filler and unnecessary explanation;
- vary rhythm only where it improves readability;
- prefer concrete wording over inflated language;
- make transitions feel earned rather than formulaic;
- do not invent anecdotes, credentials or facts;
- do not intentionally add mistakes.

OUTPUT
1. Revised text
2. Three most important changes
3. Any sentence whose meaning could not be preserved confidently
```

## Variables

- `draft`
- `audience`
- `purpose`
- `voice`
- `constraints`

## Techniques

- audience-definition
- explicit-constraints
- tone-definition
- critique-revision
- self-check

## Provenance

This is a new template generalized from a reader-centered rewriting pattern publicly attributed to the Alpacka Threads collection. It is not a verbatim copy of the source prompt.
