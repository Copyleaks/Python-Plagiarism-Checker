
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

from aifc import Error
import requests
from copyleaks.consts import Consts
from copyleaks.helpers.copyleaks_client_helper import CopyleaksClientHelper

class _AIDetectionClient:
    @staticmethod
    def __submit(url, auth_token, scan_id, submission):
        assert url and scan_id and submission

        CopyleaksClientHelper.verify_auth_token(auth_token)

        headers = {
            'Content-Type': 'application/json',
            'User-Agent': Consts.USER_AGENT,
            'Authorization': f"Bearer {auth_token['access_token']}"
        }
        json = submission.toJSON()
        response = requests.post(url, headers=headers, data=json)
        if response.ok:
            return response.json()
        elif response.status_code == 503:
            raise Error()
        else:
            raise Error(response)
        
    @staticmethod
    def submit_natural_language(auth_token, scan_id, submission):
        '''
            Use Copyleaks AI Content Detection to differentiate between human texts and AI written texts.
            This endpoint will receive submitted text to be checked. At the end of the processing stage, 
            the result will be shown as classifications. Text classification is divided into sections. 
            Each section may have a different classification

            Raises:
                `CommandError`: Server reject the request. See response status code, headers and content for more info.
                `UnderMaintenanceError`: Copyleaks servers are unavailable for maintenance. We recommend to implement exponential backoff algorithm as described here: https://api.copyleaks.com/documentation/v3/exponential-backoff
        '''
        url = f"{Consts.API_SERVER_URI}/v2/writer-detector/{scan_id}/check"
        return _AIDetectionClient.__submit(url, auth_token, scan_id, submission)
    

    @staticmethod
    def submit_source_code(auth_token, scan_id, submission):
        '''
            Use Copyleaks AI Content Detection to differentiate between human source code and AI written source code.
            This endpoint will receive submitted source code to be checked. 
            At the end of the processing stage, the result will be shown as classifications. 
            Source code classification is divided into sections. Each section may have a different classification.

            Raises:
                `CommandError`: Server reject the request. See response status code, headers and content for more info.
                `UnderMaintenanceError`: Copyleaks servers are unavailable for maintenance. We recommend to implement exponential backoff algorithm as described here: https://api.copyleaks.com/documentation/v3/exponential-backoff
        '''
        url = f"{Consts.API_SERVER_URI}/v2/writer-detector/source-code/{scan_id}/check"
        return _AIDetectionClient.__submit(url, auth_token, scan_id, submission)
