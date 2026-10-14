'''
 The MIT License(MIT)
 
 Copyright(c) 2016 Copyleaks LTD (https://copyleaks.com)
 
 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:
 
 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.
 
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 SOFTWARE.
'''

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
    """
    Represents a webhook payload containing new results found during a scan.
    Inherits from Webhook. Parse the webhook body with `NewResultWebhookModel(**request.json)`.
    """
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
