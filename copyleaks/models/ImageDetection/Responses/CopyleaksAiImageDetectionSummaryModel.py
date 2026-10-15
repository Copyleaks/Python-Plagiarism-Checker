from pydantic import BaseModel, Field, field_validator


class CopyleaksAiImageDetectionSummaryModel(BaseModel):
    """Summary statistics of the AI detection analysis."""
    
    human: float = Field(
        ...,
        description="Percentage of pixels suspected to be human-created.",
        ge=0.0,
        le=1.0,
        alias="human"
    )
    
    ai: float = Field(
        ...,
        description="Percentage of pixels suspected to be AI-generated.",
        ge=0.0,
        le=1.0,
        alias="ai"
    )

