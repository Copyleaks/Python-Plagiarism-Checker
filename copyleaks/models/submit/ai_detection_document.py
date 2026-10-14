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
from copyleaks.helpers.copyleaks_client_helper import CopyleaksClientHelper


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
        return CopyleaksClientHelper.to_json(self)


class NaturalLanguageDocument(AiDetectionDocument):
    def __init__(self, text):
        super().__init__(text)

    def get_language(self):
        return self.language

    def set_language(self, value):
        self.language = value

    def get_explain(self):
        """
            Whether AI Logic explanations are requested.
        """
        return self.explain

    def set_explain(self, value):
        """
            Enable AI Logic: the response then has `explain`, which shows the AI patterns found in the text.
            Explanations are returned for the AI Logic supported languages only.
            Leave it unset to get the server default (False).

            Parameters:
                value: Boolean.
        """
        assert isinstance(value, bool)
        self.explain = value

    def get_sensitivity(self):
        """
            The AI detection sensitivity.
        """
        return self.sensitivity

    def set_sensitivity(self, value):
        """
            Control the behavior of the AI detection, from 1 to 3:
            1 detects text copied from an AI tool without edits, 2 (the server default) also detects
            text with minor changes, and 3 also detects heavily modified text.

            Parameters:
                value: Integer from 1 to 3.
        """
        assert isinstance(value, int) and not isinstance(value, bool) and 1 <= value <= 3
        self.sensitivity = value
