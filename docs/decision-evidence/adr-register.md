# ADR register

This is an index of the approved master-plan ADR baseline, not a new set of
managed-service decisions. Every entry below has `pending` evidence unless an
ADR links a completed evidence record. In particular, an `Accepted` source
status must not be read as compatibility proof.

| ADR | Source status | Master-plan baseline | Evidence status | Required evidence / related risks |
|---|---|---|---|---|
| ADR-001 | Accepted | One shared project with namespaced dev/prod | pending | Named-database isolation; R-009 |
| ADR-002 | Accepted | Separate named Firestore dev/prod and shared control databases | pending | SPK-006; R-009, R-010 |
| ADR-003 | Accepted | Firebase SPA calls the Cloud Run BFF directly | pending | SPK-007; R-025 |
| ADR-004 | Accepted | Public-reachable, application-authenticated Cloud Run BFF | pending | Application/auth topology validation; R-025 |
| ADR-005 | Accepted | LangGraph on Agent Runtime | pending | SPK-001; R-001, R-002 |
| ADR-006 | Accepted | Application-level clarification, not native interrupts | pending | Agent/session behavior; R-003 |
| ADR-007 | Accepted | Agent Sessions without Memory Bank | pending | SPK-002; R-003 |
| ADR-008 | Accepted | EU Agent Search, custom embeddings, and pinned ranker | pending | SPK-004; R-004 to R-006 |
| ADR-009 | Accepted | Manual corpus publication only | pending | Operational process evidence |
| ADR-010 | Accepted | No live retrieval fallback or ungrounded generation | pending | Retrieval failure behavior; R-004, R-005 |
| ADR-011 | Accepted | Fixed `gemini-3.1-flash-lite` / `gemini-3.5-flash` routing | pending | SPK-001; R-011, R-012 |
| ADR-012 | Accepted | `ChatGoogleGenerativeAI` custom builder | pending | SPK-001; R-001 |
| ADR-013 | Accepted | Gemini 3 temperature `1.0` | pending | SPK-001 |
| ADR-014 | Accepted | Validated-final-only report release | pending | Deterministic core validation |
| ADR-015 | Accepted | Standalone regional Model Armor | pending | SPK-005; R-013, R-014 |
| ADR-016 | Accepted | Firestore server-only product access | pending | SPK-006; R-009 |
| ADR-017 | Accepted | 30-day retention and self-delete | pending | Lifecycle/deletion validation; R-019 |
| ADR-018 | Accepted | No PITR or scheduled backups | pending | Operational acceptance; R-020 |
| ADR-019 | Accepted | Min `0`/max `2` and health-only continuous synthetic | pending | SPK-003; R-002, R-007, R-008 |
| ADR-020 | Accepted | Terraform plus explicit deployment scripts | pending | Lifecycle/tooling validation |
| ADR-021 | Accepted | GitHub Actions WIF, environment-neutral images, environment-targeted SPA bundles | pending | Release/authentication validation; R-028 |
| ADR-022 | Accepted | No response or semantic cache | pending | Architecture review |
| ADR-023 | Accepted | No VPC/LB/Cloud Armor/IAP/CMEK/VPC-SC/PSC in v1 | pending | Threat/cost review |
| ADR-024 | Accepted | No Binary Authorization in v1 | pending | Supply-chain review; R-023 |
| ADR-025 | Accepted | Reserve quota units when billable processing starts | pending | Control-plane validation; R-010 |
| ADR-026 | Accepted | Billing-budget notification drives a soft production run kill switch | pending | Cost-guard validation; R-007 |

When a pending gate changes a baseline, create a full ADR using the template
instead of editing the decision text in this index.
