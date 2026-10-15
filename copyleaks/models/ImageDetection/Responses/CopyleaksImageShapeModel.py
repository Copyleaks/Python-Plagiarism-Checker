from pydantic import BaseModel, Field, field_validator


class CopyleaksImageShapeModel(BaseModel):
    """Dimensions of the analyzed image."""
    
    height: int = Field(
        ...,
        description="Height of the image in pixels.",
        ge=1,
        alias="height"
    )
    
    width: int = Field(
        ...,
        description="Width of the image in pixels.",
        ge=1,
        alias="width"
    )
