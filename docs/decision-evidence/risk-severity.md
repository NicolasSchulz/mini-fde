# Risk and spike severity convention

## Spike outcome severity

| Severity        | Meaning                                                                      | Required handling                                                                                                                           |
| --------------- | ---------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------- |
| `blocking`      | The architecture cannot proceed without a resolved replacement.              | Keep the compatibility gate unresolved, record a no-go if applicable, update/create an ADR, and block dependent production work.            |
| `degrading`     | The baseline remains safe, but a feature or operational behavior is reduced. | Record the degraded behavior in run/release documentation, update the affected risk and ADR, and do not represent the feature as available. |
| `informational` | The result is tuning input only.                                             | Record the measurement and any resulting configuration rationale; it does not gate architecture progression.                                |

Severity describes the consequence of an unresolved or failed spike. It is not
a likelihood score, an impact score, a production incident severity, or a
claim that the spike has passed.

## Relationship to the risk register

Use the master-plan `R-NNN` identifiers in ADRs and spike evidence. Preserve
their likelihood, impact, mitigation, trigger, and owner until a reviewed
update is made. Each new or changed spike record must state:

1. affected risk IDs;
2. whether the evidence changes the risk likelihood, impact, mitigation, or
   trigger;
3. the owner responsible for the follow-up; and
4. the ADR that records any architectural change.

Do not close a risk merely because a test command succeeded. A risk can be
closed only when its documented trigger, mitigation, and residual exposure
have been reviewed with the completed evidence.
