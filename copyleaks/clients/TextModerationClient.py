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

from copyleaks.consts import Consts
from copyleaks.helpers.copyleaks_client_helper import CopyleaksClientHelper
from copyleaks.helpers.copyleaks_http_client import CopyleaksHttpClient
from copyleaks.models.TextModeration.Responses.CopyleaksTextModerationResponseModel import CopyleaksTextModerationResponseModel


class _TextModerationClient:
    @staticmethod
    def __submit_text(url, auth_token, scan_id, requestModel, timeout):
        assert url and scan_id and requestModel

        CopyleaksClientHelper.verify_auth_token(auth_token)

        response = CopyleaksHttpClient.request('POST', url, headers=CopyleaksClientHelper.headers(auth_token),
                                               data=CopyleaksClientHelper.model_to_json_bytes(requestModel),
                                               timeout=timeout)
        return CopyleaksTextModerationResponseModel(**response.json())

    @staticmethod
    def submit_text(auth_token, scan_id, submission, timeout=None):
        '''
            Moderate a text: find unsafe or inappropriate content in the categories (labels) you request.
            For more info: https://docs.copyleaks.com/reference/actions/text-moderation/check

            Parameters:
                submission: `CopyleaksTextModerationRequestModel`.

            Raises:
                `CommandError`: Server reject the request. See response status code, headers and content for more info.
                `RateLimitError`: Too many requests. Please wait before calling again.
                `UnderMaintenanceError`: Copyleaks servers are unavailable for maintenance. We recommend to implement exponential backoff algorithm as described here: https://api.copyleaks.com/documentation/v3/exponential-backoff

            Returns:
                `CopyleaksTextModerationResponseModel`.
        '''

        url = f"{Consts.API_SERVER_URI}/v1/text-moderation/{scan_id}/check"
        return _TextModerationClient.__submit_text(url, auth_token, scan_id, submission, timeout)
