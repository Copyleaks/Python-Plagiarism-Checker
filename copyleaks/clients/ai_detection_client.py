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
from copyleaks.models.AiDetection.Responses.CopyleaksAiTextDetectionCreditsResponseModel import CopyleaksAiTextDetectionCreditsResponseModel
from copyleaks.models.AiDetection.Responses.CopyleaksAiTextDetectionResponseModel import CopyleaksAiTextDetectionResponseModel


class _AIDetectionClient:
    @staticmethod
    def __submit(url, auth_token, scan_id, submission, timeout):
        assert url and scan_id and submission

        CopyleaksClientHelper.verify_auth_token(auth_token)

        response = CopyleaksHttpClient.request('POST', url, headers=CopyleaksClientHelper.headers(auth_token),
                                               data=CopyleaksClientHelper.to_json_bytes(submission), timeout=timeout)
        return CopyleaksAiTextDetectionResponseModel(**response.json())

    @staticmethod
    def submit_natural_language(auth_token, scan_id, submission, timeout=None):
        '''
            Use Copyleaks AI Content Detection to differentiate between human texts and AI written texts.
            This endpoint will receive submitted text to be checked. At the end of the processing stage,
            the result will be shown as classifications. Text classification is divided into sections.
            Each section may have a different classification
            For more info: https://docs.copyleaks.com/reference/actions/writer-detector/check

            Parameters:
                submission: `NaturalLanguageDocument`. Set `explain` to get AI Logic and `sensitivity` (1-3) to tune the detection.

            Raises:
                `CommandError`: Server reject the request. See response status code, headers and content for more info.
                `RateLimitError`: Too many requests. Please wait before calling again.
                `UnderMaintenanceError`: Copyleaks servers are unavailable for maintenance. We recommend to implement exponential backoff algorithm as described here: https://api.copyleaks.com/documentation/v3/exponential-backoff
                `pydantic.ValidationError`: The server returned a success response whose body does not match the response model.

            Returns:
                `CopyleaksAiTextDetectionResponseModel`. Dict-style access (`response['summary']['ai']`) still works for backward compatibility.
        '''
        url = f"{Consts.API_SERVER_URI}/v2/writer-detector/{scan_id}/check"
        return _AIDetectionClient.__submit(url, auth_token, scan_id, submission, timeout)

    @staticmethod
    def credits_balance(auth_token, timeout=None):
        '''
            Get the credit balance of the AI Text Detector wallet. Read-only: it uses no credits.
            For more info: https://docs.copyleaks.com/reference/actions/writer-detector/credits

            Raises:
                `CommandError`: Server reject the request. See response status code, headers and content for more info.
                `RateLimitError`: Too many requests. Please wait before calling again.
                `UnderMaintenanceError`: Copyleaks servers are unavailable for maintenance. We recommend to implement exponential backoff algorithm as described here: https://api.copyleaks.com/documentation/v3/exponential-backoff

            Returns:
                `CopyleaksAiTextDetectionCreditsResponseModel`, with the balance in `credits`.
        '''
        CopyleaksClientHelper.verify_auth_token(auth_token)

        url = f"{Consts.API_SERVER_URI}/v2/writer-detector/credits"
        response = CopyleaksHttpClient.request('GET', url, headers=CopyleaksClientHelper.headers(auth_token, None),
                                               timeout=timeout)
        return CopyleaksAiTextDetectionCreditsResponseModel.model_validate(response.json())
