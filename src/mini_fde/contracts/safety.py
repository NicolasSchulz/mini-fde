"""Local safety boundary contracts with no managed-service dependency."""

from __future__ import annotations

from typing import Literal

from pydantic import Field

from mini_fde.contracts.base import CONTRACT_VERSION, ContractModel, NonEmptyString


class SafetyFinding(ContractModel):
    category: NonEmptyString
    confidence: Literal["low", "medium", "high"]
    action: Literal["allow", "block", "review"]


class SafetyVerdict(ContractModel):
    schema_version: Literal["1.0"] = CONTRACT_VERSION
    template_version: NonEmptyString
    direction: Literal["input", "output"]
    outcome: Literal["allowed", "blocked", "unavailable"]
    findings: list[SafetyFinding]
    latency_ms: int = Field(ge=0)
