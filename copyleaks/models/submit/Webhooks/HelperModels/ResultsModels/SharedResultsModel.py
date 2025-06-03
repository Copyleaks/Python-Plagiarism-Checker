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
from pydantic import BaseModel
from ..BaseModels.MetadataModel import MetadataModel

class SharedResultsModel(BaseModel):
    """
    Represents shared details about a result found during a scan.
    """
    _id_val: Optional[str] = None
    _title: Optional[str] = None
    _introduction: Optional[str] = None
    _matched_words: Optional[int] = None
    _scan_id: Optional[str] = None
    _metadata: Optional[MetadataModel] = None

    def __init__(self,
                 id_val: Optional[str] = None, 
                 title: Optional[str] = None,
                 introduction: Optional[str] = None,
                 matched_words: Optional[int] = None, 
                 scan_id: Optional[str] = None,    
                 metadata: Optional[MetadataModel] = None):
        """
        Initializes a SharedResultsModel object.
        """
        super().__init__(id_val=id_val, title=title, introduction=introduction,
                         matched_words=matched_words, scan_id=scan_id, metadata=metadata)
        self._id_val = id_val
        self._title = title
        self._introduction = introduction
        self._matched_words = matched_words
        self._scan_id = scan_id
        self._metadata = metadata
