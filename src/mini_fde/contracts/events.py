"""Safe public SSE event contracts without private workflow content."""

from __future__ import annotations

from typing import Annotated, Literal
from uuid import UUID

from pydantic import Field, TypeAdapter

from mini_fde.contracts.base import CONTRACT_VERSION, ContractModel, NonEmptyString, UtcDatetime
from mini_fde.contracts.workflow import ReportReference


class EventBase(ContractModel):
    schema_version: Literal["1.0"] = CONTRACT_VERSION
    event_id: UUID
    run_id: UUID
    emitted_at: UtcDatetime


class RunAcceptedEvent(EventBase):
    event: Literal["run.accepted"]
    phase: Literal["accepted"]


class PhaseStartedEvent(EventBase):
    event: Literal["phase.started"]
    phase: Literal[
        "understanding", "retrieving", "assessing", "designing", "verifying", "finalizing"
    ]


class PhaseCompletedEvent(EventBase):
    event: Literal["phase.completed"]
    phase: Literal[
        "understanding", "retrieving", "assessing", "designing", "verifying", "finalizing"
    ]


class ClarificationRequiredEvent(EventBase):
    event: Literal["clarification.required"]
    question_ids: list[NonEmptyString] = Field(min_length=1, max_length=3)


class RunCompletedEvent(EventBase):
    event: Literal["run.completed"]
    report_ref: ReportReference
    model_calls_used: int = Field(ge=0)
    input_tokens_used: int = Field(ge=0)
    output_tokens_used: int = Field(ge=0)


class RunFailedEvent(EventBase):
    event: Literal["run.failed"]
    outcome: Literal["failed", "cancelled", "timed_out"]
    code: NonEmptyString
    retryable: bool


PublicEvent = Annotated[
    RunAcceptedEvent
    | PhaseStartedEvent
    | PhaseCompletedEvent
    | ClarificationRequiredEvent
    | RunCompletedEvent
    | RunFailedEvent,
    Field(discriminator="event"),
]
PUBLIC_EVENT_ADAPTER: TypeAdapter[PublicEvent] = TypeAdapter(PublicEvent)
