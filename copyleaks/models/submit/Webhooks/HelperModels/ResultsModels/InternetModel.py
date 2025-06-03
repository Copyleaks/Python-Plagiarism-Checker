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
from ..NewResultModels.NewResultInternetModel import NewResultsInternetModel
from ..BaseModels.MetadataModel import MetadataModel
from .TagsModel import TagsModel
class InternetModel(NewResultsInternetModel):
    """
    Represents an internet result, inheriting general details from
    NewResultsInternet and adding specific tags.
    """
    _tags: List['TagsModel'] = []

    def __init__(self,
                 tags: Optional[List['TagsModel']] = None,
                 id_val: Optional[str] = None,
                 title: Optional[str] = None,
                 introduction: Optional[str] = None,
                 matched_words: Optional[int] = None,
                 scan_id: Optional[str] = None,
                 metadata: Optional['MetadataModel'] = None,
                 url: Optional[str] = None):
        """
        Initializes an Internet result object.
        """
        super().__init__(id_val=id_val,
                         title=title,
                         introduction=introduction,
                         matched_words=matched_words,
                         scan_id=scan_id,
                         metadata=metadata,
                         url=url)
        self._tags = list(tags) if tags else []
