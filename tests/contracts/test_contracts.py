from __future__ import annotations

from collections.abc import Callable
from copy import deepcopy
from typing import Any

import pytest
from pydantic import ValidationError

from mini_fde.contracts.base import ContractValidationError, parse_contract
from mini_fde.contracts.events import PUBLIC_EVENT_ADAPTER, RunAcceptedEvent
from mini_fde.contracts.openapi import build_openapi_document
from mini_fde.contracts.report import CanonicalReport
from mini_fde.contracts.workflow import GraphInputSnapshot, TerminalResult
from scripts.generate_contract_artifacts import generate

UUIDS = {
    "report_id": "00000000-0000-0000-0000-000000000001",
    "report_version_id": "00000000-0000-0000-0000-000000000002",
    "conversation_id": "00000000-0000-0000-0000-000000000003",
    "run_id": "00000000-0000-0000-0000-000000000004",
    "request_id": "00000000-0000-0000-0000-000000000005",
    "event_id": "00000000-0000-0000-0000-000000000006",
}
TIME = "2026-07-24T21:40:58+00:00"
HASH_A = "a" * 64
HASH_B = "b" * 64
HASH_C = "c" * 64


def valid_report_payload() -> dict[str, Any]:
    return {
        "schema_version": "1.0",
        "rendering_contract_version": "1.0",
        **{key: value for key, value in UUIDS.items() if key != "request_id" and key != "event_id"},
        "version": 1,
        "title": "A local architecture proposal",
        "generated_at": TIME,
        "design_as_of_date": "2026-07-24",
        "corpus_version": "corpus-v1",
        "graph_version": "graph-v1",
        "prompt_bundle_version": "prompts-v1",
        "model_config_version": "models-v1",
        "model_records": [
            {
                "model_id": "fake-model",
                "resolved_model_version": "fake-model-v1",
                "prompt_version": "prompts-v1",
                "input_tokens": 1,
                "output_tokens": 1,
                "duration_ms": 1,
                "finish_reason": "stop",
                "error_category": None,
            }
        ],
        "executive_summary": ["A bounded, local proposal."],
        "problem_framing": "Design a provider-neutral local contract foundation.",
        "assumptions": [],
        "open_questions": [],
        "requirements": [
            {
                "requirement_id": "REQ-1",
                "category": "functional",
                "statement": "Validate report contracts.",
                "priority": "must",
                "source": "user",
                "evidence_needed": True,
            }
        ],
        "recommended_architecture": "Use versioned local contracts.",
        "services": [
            {
                "service_id": "local-contracts",
                "service_name": "Local contracts",
                "role": "Validation boundary",
                "location": "local",
                "data_handled": "Fixture data",
                "configuration": ["schema_version=1.0"],
                "scaling_and_cost_posture": "No managed service calls.",
                "security_controls": ["extra fields forbidden"],
                "rationale": "The foundation remains provider-neutral.",
                "alternatives_rejected": [],
                "claim_ids": ["CL-1"],
            }
        ],
        "diagram": {
            "diagram_id": "D-1",
            "kind": "flowchart",
            "mermaid_version": "placeholder",
            "source": "flowchart LR\nA-->B",
            "text_description": "A reaches B.",
            "validation_status": "valid",
            "source_hash": HASH_B,
        },
        "data_flow": ["The fixture enters the validator."],
        "security_and_privacy": ["No credentials are accepted by the models."],
        "reliability_and_operations": ["Validation is deterministic."],
        "cost_drivers": ["There are no provider calls."],
        "pricing_links": [],
        "risks": [],
        "alternatives": [],
        "implementation_phases": [
            {
                "phase_id": "P1",
                "name": "Contracts",
                "objective": "Freeze local boundaries.",
                "dependencies": [],
                "tasks": ["Generate schemas."],
                "exit_criteria": ["Artifacts have no drift."],
            }
        ],
        "confidence": {
            "overall": "high",
            "evidence_coverage_score": 1.0,
            "requirement_coverage_score": 1.0,
            "unresolved_assumption_count": 0,
            "limitations": [],
        },
        "claims": [
            {
                "claim_id": "CL-1",
                "text": "Use provider-neutral contracts.",
                "kind": "recommendation",
                "citation_source_ids": [],
                "support": "synthesized",
            }
        ],
        "sources": [
            {
                "source_id": "S1",
                "title": "Local fixture source",
                "canonical_url": "https://cloud.google.com/docs",
                "official_domain": "cloud.google.com",
                "document_type": "product_documentation",
                "product_tags": ["contracts"],
                "section_path": ["contracts"],
                "retrieved_chunk_ids": ["chunk-1"],
                "source_updated_at": None,
                "crawled_at": TIME,
                "corpus_version": "corpus-v1",
                "content_hash": HASH_A,
            }
        ],
        "verifier_summary": {
            "outcome": "passed",
            "finding_count": 0,
            "verifier_version": "validator-v1",
        },
        "validation_summary": {
            "outcome": "passed",
            "validator_version": "validator-v1",
            "report_sha256": HASH_C,
        },
    }


def add_unknown_field(payload: dict[str, Any]) -> None:
    payload["unexpected"] = True


def use_unknown_citation(payload: dict[str, Any]) -> None:
    payload["claims"][0]["citation_source_ids"] = ["S9"]


def use_unknown_support(payload: dict[str, Any]) -> None:
    payload["claims"][0]["support"] = "future"


def use_uncited_direct_claim(payload: dict[str, Any], kind: str) -> None:
    payload["claims"][0]["kind"] = kind
    payload["claims"][0]["support"] = "direct"


@pytest.mark.contract
def test_canonical_report_accepts_complete_resolvable_contract() -> None:
    report = parse_contract(CanonicalReport, valid_report_payload())

    assert report.schema_version == "1.0"
    assert report.sources[0].source_id == "S1"


@pytest.mark.contract
@pytest.mark.parametrize(
    ("mutate", "expected_message"),
    [
        (
            use_unknown_citation,
            "claim citations must resolve to report sources",
        ),
        (
            add_unknown_field,
            "Extra inputs are not permitted",
        ),
        (
            use_unknown_support,
            "Input should be",
        ),
    ],
)
def test_canonical_report_rejects_invalid_contracts(
    mutate: Callable[[dict[str, Any]], None], expected_message: str
) -> None:
    payload = deepcopy(valid_report_payload())
    mutate(payload)

    with pytest.raises(ContractValidationError) as raised:
        parse_contract(CanonicalReport, payload)

    assert raised.value.code == "contract_validation_failed"
    assert any(expected_message in issue.message for issue in raised.value.issues)


@pytest.mark.contract
@pytest.mark.parametrize("kind", ["factual", "recommendation", "assumption", "limitation"])
def test_canonical_report_rejects_uncited_direct_claims_for_every_kind(kind: str) -> None:
    payload = deepcopy(valid_report_payload())
    use_uncited_direct_claim(payload, kind)

    with pytest.raises(ContractValidationError) as raised:
        parse_contract(CanonicalReport, payload)

    assert any(
        "direct claims require at least one citation_source_id" in issue.message
        for issue in raised.value.issues
    )


@pytest.mark.contract
def test_canonical_report_allows_uncited_non_direct_claim() -> None:
    payload = deepcopy(valid_report_payload())
    payload["claims"][0]["support"] = "assumed"

    report = parse_contract(CanonicalReport, payload)

    assert report.claims[0].citation_source_ids == []


@pytest.mark.contract
def test_workflow_nullable_fields_are_required_at_the_boundary() -> None:
    payload: dict[str, Any] = {
        "schema_version": "1.0",
        "environment": "local",
        "request_id": UUIDS["request_id"],
        "run_id": UUIDS["run_id"],
        "conversation_id": UUIDS["conversation_id"],
        "owner_subject_hash": HASH_A,
        "invocation_attempt": 1,
        "run_kind": "initial",
        "normalized_input": "A request",
        "clarification_answers": [],
        "prior_report": None,
        "change_request": None,
        "active_corpus_version": "corpus-v1",
        "graph_version": "graph-v1",
        "prompt_bundle_version": "prompts-v1",
        "model_config_version": "models-v1",
    }
    snapshot = parse_contract(GraphInputSnapshot, payload)
    assert snapshot.prior_report is None

    payload.pop("prior_report")
    with pytest.raises(ContractValidationError) as raised:
        parse_contract(GraphInputSnapshot, payload)
    assert {issue.code for issue in raised.value.issues} == {"missing"}


@pytest.mark.contract
def test_public_events_reject_private_output_and_terminal_results_require_references() -> None:
    accepted = PUBLIC_EVENT_ADAPTER.validate_python(
        {
            "schema_version": "1.0",
            "event_id": UUIDS["event_id"],
            "run_id": UUIDS["run_id"],
            "emitted_at": TIME,
            "event": "run.accepted",
            "phase": "accepted",
        }
    )
    assert isinstance(accepted, RunAcceptedEvent)

    with pytest.raises(ValidationError):
        PUBLIC_EVENT_ADAPTER.validate_python(
            {
                **accepted.model_dump(mode="json"),
                "raw_model_output": "private",
            }
        )
    with pytest.raises(ContractValidationError):
        parse_contract(
            TerminalResult,
            {
                "schema_version": "1.0",
                "outcome": "completed",
                "code": "completed",
                "report_ref": None,
                "clarification_request": None,
                "retryable": False,
            },
        )


@pytest.mark.contract
def test_generated_schemas_require_citations_and_resolvable_event_mappings() -> None:
    claim_schema = CanonicalReport.model_json_schema()["$defs"]["Claim"]
    assert {
        "if": {
            "properties": {
                "support": {"const": "direct"},
            },
            "required": ["support"],
        },
        "then": {"properties": {"citation_source_ids": {"minItems": 1}}},
    } in claim_schema["allOf"]

    schemas = build_openapi_document()["components"]["schemas"]
    mappings = schemas["PublicEvent"]["discriminator"]["mapping"]
    assert all(
        reference.startswith("#/components/schemas/")
        and reference.removeprefix("#/components/schemas/") in schemas
        for reference in mappings.values()
    )


@pytest.mark.contract
def test_generated_contract_artifacts_have_no_drift() -> None:
    assert generate(check=True)
