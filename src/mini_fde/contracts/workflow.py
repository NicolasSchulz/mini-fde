"""Typed local workflow boundaries; these models contain no provider clients."""

from __future__ import annotations

from typing import Annotated, Literal
from uuid import UUID

from pydantic import Field, model_validator

from mini_fde.contracts.base import (
    CONTRACT_VERSION,
    ContractModel,
    NonEmptyString,
    Sha256,
    SourceId,
    UtcDatetime,
)
from mini_fde.contracts.report import CanonicalReport, Requirement
from mini_fde.contracts.safety import SafetyVerdict


class ClarificationQuestion(ContractModel):
    question_id: NonEmptyString
    question: NonEmptyString
    rationale: NonEmptyString


class ClarificationRequest(ContractModel):
    schema_version: Literal["1.0"] = CONTRACT_VERSION
    questions: list[ClarificationQuestion] = Field(min_length=1, max_length=3)


class ClarificationAnswer(ContractModel):
    question_id: NonEmptyString
    answer: NonEmptyString


class GapAnalysis(ContractModel):
    missing_requirement_ids: list[NonEmptyString]
    proposed_questions: list[ClarificationQuestion] = Field(max_length=3)
    clarification_required: bool


class RequirementsSpec(ContractModel):
    schema_version: Literal["1.0"] = CONTRACT_VERSION
    requirements: list[Requirement] = Field(min_length=1)
    assumptions: list[NonEmptyString]
    gap_analysis: GapAnalysis


class RetrievalQuery(ContractModel):
    query_id: NonEmptyString
    query: NonEmptyString
    requirement_ids: list[NonEmptyString] = Field(min_length=1)
    expected_evidence_categories: list[NonEmptyString] = Field(min_length=1)


class RetrievalPlan(ContractModel):
    schema_version: Literal["1.0"] = CONTRACT_VERSION
    corpus_version: NonEmptyString
    attempt: Literal[0, 1]
    queries: list[RetrievalQuery] = Field(min_length=1, max_length=4)


class EvidenceCandidate(ContractModel):
    candidate_id: NonEmptyString
    source_id: SourceId
    chunk_id: NonEmptyString
    corpus_version: NonEmptyString
    score: float = Field(ge=0, le=1)


class EvidenceItem(ContractModel):
    evidence_id: NonEmptyString
    source_id: SourceId
    chunk_id: NonEmptyString
    requirement_ids: list[NonEmptyString] = Field(min_length=1)
    relevance_score: float = Field(ge=0, le=1)
    support_strength: Literal["weak", "partial", "strong"]


class EvidenceCoverage(ContractModel):
    requirement_id: NonEmptyString
    evidence_ids: list[NonEmptyString]
    coverage: Literal["missing", "partial", "sufficient"]


class EvidenceAssessment(ContractModel):
    schema_version: Literal["1.0"] = CONTRACT_VERSION
    coverage: list[EvidenceCoverage]
    sufficient: bool
    source_conflict_detected: bool
    stale_material_detected: bool


class VerificationFinding(ContractModel):
    finding_id: NonEmptyString
    code: NonEmptyString
    severity: Literal["error", "warning"]
    claim_id: str | None


class VerificationResult(ContractModel):
    schema_version: Literal["1.0"] = CONTRACT_VERSION
    outcome: Literal["passed", "failed"]
    findings: list[VerificationFinding]
    verifier_version: NonEmptyString


class PhaseRecord(ContractModel):
    phase: Literal[
        "accepted",
        "understanding",
        "retrieving",
        "assessing",
        "designing",
        "verifying",
        "finalizing",
        "terminal",
    ]
    started_at: UtcDatetime
    completed_at: UtcDatetime | None


class ReportReference(ContractModel):
    report_version_id: UUID
    conversation_id: UUID
    version: int = Field(ge=1, le=4)
    resource_path: AnnotatedResourcePath


AnnotatedResourcePath = Annotated[str, Field(pattern=r"^/v1/reports/[0-9a-f-]{36}$")]


class TerminalResult(ContractModel):
    schema_version: Literal["1.0"] = CONTRACT_VERSION
    outcome: Literal[
        "clarification_required",
        "completed",
        "failed",
        "cancelled",
        "timed_out",
    ]
    code: NonEmptyString
    report_ref: ReportReference | None
    clarification_request: ClarificationRequest | None
    retryable: bool

    @model_validator(mode="after")
    def terminal_payload_matches_outcome(self) -> TerminalResult:
        if self.outcome == "completed" and self.report_ref is None:
            msg = "completed terminal results require report_ref"
            raise ValueError(msg)
        if self.outcome == "clarification_required" and self.clarification_request is None:
            msg = "clarification_required terminal results require clarification_request"
            raise ValueError(msg)
        if self.outcome not in {"completed", "clarification_required"} and (
            self.report_ref is not None or self.clarification_request is not None
        ):
            msg = "failure terminal results cannot expose a report or clarification request"
            raise ValueError(msg)
        return self


class PolicyAssessment(ContractModel):
    schema_version: Literal["1.0"] = CONTRACT_VERSION
    allowed: bool
    reason_code: NonEmptyString | None
    safety_verdict: SafetyVerdict


class GraphInputSnapshot(ContractModel):
    """Immutable boundary passed into each local graph invocation."""

    schema_version: Literal["1.0"] = CONTRACT_VERSION
    environment: Literal["local"]
    request_id: UUID
    run_id: UUID
    conversation_id: UUID
    owner_subject_hash: Sha256
    invocation_attempt: int = Field(ge=1)
    run_kind: Literal["initial", "clarification", "refinement"]
    normalized_input: NonEmptyString | None
    clarification_answers: list[ClarificationAnswer]
    prior_report: CanonicalReport | None
    change_request: NonEmptyString | None
    active_corpus_version: NonEmptyString
    graph_version: NonEmptyString
    prompt_bundle_version: NonEmptyString
    model_config_version: NonEmptyString


class GraphState(ContractModel):
    """JSON-serializable state for deterministic local workflow boundaries."""

    schema_version: Literal["1.0"] = CONTRACT_VERSION
    snapshot: GraphInputSnapshot
    started_at: UtcDatetime
    deadline_at: UtcDatetime
    policy: PolicyAssessment
    requirements: RequirementsSpec | None
    clarification_request: ClarificationRequest | None
    retrieval_attempt: Literal[0, 1]
    retrieval_plan: RetrievalPlan | None
    retrieved_candidates: list[EvidenceCandidate]
    ranked_evidence: list[EvidenceItem]
    evidence_assessment: EvidenceAssessment | None
    draft: CanonicalReport | None
    verification: VerificationResult | None
    draft_repair_used: bool
    structured_repair_count: int = Field(ge=0, le=5)
    model_calls_used: int = Field(ge=0, le=14)
    input_tokens_used: int = Field(ge=0, le=220_000)
    output_tokens_used: int = Field(ge=0, le=65_000)
    phase_records: list[PhaseRecord]
    cancellation_requested: bool
    terminal: TerminalResult | None
