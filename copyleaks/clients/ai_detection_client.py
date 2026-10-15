from copyleaks.consts import Consts
from copyleaks.helpers.copyleaks_http_client import CopyleaksHttpClient
from copyleaks.models.AiDetection.Responses.CopyleaksAiTextDetectionCreditsResponseModel import CopyleaksAiTextDetectionCreditsResponseModel
from copyleaks.models.AiDetection.Responses.CopyleaksAiTextDetectionResponseModel import CopyleaksAiTextDetectionResponseModel


class _AIDetectionClient:
    @staticmethod
    def submit_natural_language(auth_token, scan_id, submission, timeout=None):
        '''
        Detect AI-written text in a `NaturalLanguageDocument`.
        Returns `CopyleaksAiTextDetectionResponseModel` (dict-style access still works).
        Docs: https://docs.copyleaks.com/reference/actions/writer-detector/check
        '''
        assert scan_id and submission

        url = f"{Consts.API_SERVER_URI}/v2/writer-detector/{scan_id}/check"
        return CopyleaksHttpClient.send('POST', url, auth_token=auth_token, json=submission, timeout=timeout,
                                        response_model=CopyleaksAiTextDetectionResponseModel)

    @staticmethod
    def credits_balance(auth_token, timeout=None):
        '''
        Credit balance of the AI Text Detector wallet, in `credits`. Uses no credits.
        Docs: https://docs.copyleaks.com/reference/actions/writer-detector/credits
        '''
        url = f"{Consts.API_SERVER_URI}/v2/writer-detector/credits"
        return CopyleaksHttpClient.send('GET', url, auth_token=auth_token, timeout=timeout,
                                        response_model=CopyleaksAiTextDetectionCreditsResponseModel)
