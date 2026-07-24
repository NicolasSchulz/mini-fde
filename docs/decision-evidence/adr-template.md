# ADR template

Create one ADR for every consequential decision, replacement, or rejected
baseline arising from a spike. Use a zero-padded ID (`ADR-001`) and keep the
record immutable after acceptance; later changes supersede it with a new ADR.

```markdown
# ADR-NNN: <short decision title>

- **Status:** proposed | accepted | superseded | rejected
- **Evidence status:** pending | validated | invalidated | not-applicable
- **Date:** YYYY-MM-DD
- **Decision owner:** <role>
- **Supersedes / superseded by:** <ADR ID or none>
- **Affected plan baseline:** <master-plan section and/or ADR ID>
- **Related spikes:** <SPK IDs>
- **Related risks:** <R IDs>

## Context

<Decision to make, constraints, and why this record is necessary. State
unknowns explicitly.>

## Decision

<The selected option, scope, and non-goals. A managed-service decision must
remain proposed/pending until linked executable evidence supports it.>

## Alternatives considered

| Alternative | Outcome | Reason |
|---|---|---|
| <option> | accepted / rejected / deferred | <reason> |

## Consequences

<Positive, negative, operational, cost, security, compatibility, and migration
consequences.>

## Evidence and validation

| Evidence record | Result | Version/environment | Raw evidence |
|---|---|---|---|
| <SPK-NNN link> | pending / go / no-go | <exact values> | <repository path or approved external location> |

## Follow-up

<Required implementation, risk, compatibility, resource cleanup, or review
actions.>
```

`accepted` records an architecture decision; `validated` records whether
required evidence supports it. These states are intentionally separate so an
accepted master-plan baseline is never mistaken for a completed compatibility
test.
