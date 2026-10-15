from typing import Optional
from pydantic import Field

from copyleaks.helpers.copyleaks_dict_access_mixin import CopyleaksDictAccessMixin


class CopyleaksAiTextDetectionCreditsResponseModel(CopyleaksDictAccessMixin):
    """Credit balance of the AI Text Detector."""

    credits: Optional[int] = Field(
        default=None,
        description="The number of available credits.",
        alias="credits"
    )
