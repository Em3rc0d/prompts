# Pattern-Breaking Rewrite Template

**Artifact type:** template  
**Status:** derived-analysis  
**Source inspiration:** Alpacka AI humanization/editing collection `DURUbidDrA5`

## Template

```text
Review the draft for repetitive writing patterns before rewriting it.

Draft: {{draft}}
Audience: {{audience}}
Non-negotiable facts: {{facts}}
Desired tone: {{tone}}

First identify up to five structural patterns that make the draft feel formulaic, such as repeated sentence openings, generic transitions, mirrored paragraph structures, repeated conclusions or unnecessary explanation.

Then rewrite the draft to remove those patterns while preserving its meaning.

Constraints:
- do not introduce new claims;
- keep domain-specific terms accurate;
- do not manufacture informality or errors;
- prefer fewer, stronger transitions to decorative connectors;
- leave a phrase unchanged when rewriting would reduce precision.

Return:
PATTERNS_FOUND
REVISED_TEXT
FACTS_PRESERVED
UNCERTAIN_CHANGES
```

## Techniques

- critique-revision
- explicit-constraints
- pattern analysis
- iterative-refinement
- self-check

## Provenance

Generalizes the publicly described pattern-breaking behavior of the Alpacka prompt family. Wording is original to this repository.
