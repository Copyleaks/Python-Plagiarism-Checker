from typing import Optional
from pydantic import Field, model_validator

from ..BaseModels.CopyleaksWebhookBaseModel import CopyleaksWebhookBaseModel


class NewResultScoreModel(CopyleaksWebhookBaseModel):
    """The score of the scan so far, in the new result webhook. A plain number is accepted as `aggregated_score`."""
    __positional_fields__ = ('aggregated_score',)

    aggregated_score: Optional[float] = Field(
        default=None,
        description="The percentage of similar words from all results found so far.",
        alias="aggregatedScore"
    )

    @model_validator(mode='before')
    @classmethod
    def number_to_score(cls, data):
        if isinstance(data, (int, float)) and not isinstance(data, bool):
            return {'aggregatedScore': data}
        return data
