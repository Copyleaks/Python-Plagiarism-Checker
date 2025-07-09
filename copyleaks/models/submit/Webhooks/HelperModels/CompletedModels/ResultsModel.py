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

from typing import Optional, List
from ..ResultsModels.BatchModel import BatchModel
from ..ResultsModels.DatabaseModel import DatabaseModel
from ..ResultsModels.InternetModel import InternetModel
from ..ResultsModels.RepositoriesModel import RepositoriesModel
from ..ResultsModels.ScoreModel import ScoreModel
from typing import Optional, List
from pydantic import BaseModel

class ResultsModel(BaseModel):
    _database: List['DatabaseModel'] = []
    _batch: List['BatchModel'] = []
    _repositories: List['RepositoriesModel'] = []
    _score: Optional['ScoreModel'] = None
    _internet: List['InternetModel'] = []

    def __init__(self,
                 database: Optional[List['DatabaseModel']] = None,
                 batch: Optional[List['BatchModel']] = None,
                 repositories: Optional[List['RepositoriesModel']] = None,
                 score: Optional['ScoreModel'] = None,
                 internet: Optional[List['InternetModel']] = None):
        """
        Initializes the Results object containing lists of different result types.
        """
        super().__init__(database=database, batch=batch, repositories=repositories, score=score, internet=internet)
        self._database = list(database) if database else []
        self._batch = list(batch) if batch else []
        self._repositories = list(repositories) if repositories else []
        self._score = score
        self._internet = list(internet) if internet else []