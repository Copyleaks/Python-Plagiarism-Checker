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

class Overview:
    '''
        Gen-AI Overview: extract key insights from the scan data.
        Unset options use the server default (False).
    '''

    @staticmethod
    def _check(value):
        if not isinstance(value, bool):
            raise TypeError('value must be True or False')
        return value

    def get_enable(self):
        return self.enable

    def set_enable(self, value):
        '''
            Enable the Gen-AI Overview for the scan.

            Parameters:
                value: Boolean.
        '''
        self.enable = self._check(value)

    def get_ignore_ai_detection(self):
        return self.ignoreAIDetection

    def set_ignore_ai_detection(self, value):
        '''
            Ignore AI detection when generating the overview.

            Parameters:
                value: Boolean.
        '''
        self.ignoreAIDetection = self._check(value)

    def get_ignore_plagiarism_detection(self):
        return self.ignorePlagiarismDetection

    def set_ignore_plagiarism_detection(self, value):
        '''
            Ignore plagiarism detection when generating the overview.

            Parameters:
                value: Boolean.
        '''
        self.ignorePlagiarismDetection = self._check(value)

    def get_ignore_writing_feedback(self):
        return self.ignoreWritingFeedback

    def set_ignore_writing_feedback(self, value):
        '''
            Ignore the Grammar Checker when generating the overview.

            Parameters:
                value: Boolean.
        '''
        self.ignoreWritingFeedback = self._check(value)

    def get_ignore_author_data(self):
        return self.ignoreAuthorData

    def set_ignore_author_data(self, value):
        '''
            Ignore the author's historical data when generating the overview.

            Parameters:
                value: Boolean.
        '''
        self.ignoreAuthorData = self._check(value)
