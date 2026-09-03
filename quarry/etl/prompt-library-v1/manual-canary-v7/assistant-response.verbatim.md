## Planning status: READY

### Current state

- The repository contains a draft README.
- Deterministic tests are reported as passing.
- No release tag exists.

### Target state

Produce an inspectable plan for a `v0.1` release without deploying, publishing, or creating a tag.

### Constraints and dependencies

**Hard constraints**

- Advisory work only.
- Do not deploy anything.
- Do not create a release tag.

**Dependency order**

```text
README finalization → release notes → tag proposal
```

**Available resources**

- GitHub repository.
- Existing CI.

### Phased plan

| Phase | Condition | Work | Exit criterion |
|---|---|---|---|
| 1. Finalize README | Draft README exists | Review installation, usage, limitations and project status; resolve incomplete sections | README is complete and ready for human review |
| 2. Prepare release notes | Phase 1 complete | Draft `v0.1` notes using only verified repository changes | Notes are inspectable and contain no unsupported release claims |
| 3. Verify release evidence | Release notes drafted | Confirm deterministic test results and identify any missing checks | Evidence checklist records pass, fail or unknown for every required check |
| 4. Prepare tag proposal | Phases 1–3 complete | Propose the tag name and associated commit without creating it | Tag proposal identifies version, commit and approval requirements |
| 5. Human release gate | Tag proposal complete | Present the plan and remaining unknowns for authorization | Human reviewer approves, rejects or requests changes |

### Critical path

The critical path is:

1. Complete the README.
2. Produce release notes from the finalized documentation.
3. Verify available CI evidence.
4. Prepare the tag proposal.
5. Obtain explicit human authorization.

### Major risks and mitigations

| Risk | Mitigation |
|---|---|
| Draft README produces incomplete release notes | Finalize and review the README first |
| Passing deterministic tests are treated as proof of production readiness | Limit the claim to the supplied test evidence |
| A proposed tag is mistaken for an executed release | Label it explicitly as a proposal and require human approval |
| Missing release requirements remain unnoticed | Use an evidence checklist with explicit `PASS`, `FAIL` and `UNKNOWN` states |

### First actions

1. Inspect the draft README and list incomplete sections.
2. Define the README completion checklist.
3. Locate the existing CI test evidence.
4. Draft release notes only after the README exit criterion is satisfied.

### Validation signals

- README review has no unresolved required sections.
- Release notes preserve only verified changes.
- CI evidence is linked or otherwise inspectable.
- The tag remains uncreated.
- No deployment or publication is claimed.

### Replanning triggers

Replan if deterministic tests stop passing, required README information cannot be established, additional release dependencies appear, or the target changes from planning to actual release execution.
