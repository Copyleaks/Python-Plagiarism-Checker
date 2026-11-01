from typing import List
from pydantic import ConfigDict, Field, field_validator

from copyleaks.helpers.copyleaks_dict_access_mixin import CopyleaksDictAccessMixin


class CopyleaksSupportedAiTextDetectionFileTypesResponseModel(CopyleaksDictAccessMixin):
    """File types supported by AI Text Detection, e.g. "pdf" and "docx"."""

    model_config = ConfigDict(populate_by_name=True)

    supported_ai_file_types: List[str] = Field(
        default_factory=list,
        description="The supported file extensions, without the dot.",
        alias="supportedAiFileTypes"
    )

    @field_validator('supported_ai_file_types', mode='before')
    @classmethod
    def none_to_empty(cls, v):
        return [] if v is None else v
