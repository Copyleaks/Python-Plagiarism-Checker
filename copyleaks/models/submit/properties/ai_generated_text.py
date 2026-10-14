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


from copyleaks.models.submit.properties.ai_generated_text_explain import AIGeneratedTextExplain


class AIGeneratedText:
    def get_detect(self):
        '''
            Detects whether the text was written by an AI.
        '''
        return self.detect
        

    def set_detect(self, value):
        '''
            Set whether to detect AI Generated text.

            Parameters: 
                value: Boolean.
        '''
        assert isinstance(value, bool)

        self.detect = value

    def get_sensitivity(self):
        '''
            The AI detection sensitivity.
        '''
        return self.sensitivity

    def set_sensitivity(self, value):
        '''
            Control the behavior of the AI detection, from 1 to 3:
            1 detects text copied from an AI tool without edits, 2 (the server default) also detects
            text with minor changes, and 3 also detects heavily modified text.

            Parameters:
                value: Integer from 1 to 3.
        '''
        assert isinstance(value, int) and not isinstance(value, bool) and 1 <= value <= 3

        self.sensitivity = value

    def get_explain(self):
        '''
            AI Logic settings.
        '''
        return self.explain

    def set_explain(self, value):
        '''
            AI Logic settings: explain the AI detection with the AI patterns found in the text.

            Parameters:
                value: `AIGeneratedTextExplain`.
        '''
        assert isinstance(value, AIGeneratedTextExplain)

        self.explain = value
