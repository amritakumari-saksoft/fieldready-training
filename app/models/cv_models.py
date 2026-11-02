"""Structured models for extracting information from CVs."""

from pydantic import BaseModel, ConfigDict, Field


class CVData(BaseModel):
    """Validated information extracted from a CV."""

    model_config = ConfigDict(extra="forbid")

    full_name: str | None = None
    email: str | None = None
    phone: str | None = None
    skills: list[str] = Field(default_factory=list)
    education: list[str] = Field(default_factory=list)
    experience_years: float | None = Field(default=None, ge=0)
