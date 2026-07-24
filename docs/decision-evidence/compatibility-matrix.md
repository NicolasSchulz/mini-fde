# Managed-service compatibility matrix

This matrix lists the Phase 0 validation exit criteria that must be answered
by executable evidence. `Unresolved` means no compatibility assertion has
been made; it does not imply the intended baseline is supported. Phase 1
managed implementation cannot begin until the Phase 0 go decisions are
completed.

| Surface | Intended baseline under evaluation | Compatibility evidence required | Evidence record | Status | Severity if incompatible | Required response |
|---|---|---|---|---|---|---|
| Agent Runtime | Custom LangGraph runnable in `europe-west4` with revision and bounded-scale behavior | Package serialization/import, invoke, safe event stream, revision lifecycle, min/max settings, resource-shape measurements | SPK-001, SPK-003 | unresolved | blocking | Update ADR-005/019 with a supported replacement or block production. |
| Agent Sessions | Temporary reconciliation state, not a LangGraph checkpointer | Create/list/read/delete, retained payload, location/retention, invocation-result reconciliation, explicit deletion | SPK-002 | unresolved | blocking | Record restart-only recovery or replacement in an ADR; do not retain undeletable sessions. |
| Agent Search / Discovery Engine | EU custom vectors with exact `corpus_version` filter | Custom import, `RETRIEVAL_DOCUMENT`/`RETRIEVAL_QUERY`, filter semantics, index readiness | SPK-004 | unresolved | blocking | Revisit retrieval architecture through ADR; do not use a global or opaque fallback silently. |
| Google Ranking API | EU endpoint and pinned `semantic-ranker-default-004` | Location/model availability, record token/truncation behavior, quality/latency comparison | SPK-004 | unresolved | blocking | Select and evaluate a pinned replacement through ADR; never use `@latest`. |
| Model Armor | Standalone `europe-west4` input/output screening | Inspect/block verdict shape and timeout/failure semantics | SPK-005 | unresolved | blocking | Update ADR-015 before production; do not claim a fail-closed posture without evidence. |
| Vertex Gen AI evaluation client | Preview client behind offline `EvaluationProvider` | Client invocation, normalized result schema, local/static fallback | SPK-009 | unresolved | degrading | Keep evaluation offline and use the validated fallback; record the adapter decision. |
| Named Firestore databases | `mini-fde-dev`, `mini-fde-prod`, and control DB with database-scoped access | Server-client access, emulator behavior, positive own/control access, negative cross-environment access | SPK-006 | unresolved | blocking | Change the one-project/resource model through ADR before product data is used. |
| Firebase/Identity blocking functions | Shared invitation gate and invited claim | `beforeCreate` block, invite lookup, claim refresh, App Check token verification | SPK-007 | unresolved | blocking | Define a replacement access-control design through ADR before enabling sign-up. |
| Browser streaming topology | Direct Firebase-origin cross-origin BFF POST/SSE | Authenticated stream over 60 seconds, framing, reconnect behavior | SPK-007 | unresolved | blocking | Change topology through ADR; do not use a 60-second Hosting rewrite for proposal runs. |
| Agent outbound OIDC run control | Dedicated agent identity and exact BFF audience | HTTPS reachability, positive token path, wrong audience/principal rejection, cancellation observation | SPK-008 | unresolved | degrading | Record the explicit degraded cancellation mode; final transaction remains cancellation-aware. |

When a row reaches a conclusion, link its completed evidence record and update
the ADR register and risk treatment in the same change.
