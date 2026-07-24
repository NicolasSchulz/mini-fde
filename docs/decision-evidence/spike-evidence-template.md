# Managed-service spike evidence template

Copy this file for each executed spike. A record is incomplete, and therefore
cannot support a go/no-go conclusion, until every required field is populated.
Do not put secrets, credentials, browser tokens, user content, or
service-account keys in the record or raw artifacts.

```markdown
# SPK-NNN: <short hypothesis>

- **Status:** planned | running | completed | blocked
- **Severity if unresolved:** blocking | degrading | informational
- **Owner:** <role>
- **Started / completed:** <ISO-8601 timestamps>
- **Environment:** <project/environment; no credentials>
- **Region / endpoint:** <exact region and endpoint>
- **Managed service / API:** <service and API surface>
- **Exact versions:** <API version, SDK/package versions, model/ranker IDs>
- **Affected ADRs:** <ADR IDs>
- **Affected risks:** <R IDs>
- **Temporary-resource inventory IDs:** <TMP IDs or none>

## Hypothesis and acceptance criteria

<What will be proven or disproven, with measurable pass/fail criteria.>

## Reproducible entry point

- **Repository revision:** <commit SHA>
- **Command or test entry point:** `<exact command>`
- **Inputs / fixtures:** <safe paths and identifiers>
- **Required permissions / preconditions:** <roles or setup; never secrets>

## Result

- **Observed result:** not run | pass | fail | inconclusive
- **Measurements:** <latency, quotas, limits, output shape, etc.>
- **Cost incurred:** <currency/amount, billing source, or explicitly unknown>
- **Raw evidence:** <immutable repository path or approved external artifact>
- **Exceptions / deviations:** <none or details>

## Go/no-go conclusion

<go | no-go | unresolved, with the exact reason. A no-go or unresolved result
must name the affected ADR/risk follow-up and must not silently choose a
fallback.>

## Cleanup and follow-up

<Temporary-resource cleanup evidence, ADR/risk/matrix updates, and next owner.>
```
