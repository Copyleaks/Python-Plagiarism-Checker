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
from copyleaks.helpers.copyleaks_multipart import CopyleaksMultipart
from copyleaks.models.ImagePlagiarism.Responses.CopyleaksImagePlagiarismResponseModel import CopyleaksImagePlagiarismResponseModel


class _ImagePlagiarismClient:
    @staticmethod
    def check(auth_token, scan_id, submission, timeout=None):
        '''
            Image Plagiarism Detector: search the web for copies of an image, in one synchronous call.
            The image file is uploaded as multipart/form-data.
            For more info: https://docs.copyleaks.com/reference/actions/image-plagiarism-detector/check

            Parameters:
                auth_token: Your login token to Copyleaks server.
                scan_id: String. A unique scan ID, 3 to 36 characters.
                submission: `CopyleaksImagePlagiarismRequestModel`.

            Raises:
                `CommandError`: Server reject the request. See response status code, headers and content for more info.
                `RateLimitError`: Too many requests. Please wait before calling again.
                `UnderMaintenanceError`: Copyleaks servers are unavailable for maintenance. We recommend to implement exponential backoff algorithm as described here: https://api.copyleaks.com/documentation/v3/exponential-backoff

            Returns:
                `CopyleaksImagePlagiarismResponseModel`.
        '''
        assert scan_id and submission

        CopyleaksClientHelper.verify_auth_token(auth_token)

        url = f"{Consts.API_SERVER_URI}/v1/image-plagiarism-detector/{scan_id}/check"
        fields = {
            'filename': submission.file_name,
            'sandbox': CopyleaksMultipart.bool_field(submission.sandbox),
        }
        if submission.developer_payload is not None:
            fields['developerPayload'] = submission.developer_payload
        files = {'image': CopyleaksMultipart.file_part(submission.file_name, submission.image)}
        response = CopyleaksHttpClient.request('POST', url, headers=CopyleaksClientHelper.headers(auth_token, None),
                                               data=fields, files=files, timeout=timeout)
        return CopyleaksImagePlagiarismResponseModel.model_validate(response.json())
