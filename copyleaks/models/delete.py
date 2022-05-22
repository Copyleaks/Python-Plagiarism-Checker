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

import json
from xmlrpc.client import Boolean


class Delete:
    def get_scans(self):
        '''
            Scans to delete list.
        '''
        return self.scans

    def set_scans(self, value):
        '''
            Scans to delete list.

            Parameters: 
                value: `DeleteScan` list.
        '''

        assert value

        self.scans = value

    def get_purge(self):
        '''
            Delete all trace of the scan from Copyleaks server, including from internal database. A purged process will not be available as a result for previous scans.
        '''
        return self.scans

    def set_purge(self, value):
        '''
            Delete all trace of the scan from Copyleaks server, including from internal database. A purged process will not be available as a result for previous scans.

            Parameters: 
                value: Boolean.
        '''

        assert value != None and type(value) is Boolean 

        self.purge = value

    def get_completion_webhook(self):
        '''
            Allows you to register to a webhook that will be fired once the removal has been completed.
            Make sure that your endpoint is listening to a POST method (no body parameters were supplied).
        '''
        return self.completionWebhook

    def set_completion_webhook(self, value):
        '''
            Allows you to register to a webhook that will be fired once the removal has been completed.
            Make sure that your endpoint is listening to a POST method (no body parameters were supplied).

            Parameters: 
                value: String (uri).
        '''

        assert value

        self.completionWebhook = value

    def toJSON(self):
        return json.dumps(self, default=lambda o: o.__dict__,
                          sort_keys=True, indent=4)


class DeleteScan:
    def __init__(self, id):
        self.set_id(id)

    def get_id(self):
        '''
            Scan Id
        '''
        return self.id

    def set_id(self, value):
        '''
            Scan Id

            Parameters: 
                value: String.
        '''

        assert value

        self.id = value
