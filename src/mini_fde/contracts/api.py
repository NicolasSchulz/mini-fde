"""Transport-neutral API boundary schemas; no HTTP handlers are defined here."""

from __future__ import annotations

from typing import Generic, Literal, TypeVar
from uuid import UUID

from pydantic import Field

from mini_fde.contracts.base import CONTRACT_VERSION, ContractModel, NonEmptyString

ItemT = TypeVar("ItemT")


class ProblemDetails(ContractModel):
    """RFC 9457-compatible problem detail with a stable application code."""

    type: NonEmptyString
    title: NonEmptyString
    status: int = Field(ge=400, le=599)
    code: NonEmptyString
    detail: NonEmptyString
    request_id: UUID
    run_id: UUID | None
    retryable: bool
    schema_version: Literal["1.0"] = CONTRACT_VERSION


class PageEnvelope(ContractModel, Generic[ItemT]):
    """Versioned pagination shape reserved for a later transport implementation."""

    items: list[ItemT]
    next_cursor: str | None
    has_more: bool
    request_id: UUID
    schema_version: Literal["1.0"] = CONTRACT_VERSION
