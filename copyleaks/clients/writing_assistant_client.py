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
from copyleaks.models.WritingAssistant.Responses.CopyleaksWritingAssistantResponseModel import CopyleaksWritingAssistantResponseModel


class _WritingAssistantClient:
    @staticmethod
    def __submit(url, auth_token, scan_id, submission, timeout):
        assert url and scan_id and submission

        CopyleaksClientHelper.verify_auth_token(auth_token)

        response = CopyleaksHttpClient.request('POST', url, headers=CopyleaksClientHelper.headers(auth_token),
                                               data=CopyleaksClientHelper.to_json_bytes(submission), timeout=timeout)
        return CopyleaksWritingAssistantResponseModel(**response.json())

    @staticmethod
    def submit_text(auth_token, scan_id, submission, timeout=None):
        '''
            Use Copyleaks Writing Assistant to generate grammar, spelling and sentence corrections for a given text.
            This endpoint will receive submitted text to be checked. The response will show the suggested corrections to the input text.
            For more info: https://docs.copyleaks.com/reference/actions/writing-assistant/check

            Raises:
                `CommandError`: Server reject the request. See response status code, headers and content for more info.
                `RateLimitError`: Too many requests. Please wait before calling again.
                `UnderMaintenanceError`: Copyleaks servers are unavailable for maintenance. We recommend to implement exponential backoff algorithm as described here: https://api.copyleaks.com/documentation/v3/exponential-backoff
                `pydantic.ValidationError`: The server returned a success response whose body does not match the response model.

            Returns:
                `CopyleaksWritingAssistantResponseModel`. Dict-style access (`response['score']['corrections']['overallScore']`) still works for backward compatibility.
        '''
        url = f"{Consts.API_SERVER_URI}/v1/writing-feedback/{scan_id}/check"
        return _WritingAssistantClient.__submit(url, auth_token, scan_id, submission, timeout)

    @staticmethod
    def get_correction_types(language_code, timeout=None):
        '''
            Get a list of correction types supported within the Writing Assistant API.
            Correction types apply to all supported languages.
            The supplied language code for this request is used to determine the language of the texts returned.
            For more info: https://docs.copyleaks.com/reference/actions/writing-assistant/correction-types

            Raises:
                `CommandError`: Server reject the request. See response status code, headers and content for more info.
                `UnderMaintenanceError`: Copyleaks servers are unavailable for maintenance. We recommend to implement exponential backoff algorithm as described here: https://api.copyleaks.com/documentation/v3/exponential-backoff

            Returns:
                List of supported correction types.
        '''

        url = f"{Consts.API_SERVER_URI}/v1/writing-feedback/correction-types/{language_code}"
        response = CopyleaksHttpClient.request('GET', url, headers=CopyleaksClientHelper.headers(content_type=None),
                                               timeout=timeout)
        return response.json()
