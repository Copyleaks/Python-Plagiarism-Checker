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
from ..BaseModels.MetadataModel import MetadataModel
from pydantic import BaseModel

class NewResultsInternetModel(BaseModel):

    """Unique result ID to identify the result."""
    _id: Optional[str] = None, 
    
    """Document title. Mostly extracted from the document content."""
    _title: Optional[str] = None,

    """Document brief introduction. Mostly extracted from the document content."""
    _introduction: Optional[str] = None,

    """Total matched words between this result and the scanned document."""
    _matched_words: Optional[int] = None,  

    _scan_id: Optional[str] = None,

    """Metadata object"""
    _metadata: Optional[MetadataModel] = None, 

    """Public URL of the resource."""
    _url: Optional[str] = None
    

    def __init__(self,
                 id: Optional[str] = None, 
                 title: Optional[str] = None,
                 introduction: Optional[str] = None,
                 matched_words: Optional[int] = None, 
                 scan_id: Optional[str] = None,     
                 metadata: Optional[MetadataModel] = None, 
                 url: Optional[str] = None):
        """
        Initializes a NewResultsInternet object, storing values in internal attributes..
        """
        super().__init__(id=id,title=title,introduction=introduction,matched_words=matched_words,scan_id=scan_id,metadata=metadata,url=url)
        self._id: Optional[str] = id
        self._title: Optional[str] = title
        self._introduction: Optional[str] = introduction
        self._matched_words: Optional[int] = matched_words
        self._scan_id: Optional[str] = scan_id
        self._metadata: Optional[MetadataModel] = metadata 
        self._url: Optional[str] = url
