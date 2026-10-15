from typing import Optional
from pydantic import Field

from ..BaseModels.CopyleaksWebhookBaseModel import CopyleaksWebhookBaseModel


class ReferencesValidationSummaryModel(CopyleaksWebhookBaseModel):
    """Counts of the references that the Citation Checker detected and validated."""

    total: Optional[int] = Field(
        default=None,
        description="The total number of references detected in the scanned content.",
        alias="total"
    )

    academic: Optional[int] = Field(
        default=None,
        description="The number of detected references that were identified as academic.",
        alias="academic"
    )

    academic_validated: Optional[int] = Field(
        default=None,
        description="The number of academic references fully corroborated against the Copyleaks academic citation index.",
        alias="academicValidated"
    )

    non_academic_validated: Optional[int] = Field(
        default=None,
        description="The number of non-academic references fully corroborated against their cited source.",
        alias="nonAcademicValidated"
    )


class ReferencesValidationModel(CopyleaksWebhookBaseModel):
    """Citation Checker summary. The per-reference results are in the crawled version of the scan."""

    summary: Optional[ReferencesValidationSummaryModel] = Field(
        default=None,
        description="An aggregated count of the references that were detected and validated.",
        alias="summary"
    )
