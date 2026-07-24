# Temporary-resource inventory and cleanup ownership

Temporary resources exist only to execute approved spikes. They are not a
Phase 2 foundation, and an experiment is not complete until its resources are
deleted or explicitly handed over through an approved record.

## Current inventory

No temporary cloud resources have been created by this documentation baseline.
Register a resource before creating it; do not replace this empty state with
an inferred or console-only experiment.

| Inventory ID | Resource | Environment / region | Created | Expiry | Cleanup owner | Related spike | Status | Cleanup evidence |
| ------------ | -------- | -------------------- | ------- | ------ | ------------- | ------------- | ------ | ---------------- |
| _No entries_ | —        | —                    | —       | —      | —             | —             | empty  | —                |

## Registration and cleanup convention

For every temporary resource, add a row with all fields below before creation:

| Field                | Required value                                                                           |
| -------------------- | ---------------------------------------------------------------------------------------- |
| Inventory ID         | Stable `TMP-NNN` identifier.                                                             |
| Resource             | Resource type and non-secret resource identifier.                                        |
| Environment / region | Exact project environment and region/multi-region.                                       |
| Created              | ISO-8601 timestamp and creator role.                                                     |
| Expiry               | ISO-8601 timestamp selected before creation; no resource may have an unspecified expiry. |
| Cleanup owner        | A named accountable role or individual responsible for deletion and evidence.            |
| Related spike        | One or more `SPK-NNN` IDs and the evidence record path.                                  |
| Status               | `registered`, `created`, `cleanup-due`, `deleted`, or `handed-over`.                     |
| Cleanup evidence     | Safe deletion command/test reference, timestamp, and raw artifact location.              |

The cleanup owner must delete the resource by expiry, update the row to
`deleted`, and link evidence that it no longer exists. If retention is
necessary for later work, the owner must record a new expiry, receiving owner,
reason, and approved Phase 2 handover before the original expiry. `handed-over`
does not waive cleanup ownership; it transfers it explicitly.

No entry may contain credentials, access tokens, private endpoints, user
content, or service-account keys. Billing cost belongs in the related spike
evidence record, not in a secret-bearing console export.
