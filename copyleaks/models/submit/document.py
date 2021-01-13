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

from abc import ABC
import json


class Document(ABC):

    def get_properties(self):
        return self.properties

    def set_properties(self, value):
        self.properties = value

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class FileDocument(Document):
    def __init__(self, base64, filename):
        self.set_base64(base64)
        self.set_filename(filename)

    def get_base64(self):
        return self.base64

    def set_base64(self, value):
        assert value
        self.base64 = value

    def get_filename(self):
        return self.filename

    def set_filename(self, value):
        assert value
        self.filename = value


class OcrFileDocument(FileDocument):
    def get_language(self):
        return self.langCode

    def set_language(self, value):
        self.langCode = value


class UrlDocument(Document):
    def get_url(self):
        return self.url

    def set_url(self, value):
        self.url = value
