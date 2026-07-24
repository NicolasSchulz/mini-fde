# mini-fde
Tiny FDE.

## Decision and evidence baseline

Phase 0 validation decision records, managed-service spike templates,
compatibility gates, and temporary-resource cleanup conventions live in
[`docs/decision-evidence/`](docs/decision-evidence/README.md). They are
documentation only: no cloud resources, managed-service spike results, or
implementation decisions are created by this repository baseline.

The managed-service spike/evidence scaffolding and unresolved spikes are
Phase 0 validation exit criteria. Phase 1 managed implementation cannot begin
until the Phase 0 go decisions are completed.

## Local contract foundation

Provider-neutral Phase 1 contracts live in `src/mini_fde/contracts/`. Regenerate
the committed JSON Schema, OpenAPI component, version manifest, and narrow
TypeScript contract artifact with:

```sh
uv run python scripts/generate_contract_artifacts.py
```

Use `--check` in validation to fail on generated-artifact drift. The OpenAPI
document intentionally has no paths: this phase defines schemas only and does
not implement BFF endpoints.
