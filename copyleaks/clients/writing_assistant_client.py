from copyleaks.consts import Consts
from copyleaks.helpers.copyleaks_http_client import CopyleaksHttpClient
from copyleaks.models.WritingAssistant.Responses.CopyleaksWritingAssistantResponseModel import CopyleaksWritingAssistantResponseModel


class _WritingAssistantClient:
    @staticmethod
    def submit_text(auth_token, scan_id, submission, timeout=None):
        '''
        Grammar, spelling and sentence corrections for a `WritingAssistantDocument`.
        Returns `CopyleaksWritingAssistantResponseModel` (dict-style access still works).
        Docs: https://docs.copyleaks.com/reference/actions/writing-assistant/check
        '''
        assert scan_id and submission

        url = f"{Consts.API_SERVER_URI}/v1/writing-feedback/{scan_id}/check"
        return CopyleaksHttpClient.send('POST', url, auth_token=auth_token, json=submission, timeout=timeout,
                                        response_model=CopyleaksWritingAssistantResponseModel)

    @staticmethod
    def get_correction_types(language_code, timeout=None):
        '''
        Correction types (the same for every language), with their texts in the language of `language_code`.
        Docs: https://docs.copyleaks.com/reference/actions/writing-assistant/correction-types
        '''

        url = f"{Consts.API_SERVER_URI}/v1/writing-feedback/correction-types/{language_code}"
        return CopyleaksHttpClient.send('GET', url, timeout=timeout).json()
