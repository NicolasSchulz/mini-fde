"""Versioned, provider-neutral contracts for the local mini-fDE core."""

from mini_fde.contracts.api import PageEnvelope, ProblemDetails
from mini_fde.contracts.corpus import (
    Chunk,
    CorpusManifest,
    CorpusVersion,
    NormalizedDocument,
)
from mini_fde.contracts.events import PublicEvent
from mini_fde.contracts.report import CanonicalReport
from mini_fde.contracts.safety import SafetyVerdict
from mini_fde.contracts.workflow import GraphInputSnapshot, GraphState, TerminalResult

__all__ = [
    "CanonicalReport",
    "Chunk",
    "CorpusManifest",
    "CorpusVersion",
    "GraphInputSnapshot",
    "GraphState",
    "NormalizedDocument",
    "PageEnvelope",
    "ProblemDetails",
    "PublicEvent",
    "SafetyVerdict",
    "TerminalResult",
]
