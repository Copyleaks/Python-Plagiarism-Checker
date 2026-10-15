from typing import Optional
from pydantic import Field

from ..BaseModels.CopyleaksWebhookBaseModel import CopyleaksWebhookBaseModel


class ScoreModel(CopyleaksWebhookBaseModel):
    __positional_fields__ = ('identical_words', 'minor_changed_words', 'related_meaning_words', 'aggregated_score')

    identical_words: Optional[int] = Field(
        default=None,
        description="Number of words which matched exactly.",
        alias="identicalWords"
    )

    minor_changed_words: Optional[int] = Field(
        default=None,
        description="Number of nearly identical words with small differences like 'slow' and 'slowly'.",
        alias="minorChangedWords"
    )

    related_meaning_words: Optional[int] = Field(
        default=None,
        description="Number of paraphrased words showing similar ideas with different words.",
        alias="relatedMeaningWords"
    )

    aggregated_score: Optional[float] = Field(
        default=None,
        description="The percentage of similar words from all results. Excluded references, quotations, etc. are not counted.",
        alias="aggregatedScore"
    )
