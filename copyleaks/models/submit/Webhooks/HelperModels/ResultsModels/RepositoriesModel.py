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
from pydantic import Field

from .SharedResultsModel import SharedResultsModel
from .RepositoryMetadataModel import RepositoryMetadataModel


class RepositoriesModel(SharedResultsModel):
    """
    A result found in a Private Cloud Hub repository.
    """
    __positional_fields__ = ('repository_id', 'tags', 'id', 'title', 'introduction', 'matched_words', 'scan_id',
                             'metadata')

    repository_id: Optional[str] = Field(
        default=None,
        description="The repository Id that has the result.",
        alias="repositoryId"
    )

    metadata: Optional[RepositoryMetadataModel] = Field(
        default=None,
        description="Metadata of the result.",
        alias="metadata"
    )
