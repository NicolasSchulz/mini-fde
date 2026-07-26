"""Canonical report contracts and provenance records."""

from __future__ import annotations

from datetime import date
from typing import Annotated, Literal
from uuid import UUID

from pydantic import AnyHttpUrl, ConfigDict, Field, field_validator, model_validator

from mini_fde.contracts.base import (
    CONTRACT_VERSION,
    ContractModel,
    NonEmptyString,
    Sha256,
    SourceId,
    UtcDatetime,
)


class ModelCallRecord(ContractModel):
    model_id: NonEmptyString
    resolved_model_version: NonEmptyString
    prompt_version: NonEmptyString
    input_tokens: int = Field(ge=0)
    output_tokens: int = Field(ge=0)
    duration_ms: int = Field(ge=0)
    finish_reason: NonEmptyString
    error_category: str | None


class Source(ContractModel):
    source_id: SourceId
    title: NonEmptyString
    canonical_url: AnyHttpUrl
    official_domain: AnnotatedDomain
    document_type: Literal[
        "product_documentation",
        "architecture_center",
        "security_guidance",
        "operations_guidance",
        "pricing",
        "lifecycle_notice",
    ]
    product_tags: list[NonEmptyString]
    section_path: list[NonEmptyString]
    retrieved_chunk_ids: list[NonEmptyString]
    source_updated_at: UtcDatetime | None
    crawled_at: UtcDatetime
    corpus_version: NonEmptyString
    content_hash: Sha256

    @model_validator(mode="after")
    def canonical_url_is_official(self) -> Source:
        host = self.canonical_url.host
        if host is None or not (
            host == self.official_domain or host.endswith(f".{self.official_domain}")
        ):
            msg = "canonical_url host must match official_domain"
            raise ValueError(msg)
        if self.canonical_url.scheme != "https":
            msg = "canonical_url must use HTTPS"
            raise ValueError(msg)
        return self


AnnotatedDomain = Annotated[
    str,
    Field(pattern=r"^[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?(?:\.[a-z0-9-]+)+$"),
]


class Claim(ContractModel):
    model_config = ConfigDict(
        json_schema_extra={
            "x-contract-version": CONTRACT_VERSION,
            "allOf": [
                {
                    "if": {
                        "properties": {
                            "kind": {"const": "factual"},
                            "support": {"const": "direct"},
                        },
                        "required": ["kind", "support"],
                    },
                    "then": {"properties": {"citation_source_ids": {"minItems": 1}}},
                }
            ],
        }
    )

    claim_id: NonEmptyString
    text: NonEmptyString
    kind: Literal["factual", "recommendation", "assumption", "limitation"]
    citation_source_ids: list[SourceId]
    support: Literal["direct", "synthesized", "assumed", "unsupported"]

    @model_validator(mode="after")
    def direct_factual_claim_requires_citation(self) -> Claim:
        if self.kind == "factual" and self.support == "direct" and not self.citation_source_ids:
            msg = "direct factual claims require at least one citation_source_id"
            raise ValueError(msg)
        return self


class Requirement(ContractModel):
    requirement_id: NonEmptyString
    category: Literal[
        "business",
        "functional",
        "security",
        "privacy",
        "reliability",
        "performance",
        "cost",
        "operations",
        "data",
        "integration",
    ]
    statement: NonEmptyString
    priority: Literal["must", "should", "could"]
    source: Literal["user", "clarification", "derived"]
    evidence_needed: bool


class Assumption(ContractModel):
    assumption_id: NonEmptyString
    statement: NonEmptyString
    impact_if_wrong: NonEmptyString
    validation_action: NonEmptyString
    confidence: Literal["low", "medium", "high"]


class ServiceRecommendation(ContractModel):
    service_id: NonEmptyString
    service_name: NonEmptyString
    role: NonEmptyString
    location: NonEmptyString
    data_handled: NonEmptyString
    configuration: list[NonEmptyString]
    scaling_and_cost_posture: NonEmptyString
    security_controls: list[NonEmptyString]
    rationale: NonEmptyString
    alternatives_rejected: list[NonEmptyString]
    claim_ids: list[NonEmptyString]


class Diagram(ContractModel):
    diagram_id: NonEmptyString
    kind: Literal["flowchart"]
    mermaid_version: NonEmptyString
    source: NonEmptyString
    text_description: NonEmptyString
    validation_status: Literal["valid"]
    source_hash: Sha256


class Risk(ContractModel):
    risk_id: NonEmptyString
    description: NonEmptyString
    likelihood: Literal["low", "medium", "high"]
    impact: Literal["low", "medium", "high", "critical"]
    mitigation: NonEmptyString
    trigger: NonEmptyString
    owner_role: NonEmptyString
    residual_risk: NonEmptyString


class Alternative(ContractModel):
    alternative_id: NonEmptyString
    option: NonEmptyString
    advantages: list[NonEmptyString]
    disadvantages: list[NonEmptyString]
    rejection_reason: NonEmptyString
    reconsider_when: NonEmptyString


class ImplementationPhase(ContractModel):
    phase_id: NonEmptyString
    name: NonEmptyString
    objective: NonEmptyString
    dependencies: list[NonEmptyString]
    tasks: list[NonEmptyString]
    exit_criteria: list[NonEmptyString]


class Confidence(ContractModel):
    overall: Literal["low", "medium", "high"]
    evidence_coverage_score: float = Field(ge=0, le=1)
    requirement_coverage_score: float = Field(ge=0, le=1)
    unresolved_assumption_count: int = Field(ge=0)
    limitations: list[NonEmptyString]


class VerifierSummary(ContractModel):
    outcome: Literal["passed", "failed", "repaired"]
    finding_count: int = Field(ge=0)
    verifier_version: NonEmptyString


class ValidationSummary(ContractModel):
    outcome: Literal["passed"]
    validator_version: NonEmptyString
    report_sha256: Sha256


class CanonicalReport(ContractModel):
    """The immutable, versioned document from which all renderings derive."""

    schema_version: Literal["1.0"] = CONTRACT_VERSION
    rendering_contract_version: Literal["1.0"] = CONTRACT_VERSION
    report_id: UUID
    report_version_id: UUID
    conversation_id: UUID
    run_id: UUID
    version: int = Field(ge=1, le=4)
    title: NonEmptyString
    generated_at: UtcDatetime
    design_as_of_date: date
    corpus_version: NonEmptyString
    graph_version: NonEmptyString
    prompt_bundle_version: NonEmptyString
    model_config_version: NonEmptyString
    model_records: list[ModelCallRecord]
    executive_summary: list[NonEmptyString] = Field(min_length=1)
    problem_framing: NonEmptyString
    assumptions: list[Assumption]
    open_questions: list[NonEmptyString]
    requirements: list[Requirement] = Field(min_length=1)
    recommended_architecture: NonEmptyString
    services: list[ServiceRecommendation] = Field(min_length=1)
    diagram: Diagram
    data_flow: list[NonEmptyString] = Field(min_length=1)
    security_and_privacy: list[NonEmptyString] = Field(min_length=1)
    reliability_and_operations: list[NonEmptyString] = Field(min_length=1)
    cost_drivers: list[NonEmptyString] = Field(min_length=1)
    pricing_links: list[AnyHttpUrl]
    risks: list[Risk]
    alternatives: list[Alternative]
    implementation_phases: list[ImplementationPhase] = Field(min_length=1)
    confidence: Confidence
    claims: list[Claim] = Field(min_length=1)
    sources: list[Source] = Field(min_length=1)
    verifier_summary: VerifierSummary
    validation_summary: ValidationSummary

    @field_validator("pricing_links")
    @classmethod
    def pricing_links_are_https(cls, value: list[AnyHttpUrl]) -> list[AnyHttpUrl]:
        if any(link.scheme != "https" for link in value):
            msg = "pricing_links must use HTTPS"
            raise ValueError(msg)
        return value

    @model_validator(mode="after")
    def references_are_resolvable(self) -> CanonicalReport:
        source_ids = [source.source_id for source in self.sources]
        claim_ids = [claim.claim_id for claim in self.claims]
        requirement_ids = [requirement.requirement_id for requirement in self.requirements]
        if len(source_ids) != len(set(source_ids)):
            msg = "source_id values must be unique"
            raise ValueError(msg)
        if len(claim_ids) != len(set(claim_ids)):
            msg = "claim_id values must be unique"
            raise ValueError(msg)
        if len(requirement_ids) != len(set(requirement_ids)):
            msg = "requirement_id values must be unique"
            raise ValueError(msg)
        known_sources = set(source_ids)
        unknown_citations = {
            source_id for claim in self.claims for source_id in claim.citation_source_ids
        } - known_sources
        if unknown_citations:
            msg = "claim citations must resolve to report sources"
            raise ValueError(msg)
        if any(claim.support == "unsupported" for claim in self.claims):
            msg = "completed reports cannot include unsupported claims"
            raise ValueError(msg)
        known_claims = set(claim_ids)
        if {claim_id for service in self.services for claim_id in service.claim_ids} - known_claims:
            msg = "service claim_ids must resolve to report claims"
            raise ValueError(msg)
        if any(source.corpus_version != self.corpus_version for source in self.sources):
            msg = "sources must use the report corpus_version"
            raise ValueError(msg)
        return self
