# MK1 F4 Fixture Provenance

F4 behavioral fixtures are grounded in MK0 without pretending that an MK0 structural exemplar is already a behavioral test.

## Two provenance layers

### Direct case lineage

Each F4 case contains:

```text
provenance.mk0_fixture_ids
```

Use this only if that exact behavioral case is genuinely derived from a specific MK0 fixture.

An empty array is valid. Do not populate it cosmetically.

### Cross-stage architecture/technique derivation

`mk0-derivation-map.json` maps every F4 fixture set to existing MK0 Golden Dataset fixtures that support the architecture/techniques used by the engineered prompt family.

The current map uses:

- a writing/revision exemplar for clear rewrite;
- a critique/self-check exemplar for code review architecture;
- evidence-requirement and comparison exemplars for technical research/decision architecture.

These references are **evidence foundations**, not copied behavioral cases.

## Why this boundary matters

MK0 asks:

```text
What structures and techniques exist in observed prompt evidence?
```

F4 asks:

```text
Does our engineered prompt behave correctly under controlled task fixtures?
```

Those are different questions.

Therefore:

```text
MK0 golden exemplar
        ↓
architecture / technique evidence
        ↓
MK1 engineered prompt
        ↓
MK1-authored behavioral fixture set
        ↓
real runtime execution
        ↓
F4 receipt
```

## Validation

`tools/validate_mk1_fixture_provenance.py` verifies that:

- the declared MK0 Golden Dataset files exist;
- the Golden manifest count matches the actual inventory;
- every F4 fixture set has one derivation mapping;
- every referenced MK0 fixture id exists;
- referenced fixture titles match;
- every technique claimed as inherited is actually present in that MK0 fixture;
- any direct per-case MK0 lineage id also exists.

The validator is part of both the F4 characterization gate and the F4B TESTED-promotion workflow.

## Evidence boundary

MK0 provenance can justify why Prompt Forge selected a pattern or architecture.

It cannot prove that the MK1 prompt behaves well. Only F4 real execution can do that.
