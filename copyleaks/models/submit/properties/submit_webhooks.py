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


class SubmitWebhooks:
    def get_new_result(self):
        '''
            Get the HTTP new result webhook URL.
        '''
        return self.newResult

    def set_new_result(self, value):
        '''
            Set the HTTP endpoint to be triggered while the scan is still running and a new result is found.

            Parameters: 
                value: string(url).
        '''
        assert value

        self.newResult = value

    def get_status(self):
        '''
            Get the scan status changed webhook URL.
        '''

        return self.status

    def set_status(self, value):
        '''
            Set the webhook event that triggered once the scan status changes.

            Parameters: 
                value: string(url).
        '''
        assert value

        self.status = value
