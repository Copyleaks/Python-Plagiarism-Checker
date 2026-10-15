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
        Grammar, spelling and sentence corrections for a `WritingAssistantDocument`.
        Returns `CopyleaksWritingAssistantResponseModel` (dict-style access still works).
        Docs: https://docs.copyleaks.com/reference/actions/writing-assistant/check
        '''
        url = f"{Consts.API_SERVER_URI}/v1/writing-feedback/{scan_id}/check"
        return _WritingAssistantClient.__submit(url, auth_token, scan_id, submission, timeout)

    @staticmethod
    def get_correction_types(language_code, timeout=None):
        '''
        Correction types (the same for every language), with their texts in the language of `language_code`.
        Docs: https://docs.copyleaks.com/reference/actions/writing-assistant/correction-types
        '''

        url = f"{Consts.API_SERVER_URI}/v1/writing-feedback/correction-types/{language_code}"
        response = CopyleaksHttpClient.request('GET', url, headers=CopyleaksClientHelper.headers(content_type=None),
                                               timeout=timeout)
        return response.json()
