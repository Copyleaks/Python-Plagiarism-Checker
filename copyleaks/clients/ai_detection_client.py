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
        Detect AI-written text in a `NaturalLanguageDocument`.
        Returns `CopyleaksAiTextDetectionResponseModel` (dict-style access still works).
        Docs: https://docs.copyleaks.com/reference/actions/writer-detector/check
        '''
        url = f"{Consts.API_SERVER_URI}/v2/writer-detector/{scan_id}/check"
        return _AIDetectionClient.__submit(url, auth_token, scan_id, submission, timeout)

    @staticmethod
    def credits_balance(auth_token, timeout=None):
        '''
        Credit balance of the AI Text Detector wallet, in `credits`. Uses no credits.
        Docs: https://docs.copyleaks.com/reference/actions/writer-detector/credits
        '''
        CopyleaksClientHelper.verify_auth_token(auth_token)

        url = f"{Consts.API_SERVER_URI}/v2/writer-detector/credits"
        response = CopyleaksHttpClient.request('GET', url, headers=CopyleaksClientHelper.headers(auth_token, None),
                                               timeout=timeout)
        return CopyleaksAiTextDetectionCreditsResponseModel.model_validate(response.json())
