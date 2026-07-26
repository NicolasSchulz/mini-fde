"""Common validation and versioning primitives for public contracts."""

from __future__ import annotations

from datetime import datetime
from typing import Annotated, Any, Final, Literal, TypeVar

from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    Field,
    ValidationError,
)

CONTRACT_VERSION: Final[Literal["1.0"]] = "1.0"
SourceId = Annotated[str, Field(pattern=r"^S[1-9][0-9]*$")]
Sha256 = Annotated[str, Field(pattern=r"^[a-f0-9]{64}$")]
NonEmptyString = Annotated[str, Field(min_length=1)]


def _require_utc(value: datetime) -> datetime:
    if value.tzinfo is None or value.utcoffset() is None:
        msg = "datetime values must include an offset"
        raise ValueError(msg)
    return value


UtcDatetime = Annotated[datetime, AfterValidator(_require_utc)]


class ContractModel(BaseModel):
    """Base configuration shared by all serializable domain contracts."""

    model_config = ConfigDict(
        extra="forbid",
        frozen=True,
        json_schema_extra={"x-contract-version": CONTRACT_VERSION},
    )


class ValidationIssue(ContractModel):
    location: tuple[str | int, ...]
    code: NonEmptyString
    message: NonEmptyString


class ContractValidationError(ValueError):
    """Stable validation boundary used instead of provider-specific exceptions."""

    code = "contract_validation_failed"

    def __init__(self, issues: tuple[ValidationIssue, ...]) -> None:
        super().__init__(self.code)
        self.issues = issues


ModelT = TypeVar("ModelT", bound=ContractModel)


def parse_contract(model: type[ModelT], payload: Any) -> ModelT:
    """Validate a payload and expose stable, sanitizable contract failures."""

    try:
        return model.model_validate(payload)
    except ValidationError as error:
        issues = tuple(
            ValidationIssue(
                location=tuple(item["loc"]),
                code=str(item["type"]),
                message=str(item["msg"]),
            )
            for item in error.errors(include_url=False)
        )
        raise ContractValidationError(issues) from None
