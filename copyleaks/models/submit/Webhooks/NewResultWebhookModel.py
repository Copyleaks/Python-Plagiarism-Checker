from typing import List, Optional
from pydantic import Field, field_validator
from .HelperModels.BaseModels.CopyleaksWebhookBaseModel import none_to_empty_list
from .HelperModels.BaseModels.WebhookModel import WebhookModel
from .HelperModels.NewResultModels.NewResultInternetModel import NewResultsInternetModel
from .HelperModels.NewResultModels.NewResultRepositoriesModel import NewResultsRepositoriesModel
from .HelperModels.NewResultModels.NewResultScoreModel import NewResultScoreModel
from .HelperModels.ResultsModels.InternalAiDataModel import InternalAiDataModel
from .HelperModels.ResultsModels.SharedResultsModel import SharedResultsModel


class NewResultWebhookModel(WebhookModel):
    """New results found while the scan runs. Parse it with `NewResultWebhookModel(**request.json)`."""
    __positional_fields__ = ('score', 'internet', 'database', 'batch', 'repositories')

    score: Optional[NewResultScoreModel] = Field(
        default=None,
        description="The score of the scan so far.",
        alias="score"
    )

    internet: List[NewResultsInternetModel] = Field(
        default_factory=list,
        description="New results found on the internet.",
        alias="internet"
    )

    database: List[SharedResultsModel] = Field(
        default_factory=list,
        description="New results found in the Copyleaks internal database.",
        alias="database"
    )

    batch: List[SharedResultsModel] = Field(
        default_factory=list,
        description="New results found in the same batch.",
        alias="batch"
    )

    repositories: List[NewResultsRepositoriesModel] = Field(
        default_factory=list,
        description="New results found in your Private Cloud Hub repositories.",
        alias="repositories"
    )

    internal_ai_data: List[InternalAiDataModel] = Field(
        default_factory=list,
        description="New matches in the Copyleaks internal AI database.",
        alias="internalAIData"
    )

    @field_validator('internet', 'database', 'batch', 'repositories', 'internal_ai_data', mode='before')
    @classmethod
    def lists_none_to_empty(cls, v):
        return none_to_empty_list(v)
