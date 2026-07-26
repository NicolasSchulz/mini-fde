"""Provider-neutral corpus and evidence contracts."""

from __future__ import annotations

from typing import Literal

from pydantic import AnyHttpUrl, Field, model_validator

from mini_fde.contracts.base import (
    CONTRACT_VERSION,
    ContractModel,
    NonEmptyString,
    Sha256,
    UtcDatetime,
)


class SourceManifestEntry(ContractModel):
    source_url: AnyHttpUrl
    document_type: Literal[
        "product_documentation",
        "architecture_center",
        "security_guidance",
        "operations_guidance",
        "pricing",
        "lifecycle_notice",
    ]
    product_tags: list[NonEmptyString]
    expected_official_domain: NonEmptyString


class CorpusManifest(ContractModel):
    schema_version: Literal["1.0"] = CONTRACT_VERSION
    corpus_version: NonEmptyString
    source_rules_commit: Sha256
    generated_at: UtcDatetime
    sources: list[SourceManifestEntry] = Field(min_length=1)


class NormalizedDocument(ContractModel):
    schema_version: Literal["1.0"] = CONTRACT_VERSION
    document_id: NonEmptyString
    canonical_url: AnyHttpUrl
    title: NonEmptyString
    document_type: NonEmptyString
    product_tags: list[NonEmptyString]
    normalized_markdown: NonEmptyString
    source_updated_at: UtcDatetime | None
    crawled_at: UtcDatetime
    corpus_version: NonEmptyString
    content_hash: Sha256

    @model_validator(mode="after")
    def canonical_url_is_https(self) -> NormalizedDocument:
        if self.canonical_url.scheme != "https":
            msg = "canonical_url must use HTTPS"
            raise ValueError(msg)
        return self


class Chunk(ContractModel):
    schema_version: Literal["1.0"] = CONTRACT_VERSION
    chunk_id: NonEmptyString
    chunk_logical_id: NonEmptyString
    document_id: NonEmptyString
    ordinal: int = Field(ge=0)
    section_path: list[NonEmptyString]
    text: NonEmptyString
    ranking_text: NonEmptyString
    token_count: int = Field(ge=1)
    corpus_version: NonEmptyString
    content_hash: Sha256


class CorpusVersion(ContractModel):
    schema_version: Literal["1.0"] = CONTRACT_VERSION
    corpus_version: NonEmptyString
    status: Literal["staged", "active", "inactive", "failed"]
    manifest_sha256: Sha256
    document_count: int = Field(ge=0)
    chunk_count: int = Field(ge=0)
    created_at: UtcDatetime
    activated_at: UtcDatetime | None
