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
        Detect AI in a base64 image (`CopyleaksAiImageDetectionRequestModel`). For large images use `submit_file`.
        Returns `CopyleaksAiImageDetectionResponseModel`.
        Docs: https://docs.copyleaks.com/reference/actions/ai-image-detector/check
        '''
        assert submission
        return _AiImageDetectionClient.__check(auth_token, scan_id, CopyleaksClientHelper.headers(auth_token),
                                               CopyleaksClientHelper.model_to_json_bytes(submission), None, timeout)

    @staticmethod
    def submit_file(auth_token, scan_id, submission, timeout=None):
        '''
        Like `submit`, but uploads the file as multipart/form-data, which is faster and lighter for large images.
        `submission` is a `CopyleaksAiImageDetectionFileRequestModel`.
        Docs: https://docs.copyleaks.com/reference/actions/ai-image-detector/check
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
        Detect AI in an image at a URL, asynchronously (`CopyleaksAiImageDetectionAsyncRequestModel`).
        The result is sent to `submission.webhooks.url`, see `CopyleaksAiImageDetectionResponseModel`.
        Docs: https://docs.copyleaks.com/reference/actions/ai-image-detector/submit
        '''
        assert scan_id and submission

        CopyleaksClientHelper.verify_auth_token(auth_token)

        url = f"{Consts.API_SERVER_URI}/v1/ai-image-detector-async/{scan_id}/submit"
        CopyleaksHttpClient.request('PUT', url, headers=CopyleaksClientHelper.headers(auth_token),
                                    data=CopyleaksClientHelper.model_to_json_bytes(submission), timeout=timeout)
