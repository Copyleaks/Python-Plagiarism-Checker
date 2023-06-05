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


class Repository:
    def get_id(self):
        '''
            Id of a repository to scan the submitted document against.
        '''
        return self.id

    def set_id(self, value):
        '''
            Id of a repository to scan the submitted document against.

            Parameters:
                value: String.
        '''
        assert value

        self.id = value


class SearchRepository(Repository):
    def get_include_my_submissions(self):
        '''
            Compare the scanned document against MY submittions in the repository.
        '''
        return self.includeMySubmissions

    def set_include_my_submissions(self, value):
        '''
            Compare the scanned document against MY submittions in the repository.

            Parameters: 
                value: Boolean.
        '''
        assert value

        self.includeMySubmissions = value

    def get_include_others_submissions(self):
        '''
            Compare the scanned document against OTHER users submittions in the repository.
        '''
        return self.includeOthersSubmissions

    def set_include_others_submissions(self, value):
        '''
            Compare the scanned document against OTHER users submittions in the repository.

            Parameters: 
                value: Boolean.
        '''
        assert value

        self.includeOthersSubmissions = value

class IndexingRepository(Repository):
    def get_masking_policy(self):
        '''
            Get the masking policy
        '''
        return self.maskingPolicy

    def set_masking_policy(self, value):

        '''
            allows to specify a document masking policy on the document level.

            If the repo has it's own masking policy, the stricter policy will be applied to results from this document.

            value: `MaskingPolicy` enum
        '''
        assert value

        self.maskingPolicy = value
