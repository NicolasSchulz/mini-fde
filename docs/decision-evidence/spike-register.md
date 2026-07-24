# Managed-service spike register

All rows are Phase 0 validation exit criteria represented by planned
hypotheses. No experiment has run, no API/SDK version has been observed, no
cost has been incurred by this documentation, and no go/no-go decision has
been made. Complete an [evidence record](spike-evidence-template.md) before
changing a row's status. Phase 1 managed implementation cannot begin until
the Phase 0 go decisions are completed.

| Spike | Hypothesis to test | Severity | Evidence fields that must be recorded | Current conclusion | Affected ADRs / risks |
|---|---|---|---|---|---|
| SPK-001 | Agent Runtime can deploy/import a minimal custom LangGraph runnable and use the custom model builder with both pinned baseline models, structured output, thinking level, metadata, safe events, and revision flows. | blocking | API/SDK/package/model versions; `europe-west4`; deploy/invoke command; measurements; artifacts; cost | not run — unresolved | ADR-005, 011–013; R-001, R-011, R-012 |
| SPK-002 | Agent Sessions can create/list/read/delete bounded state, reveal retention/location behavior, reconcile invocation results, and be deleted after terminal reconciliation. | blocking | API/SDK version; deployment/region; session lifecycle command; retained payload inspection; cleanup evidence; cost | not run — unresolved | ADR-006, 007; R-003 |
| SPK-003 | Agent Runtime can enforce min `0`/max `2`; a supported CPU/memory shape passes cold-start, maximum-state, representative latency, and maximum-size/retry budgets without truncation. | blocking | Runtime API version; exact resource settings; test command; latency/token/call measurements; artifacts; cost | not run — unresolved | ADR-005, 019; R-002, R-008, R-026 |
| SPK-004 | EU Agent Search accepts custom embeddings and exact corpus-version filters, and the EU endpoint supports pinned `semantic-ranker-default-004`; ranking limits and 768/1536/3072 quality are measurable. | blocking | Discovery/Ranking API and SDK versions; endpoint; import/query/rank commands; quality/limit/latency data; cost | not run — unresolved | ADR-008, 010; R-004, R-005, R-006 |
| SPK-005 | Standalone Model Armor in `europe-west4` supports input/output inspect and block behavior with known verdict and failure semantics. | blocking | API/SDK/template versions; region; screening command; verdict/failure results; cost | not run — unresolved | ADR-015; R-013, R-014 |
| SPK-006 | Named Firestore databases work through server clients, emulator limitations are known, and database-scoped access permits own/control DB while denying the opposite environment. | blocking | Client/emulator versions; database/region; positive and negative IAM test commands; artifacts; cost | not run — unresolved | ADR-001, 002, 016; R-009, R-010 |
| SPK-007 | A Firebase-hosted origin can make authenticated cross-origin POST/SSE calls longer than 60 seconds with reconnect behavior; Identity blocking, invite claim, and App Check verification work. | blocking | Firebase/Identity/App Check versions; origins/regions; browser test command; framing/reconnect and auth results; cost | not run — unresolved | ADR-003, 004; R-025 |
| SPK-008 | Agent Runtime can call BFF run control over HTTPS using a dedicated identity and exact-audience Google OIDC token, or the defined degraded cancellation mode is accurately recorded. | degrading | Runtime/auth API versions; audience/principal; positive and negative commands; cancellation observations; cost | not run — unresolved | ADR-005; R-027 |
| SPK-009 | The Preview Vertex Gen AI evaluation client works behind its adapter, or a local/static offline fallback is validated without becoming a serving dependency. | degrading | Client/SDK/API versions; location; adapter command; normalized result; cost | not run — unresolved | R-022 |
| SPK-010 | BFF final validation, Model Armor output screening, Firestore commit, and terminal SSE fit the 30-second finalization allocation after a 150-second agent budget. | blocking | Exact component versions; environment; maximum-payload command; stage timings; raw measurements; cost | not run — unresolved | ADR-014; R-026 |

For each row, the evidence record must include the exact API/SDK/package
versions, environment and region, command/test entry point, raw-evidence
location, cost, result, conclusion, and affected ADR/risk.
