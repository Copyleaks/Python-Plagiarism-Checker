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

class AiDetectionDocument(ABC):
    def __init__(self, text):
        assert text
        self.text = text

    def get_text(self):
        return self.text

    def set_text(self, value):
        assert value
        self.text = value

    def get_sandbox(self):
        return self.sandbox

    def set_sandbox(self, value):
        self.sandbox = value

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class NaturalLanguageDocument(AiDetectionDocument):
    def __init__(self, text):
        super().__init__(text)

    def get_language(self):
        return self.language

    def set_language(self, value):
        self.language = value


class SourceCodeDocument(AiDetectionDocument):
    def __init__(self, text, filename):
        super().__init__(text)
        self.filename = filename

    def get_filename(self):
        return self.filename

    def set_filename(self, value):
        assert value
        self.filename = value
