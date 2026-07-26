"""Generate the local contract OpenAPI document without implementing a BFF."""

from __future__ import annotations

from typing import Any

from fastapi.openapi.utils import get_openapi

from mini_fde.contracts.api import PageEnvelope, ProblemDetails
from mini_fde.contracts.base import CONTRACT_VERSION
from mini_fde.contracts.corpus import Chunk, CorpusManifest, CorpusVersion, NormalizedDocument
from mini_fde.contracts.events import PUBLIC_EVENT_ADAPTER
from mini_fde.contracts.report import CanonicalReport
from mini_fde.contracts.safety import SafetyVerdict
from mini_fde.contracts.workflow import GraphInputSnapshot, GraphState, TerminalResult


def _replace_definition_references(value: Any) -> Any:
    if isinstance(value, dict):
        return {
            key: (
                f"#/components/schemas/{child.removeprefix('#/$defs/')}"
                if key == "$ref" and isinstance(child, str) and child.startswith("#/$defs/")
                else {
                    mapping_key: (
                        f"#/components/schemas/{mapping_reference.removeprefix('#/$defs/')}"
                        if isinstance(mapping_reference, str)
                        and mapping_reference.startswith("#/$defs/")
                        else _replace_definition_references(mapping_reference)
                    )
                    for mapping_key, mapping_reference in child.items()
                }
                if key == "mapping" and isinstance(child, dict)
                else _replace_definition_references(child)
            )
            for key, child in value.items()
        }
    if isinstance(value, list):
        return [_replace_definition_references(item) for item in value]
    return value


def build_openapi_document() -> dict[str, Any]:
    """Create a schema-only document; an executable BFF belongs to a later phase."""

    document = get_openapi(
        title="mini-fde local contract foundation",
        version=CONTRACT_VERSION,
        openapi_version="3.1.0",
        description=(
            "Provider-neutral Phase 1 contract components only. "
            "No executable browser or internal BFF operations are implemented."
        ),
        routes=[],
    )
    components: dict[str, Any] = {}

    schemas: dict[str, Any] = {
        "CanonicalReport": CanonicalReport.model_json_schema(),
        "CorpusManifest": CorpusManifest.model_json_schema(),
        "NormalizedDocument": NormalizedDocument.model_json_schema(),
        "Chunk": Chunk.model_json_schema(),
        "CorpusVersion": CorpusVersion.model_json_schema(),
        "SafetyVerdict": SafetyVerdict.model_json_schema(),
        "GraphInputSnapshot": GraphInputSnapshot.model_json_schema(),
        "GraphState": GraphState.model_json_schema(),
        "TerminalResult": TerminalResult.model_json_schema(),
        "ProblemDetails": ProblemDetails.model_json_schema(),
        "PageEnvelope": PageEnvelope[CanonicalReport].model_json_schema(),
        "PublicEvent": PUBLIC_EVENT_ADAPTER.json_schema(),
    }
    for name, schema in schemas.items():
        definitions = schema.pop("$defs", {})
        for definition_name, definition in definitions.items():
            normalized_definition = _replace_definition_references(definition)
            existing = components.get(definition_name)
            if existing is not None and existing != normalized_definition:
                msg = f"conflicting component schema for {definition_name}"
                raise ValueError(msg)
            components[definition_name] = normalized_definition
        components[name] = _replace_definition_references(schema)

    document["paths"] = {}
    document["components"] = {"schemas": components}
    document["x-contract-version"] = CONTRACT_VERSION
    document["x-contract-scope"] = "local-provider-neutral-foundation"
    return document
