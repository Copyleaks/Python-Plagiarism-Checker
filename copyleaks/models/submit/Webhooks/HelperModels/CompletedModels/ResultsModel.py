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

from ..BaseModels.CopyleaksWebhookBaseModel import CopyleaksWebhookBaseModel, none_to_empty_list
from ..ResultsModels.BatchModel import BatchModel
from ..ResultsModels.DatabaseModel import DatabaseModel
from ..ResultsModels.InternalAiDataModel import InternalAiDataModel
from ..ResultsModels.InternetModel import InternetModel
from ..ResultsModels.RepositoriesModel import RepositoriesModel
from ..ResultsModels.ScoreModel import ScoreModel


class ResultsModel(CopyleaksWebhookBaseModel):
    """
    All the results that were found, and their aggregated score.
    """
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
