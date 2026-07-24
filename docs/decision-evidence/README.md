# Phase 1 decision and evidence baseline

This directory implements the Phase 1 decision/evidence framework from the
approved implementation plan. It is a reviewable place to record evidence; it
is **not** evidence that any managed service, API, region, SDK, or deployment
has been tested.

## Contents

- [ADR template](adr-template.md) — the required record for consequential
  architecture changes.
- [ADR register](adr-register.md) — index of the 26 master-plan ADRs and
  their evidence gates.
- [Spike evidence template](spike-evidence-template.md) — one record per
  executable managed-service experiment.
- [Spike register](spike-register.md) — Phase 1 managed-service hypotheses
  awaiting execution.
- [Compatibility matrix](compatibility-matrix.md) — evolving/Preview surface
  gates and the consequences of incompatibility.
- [Risk and severity convention](risk-severity.md) — shared interpretation of
  spike outcomes and their relationship to the risk register.
- [Temporary-resource inventory](temporary-resource-inventory.md) — inventory
  and cleanup ownership rules for temporary cloud experiments.

## Current state

All evidence-bearing entries in this directory are `not run` or `unresolved`.
The master plan supplies the proposed/accepted architecture baseline, but this
directory does not convert a baseline into a validated managed-service
decision. A spike can be marked `go` only when its completed evidence record
is linked from the register and contains the required version, environment,
command, result, cost, and raw-evidence references.

## Recording workflow

1. Register a temporary resource before creating it, including cleanup owner
   and expiry.
2. Create a copy of the spike evidence template with the spike ID in its file
   name and run the documented executable experiment.
3. Store raw, non-secret command output or test artifacts at the location
   recorded in that evidence record. Do not store credentials, tokens, user
   content, or service-account keys.
4. Update the spike register, compatibility matrix, affected ADR, risk
   treatment, and temporary-resource inventory with links to the completed
   evidence.
5. If the result is not a go, record the result as-is and open or update an
   ADR for the replacement or explicit blocked state. Never silently select a
   fallback.
6. Delete temporary resources by their expiry, then record the cleanup
   evidence before closing the inventory item.

The plan remains the source of truth for architecture intent. A completed
evidence record is the source of truth for a spike result.
