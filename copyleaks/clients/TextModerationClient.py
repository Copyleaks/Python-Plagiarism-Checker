from copyleaks.consts import Consts
from copyleaks.helpers.copyleaks_client_helper import CopyleaksClientHelper
from copyleaks.helpers.copyleaks_http_client import CopyleaksHttpClient
from copyleaks.models.TextModeration.Responses.CopyleaksTextModerationResponseModel import CopyleaksTextModerationResponseModel


class _TextModerationClient:
    @staticmethod
    def __submit_text(url, auth_token, scan_id, requestModel, timeout):
        assert url and scan_id and requestModel

        CopyleaksClientHelper.verify_auth_token(auth_token)

        response = CopyleaksHttpClient.request('POST', url, headers=CopyleaksClientHelper.headers(auth_token),
                                               data=CopyleaksClientHelper.model_to_json_bytes(requestModel),
                                               timeout=timeout)
        return CopyleaksTextModerationResponseModel(**response.json())

    @staticmethod
    def submit_text(auth_token, scan_id, submission, timeout=None):
        '''
        Find unsafe content in the requested categories (`CopyleaksTextModerationRequestModel`).
        Returns `CopyleaksTextModerationResponseModel`.
        Docs: https://docs.copyleaks.com/reference/actions/text-moderation/check
        '''

        url = f"{Consts.API_SERVER_URI}/v1/text-moderation/{scan_id}/check"
        return _TextModerationClient.__submit_text(url, auth_token, scan_id, submission, timeout)
