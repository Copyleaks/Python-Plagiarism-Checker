from copyleaks.consts import Consts
from copyleaks.helpers.copyleaks_http_client import CopyleaksHttpClient


class _AiVideoDetectionClient:
    @staticmethod
    def submit(auth_token, scan_id, submission, timeout=None):
        '''
        Detect AI in a video at a URL (`CopyleaksAiVideoDetectionRequestModel`); `scan_id` is 3 to 36 characters.
        The result is sent to `submission.webhooks.url`, see `CopyleaksAiVideoDetectionResponseModel`.
        Docs: https://docs.copyleaks.com/reference/actions/ai-video-detector/submit
        '''
        assert scan_id and submission

        url = f"{Consts.API_SERVER_URI}/v1/ai-video-detector/{scan_id}/submit"
        CopyleaksHttpClient.send('POST', url, auth_token=auth_token, json=submission, timeout=timeout)
