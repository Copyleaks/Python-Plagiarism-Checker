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

from copyleaks.consts import Consts
from copyleaks.helpers.copyleaks_client_helper import CopyleaksClientHelper
from copyleaks.helpers.copyleaks_http_client import CopyleaksHttpClient
from copyleaks.helpers.copyleaks_multipart import CopyleaksMultipart
from copyleaks.models.ImageDetection.Responses.CopyleaksAiImageDetectionResponseModel import CopyleaksAiImageDetectionResponseModel


class _AiImageDetectionClient:
    @staticmethod
    def __check(auth_token, scan_id, headers, data, files, timeout):
        assert scan_id

        CopyleaksClientHelper.verify_auth_token(auth_token)

        url = f"{Consts.API_SERVER_URI}/v1/ai-image-detector/{scan_id}/check"
        response = CopyleaksHttpClient.request('POST', url, headers=headers, data=data, files=files, timeout=timeout)
        return CopyleaksAiImageDetectionResponseModel(**response.json())

    @staticmethod
    def submit(auth_token, scan_id, submission, timeout=None):
        '''
            Detect whether an image is AI-generated or partially AI-generated. The image is sent base64-encoded in JSON.
            For large images, prefer `submit_file`, which uploads the image without base64.
            For more info: https://docs.copyleaks.com/reference/actions/ai-image-detector/check

            Parameters:
                submission: `CopyleaksAiImageDetectionRequestModel`.

            Raises:
                `CommandError`: Server reject the request. See response status code, headers and content for more info.
                `RateLimitError`: Too many requests. Please wait before calling again.
                `UnderMaintenanceError`: Copyleaks servers are unavailable for maintenance. We recommend to implement exponential backoff algorithm as described here: https://api.copyleaks.com/documentation/v3/exponential-backoff

            Returns:
                `CopyleaksAiImageDetectionResponseModel`.
        '''
        assert submission
        return _AiImageDetectionClient.__check(auth_token, scan_id, CopyleaksClientHelper.headers(auth_token),
                                               CopyleaksClientHelper.model_to_json_bytes(submission), None, timeout)

    @staticmethod
    def submit_file(auth_token, scan_id, submission, timeout=None):
        '''
            Detect whether an image is AI-generated or partially AI-generated. The image file is uploaded as
            multipart/form-data, without base64 encoding, which is faster and uses less memory for large images.
            For more info: https://docs.copyleaks.com/reference/actions/ai-image-detector/check

            Parameters:
                submission: `CopyleaksAiImageDetectionFileRequestModel`.

            Raises:
                `CommandError`: Server reject the request. See response status code, headers and content for more info.
                `RateLimitError`: Too many requests. Please wait before calling again.
                `UnderMaintenanceError`: Copyleaks servers are unavailable for maintenance. We recommend to implement exponential backoff algorithm as described here: https://api.copyleaks.com/documentation/v3/exponential-backoff

            Returns:
                `CopyleaksAiImageDetectionResponseModel`.
        '''
        assert submission
        fields = {
            'filename': submission.file_name,
            'model': submission.model,
            'sandbox': CopyleaksMultipart.bool_field(submission.sandbox),
        }
        if submission.mask_type is not None:
            fields['maskType'] = submission.mask_type
        if submission.object_detection is not None:
            fields['objectDetection'] = json.dumps(
                [item.model_dump(by_alias=True) for item in submission.object_detection], separators=(',', ':'))
        files = {'image': CopyleaksMultipart.file_part(submission.file_name, submission.image)}
        return _AiImageDetectionClient.__check(auth_token, scan_id, CopyleaksClientHelper.headers(auth_token, None),
                                               fields, files, timeout)

    @staticmethod
    def submit_async(auth_token, scan_id, submission, timeout=None):
        '''
            Submit an image URL for asynchronous AI Image Detection. The call returns once the request is accepted,
            and the result is sent to `submission.webhooks.url`. Parse the webhook body with
            `CopyleaksAiImageDetectionResponseModel(**request.json)`.
            For more info: https://docs.copyleaks.com/reference/actions/ai-image-detector/submit

            Parameters:
                submission: `CopyleaksAiImageDetectionAsyncRequestModel`.

            Raises:
                `CommandError`: Server reject the request. See response status code, headers and content for more info.
                `RateLimitError`: Too many requests. Please wait before calling again.
                `UnderMaintenanceError`: Copyleaks servers are unavailable for maintenance. We recommend to implement exponential backoff algorithm as described here: https://api.copyleaks.com/documentation/v3/exponential-backoff
        '''
        assert scan_id and submission

        CopyleaksClientHelper.verify_auth_token(auth_token)

        url = f"{Consts.API_SERVER_URI}/v1/ai-image-detector-async/{scan_id}/submit"
        CopyleaksHttpClient.request('PUT', url, headers=CopyleaksClientHelper.headers(auth_token),
                                    data=CopyleaksClientHelper.model_to_json_bytes(submission), timeout=timeout)
