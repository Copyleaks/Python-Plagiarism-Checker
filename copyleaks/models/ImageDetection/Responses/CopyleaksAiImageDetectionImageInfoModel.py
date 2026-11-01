from typing import Optional
from pydantic import BaseModel, Field

from copyleaks.models.ImageDetection.Responses.CopyleaksImageMetadataModel import CopyleaksImageMetadataModel
from copyleaks.models.ImageDetection.Responses.CopyleaksImageShapeModel import CopyleaksImageShapeModel


class CopyleaksAiImageDetectionImageInfoModel(BaseModel):
    """Information about the analyzed image."""
    
    shape: Optional[CopyleaksImageShapeModel] = Field(
        default=None,
        description="Dimensions of the analyzed image.",
        alias="shape"
    )
    
    metadata: Optional[CopyleaksImageMetadataModel] = Field(
        default=None,
        description="Optional metadata extracted from the image.",
        alias="metadata"
    )

