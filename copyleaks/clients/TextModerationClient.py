from copyleaks.consts import Consts
from copyleaks.helpers.copyleaks_http_client import CopyleaksHttpClient
from copyleaks.models.TextModeration.Responses.CopyleaksTextModerationResponseModel import CopyleaksTextModerationResponseModel


class _TextModerationClient:
    @staticmethod
    def submit_text(auth_token, scan_id, submission, timeout=None):
        '''
        Find unsafe content in the requested categories (`CopyleaksTextModerationRequestModel`).
        Returns `CopyleaksTextModerationResponseModel`.
        Docs: https://docs.copyleaks.com/reference/actions/text-moderation/check
        '''
        assert scan_id and submission

        url = f"{Consts.API_SERVER_URI}/v1/text-moderation/{scan_id}/check"
        return CopyleaksHttpClient.send('POST', url, auth_token=auth_token, json=submission, timeout=timeout,
                                        response_model=CopyleaksTextModerationResponseModel)
