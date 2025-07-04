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

from typing import Optional
from ..ResultsModels.SharedResultsModel import SharedResultsModel
from ..ResultsModels.RepositoryMetadataModel import RepositoryMetadataModel

class NewResultsRepositoriesModel(SharedResultsModel):

    """The repository Id that has the result."""
    _repository_id: Optional[str] = None

    def __init__(self,
                 repository_id: Optional[str] = None, # snake_case
                 # Arguments for the parent SharedResultsModel class:
                 id_val: Optional[str] = None,
                 title: Optional[str] = None,
                 introduction: Optional[str] = None,
                 matched_words: Optional[int] = None,
                 scan_id: Optional[str] = None,
                 metadata: Optional[RepositoryMetadataModel] = None):
        """
        Initializes a NewResultsRepositories object.
        """
        super().__init__(id_val=id_val,
                         title=title,
                         introduction=introduction,
                         matched_words=matched_words,
                         scan_id=scan_id,
                         metadata=metadata) 
        self._repository_id = repository_id
