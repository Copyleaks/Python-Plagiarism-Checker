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

from typing import Any, List, Optional
from .HelperModels.BaseModels.WebhookModel import WebhookModel
from .HelperModels.NewResultModels.NewResultInternetModel import NewResultsInternetModel
from .HelperModels.NewResultModels.NewResultRepositoriesModel import NewResultsRepositoriesModel
from .HelperModels.NewResultModels.NewResultScoreModel import NewResultScoreModel
from .HelperModels.ResultsModels.SharedResultsModel import SharedResultsModel

class NewResultWebhookModel(WebhookModel):
    """
    Represents a webhook payload containing new results found during a scan.
    Inherits from Webhook.
    """
    score: Optional[NewResultScoreModel] = None
    internet: List[NewResultsInternetModel] = []
    database: List[SharedResultsModel] = []
    batch: List[SharedResultsModel] = []
    repositories: List[NewResultsRepositoriesModel] = []

    def __init__(self,
                 score: Optional[NewResultScoreModel] = None,
                 internet: Optional[List[NewResultsInternetModel]] = None,
                 database: Optional[List[SharedResultsModel]] = None,
                 batch: Optional[List[SharedResultsModel]] = None,
                 repositories: Optional[List[NewResultsRepositoriesModel]] = None,
                 **kwargs: Any):
        """
        Initializes a NewResultWebhook object.
        """
        super().__init__(**kwargs)
        self.score = score
        self.internet = internet if internet is not None else []
        self.database = database if database is not None else []
        self.batch = batch if batch is not None else []
        self.repositories = repositories if repositories is not None else []