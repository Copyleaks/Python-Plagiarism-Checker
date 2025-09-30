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

import requests
from copyleaks.consts import Consts
from copyleaks.exceptions.command_error import CommandError
from copyleaks.exceptions.under_maintenance_error import UnderMaintenanceError
from copyleaks.helpers.copyleaks_client_helper import CopyleaksClientHelper
from copyleaks.models.ImageDetection.Responses.CopyleaksAiImageDetectionResponseModel import CopyleaksAiImageDetectionResponseModel


class _AiImageDetectionClient:
    @staticmethod
    def __submit(url, auth_token, scan_id, requestModel):
        assert url and scan_id and requestModel

        CopyleaksClientHelper.verify_auth_token(auth_token)

        headers = {
            'Content-Type': 'application/json',
            'User-Agent': Consts.USER_AGENT,
            'Authorization': f"Bearer {auth_token['access_token']}"
        }

        json_data = requestModel.model_dump_json(by_alias=True)
        
        response = requests.post(url, headers=headers, data=json_data)

        if response.ok:
           return CopyleaksAiImageDetectionResponseModel(**response.json())
        elif response.status_code == 503:
            print(f"Error: Service under maintenance (HTTP {response.status_code})")
            print(f"Response: {response.text}")
            raise UnderMaintenanceError()
        else:
            print(f"Error: AI Image Detection request failed (HTTP {response.status_code})")
            print(f"Response: {response.text}")
            raise CommandError(response)
        
    @staticmethod
    def submit(auth_token, scan_id, submission):

        url = f"{Consts.API_SERVER_URI}/v1/ai-image-detector/{scan_id}/check"
        return _AiImageDetectionClient.__submit(url, auth_token, scan_id, submission)
