from typing import List, Optional
from pydantic import Field, field_validator

from ..BaseModels.CopyleaksWebhookBaseModel import CopyleaksWebhookBaseModel, none_to_empty_list
from ..ResultsModels.BatchModel import BatchModel
from ..ResultsModels.DatabaseModel import DatabaseModel
from ..ResultsModels.InternalAiDataModel import InternalAiDataModel
from ..ResultsModels.InternetModel import InternetModel
from ..ResultsModels.RepositoriesModel import RepositoriesModel
from ..ResultsModels.ScoreModel import ScoreModel


class ResultsModel(CopyleaksWebhookBaseModel):
    """All the results that were found, and their aggregated score."""
    __positional_fields__ = ('database', 'batch', 'repositories', 'score', 'internet')

    internet: List[InternetModel] = Field(
        default_factory=list,
        description="Results found on the internet.",
        alias="internet"
    )

    database: List[DatabaseModel] = Field(
        default_factory=list,
        description="Results found in the Copyleaks internal database.",
        alias="database"
    )

    batch: List[BatchModel] = Field(
        default_factory=list,
        description="Results found in the same batch.",
        alias="batch"
    )

    repositories: List[RepositoriesModel] = Field(
        default_factory=list,
        description="Results found in your Private Cloud Hub repositories.",
        alias="repositories"
    )

    internal_ai_data: List[InternalAiDataModel] = Field(
        default_factory=list,
        description="Matches in the Copyleaks internal AI database, found by Internal AI Source Match.",
        alias="internalAIData"
    )

    score: Optional[ScoreModel] = Field(
        default=None,
        description="The aggregated score of all results.",
        alias="score"
    )

    @field_validator('internet', 'database', 'batch', 'repositories', 'internal_ai_data', mode='before')
    @classmethod
    def lists_none_to_empty(cls, v):
        return none_to_empty_list(v)
