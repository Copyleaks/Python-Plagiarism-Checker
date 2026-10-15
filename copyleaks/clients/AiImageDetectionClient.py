import json

from copyleaks.consts import Consts
from copyleaks.helpers.copyleaks_http_client import CopyleaksHttpClient
from copyleaks.helpers.copyleaks_multipart import CopyleaksMultipart
from copyleaks.models.ImageDetection.Responses.CopyleaksAiImageDetectionResponseModel import CopyleaksAiImageDetectionResponseModel


class _AiImageDetectionClient:
    @staticmethod
    def submit(auth_token, scan_id, submission, timeout=None):
        '''
        Detect AI in a base64 image (`CopyleaksAiImageDetectionRequestModel`). For large images use `submit_file`.
        Returns `CopyleaksAiImageDetectionResponseModel`.
        Docs: https://docs.copyleaks.com/reference/actions/ai-image-detector/check
        '''
        assert scan_id and submission

        url = f"{Consts.API_SERVER_URI}/v1/ai-image-detector/{scan_id}/check"
        return CopyleaksHttpClient.send('POST', url, auth_token=auth_token, json=submission, timeout=timeout,
                                        response_model=CopyleaksAiImageDetectionResponseModel)

    @staticmethod
    def submit_file(auth_token, scan_id, submission, timeout=None):
        '''
        Like `submit`, but uploads the file as multipart/form-data, which is faster and lighter for large images.
        `submission` is a `CopyleaksAiImageDetectionFileRequestModel`.
        Docs: https://docs.copyleaks.com/reference/actions/ai-image-detector/check
        '''
        assert scan_id and submission

        url = f"{Consts.API_SERVER_URI}/v1/ai-image-detector/{scan_id}/check"
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
        return CopyleaksHttpClient.send('POST', url, auth_token=auth_token, form=fields, files=files, timeout=timeout,
                                        response_model=CopyleaksAiImageDetectionResponseModel)

    @staticmethod
    def submit_async(auth_token, scan_id, submission, timeout=None):
        '''
        Detect AI in an image at a URL, asynchronously (`CopyleaksAiImageDetectionAsyncRequestModel`).
        The result is sent to `submission.webhooks.url`, see `CopyleaksAiImageDetectionResponseModel`.
        Docs: https://docs.copyleaks.com/reference/actions/ai-image-detector/submit
        '''
        assert scan_id and submission

        url = f"{Consts.API_SERVER_URI}/v1/ai-image-detector-async/{scan_id}/submit"
        CopyleaksHttpClient.send('PUT', url, auth_token=auth_token, json=submission, timeout=timeout)
