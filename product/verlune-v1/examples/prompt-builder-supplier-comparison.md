# Example — Build a Supplier Comparison Prompt

Status: `ILLUSTRATIVE BUILDER EXAMPLE / NOT RUNTIME EVIDENCE`

This shows the intended customer journey for the Prompt Builder. It is not a recorded model execution.

## User starts with

> I frequently receive quotes from suppliers and want AI to compare them.

## Builder should discover

Material questions only:

- What is being purchased?
- Which criteria matter every time?
- Are any criteria hard requirements?
- What information is normally present in a quote?
- Should AI choose a supplier or support a human decision?
- What should happen when a quote omits critical information?

Assume the user answers:

- industrial supplies;
- cost, delivery time, warranty, payment terms;
- warranty of at least 12 months is mandatory;
- quotes vary in completeness;
- human makes the final choice;
- incomplete quotes should be flagged rather than guessed.

## Expected generated artifact shape

```text
SUPPLIER QUOTE COMPARISON

PURPOSE
Compare supplier quotes consistently and prepare evidence for a human purchasing decision.

PER-RUN INPUTS
- quotes
- item/specification
- quantity
- any project-specific deadline

STABLE RULES
- warranty >= 12 months is a hard requirement
- never invent missing quote terms
- compare all viable suppliers using the same criteria
- final purchase decision remains human

PROCESS
1. Normalize quote information.
2. Flag missing fields.
3. Check hard requirements.
4. Compare viable suppliers on cost, delivery, warranty and payment terms.
5. Identify trade-offs and unknowns.
6. Recommend a next action only when evidence supports it.

OUTPUT
- quote completeness
- hard-constraint status
- comparison table
- missing information
- trade-offs
- recommendation / request-more-information state
- verification checklist
```

## Why this is a Prompt Builder success

The user did not need to know:

- variable templates;
- evidence semantics;
- operating contracts;
- fallback schemas.

The Builder translated ordinary needs into those structures.
