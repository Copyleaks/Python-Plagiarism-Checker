from copyleaks.consts import Consts
from copyleaks.exceptions.command_error import CommandError
from copyleaks.exceptions.under_maintenance_error import UnderMaintenanceError
from copyleaks.exceptions.rate_limit_error import RateLimitError
from copyleaks.exceptions.auth_expired_error import AuthExipredError
from copyleaks.helpers.copyleaks_client_helper import CopyleaksClientHelper
from copyleaks.helpers.copyleaks_http_client import CopyleaksHttpClient
from copyleaks.clients.ai_detection_client import _AIDetectionClient
from copyleaks.clients.writing_assistant_client import _WritingAssistantClient
from copyleaks.clients.TextModerationClient import _TextModerationClient
from copyleaks.clients.AiImageDetectionClient import _AiImageDetectionClient
from copyleaks.clients.ImagePlagiarismClient import _ImagePlagiarismClient
from copyleaks.clients.AiVideoDetectionClient import _AiVideoDetectionClient
from copyleaks.models.Miscellaneous.Responses.CopyleaksAllowedCrossLanguagesResponseModel import CopyleaksAllowedCrossLanguagesResponseModel
from copyleaks.models.Miscellaneous.Responses.CopyleaksSupportedAiTextDetectionFileTypesResponseModel import CopyleaksSupportedAiTextDetectionFileTypesResponseModel
from copyleaks.models.PrivateCloudHub.Responses.CopyleaksRepositoryInfoResponseModel import CopyleaksRepositoryInfoResponseModel


class Copyleaks(object):
    """
    Copyleaks API client. Calls share one keep-alive `requests.Session`; set timeouts with `set_timeout` or `timeout=`.
    Errors raised by the API calls here and in the `*Client` classes:
        `CommandError`: the request was rejected; `get_response()` has the status code, headers and body.
        `RateLimitError` (HTTP 429, a `CommandError`): `retry_after` is the server's `Retry-After` in seconds.
        `UnderMaintenanceError` (HTTP 503): retry later with exponential backoff.
        `requests.exceptions.Timeout` / `ConnectionError`: network errors.
        `pydantic.ValidationError`: a success response that does not match the typed response model.
    """

    WritingAssistantClient = _WritingAssistantClient
    AiDetectionClient = _AIDetectionClient
    TextModerationClient = _TextModerationClient
    ImageDetectionClient = _AiImageDetectionClient
    ImagePlagiarismClient = _ImagePlagiarismClient
    VideoDetectionClient = _AiVideoDetectionClient

    @staticmethod
    def set_identity_uri(uri):
        '''Override the identity server base URI (default https://id.copyleaks.com).'''
        Consts.IDENTITY_SERVER_URI = uri

    @staticmethod
    def set_api_uri(uri):
        '''Override the API server base URI (default https://api.copyleaks.com).'''
        Consts.API_SERVER_URI = uri

    @staticmethod
    def set_timeout(timeout):
        '''
        Default timeout of every API call: seconds, a (connect, read) tuple, or None. SDK default: (10, 180).
        The read timeout is the longest wait for data from the server, not a limit on the whole call.
        '''
        CopyleaksHttpClient.set_timeout(timeout)

    @staticmethod
    def get_timeout():
        return CopyleaksHttpClient.get_timeout()

    @staticmethod
    def set_session(session):
        '''
        Use your own `requests.Session` (proxies, retries, pool sizes), or None for the SDK default.
        The default session retries only connection errors, never a request that may have reached the server.
        '''
        CopyleaksHttpClient.set_session(session)

    @staticmethod
    def get_session():
        return CopyleaksHttpClient.get_session()

    @staticmethod
    def login(email, key, timeout=None):
        '''
        Log in with the account email and secret key. Returns the auth token, which expires (see `verify_auth_token`).
        Docs: https://docs.copyleaks.com/reference/actions/account/login
        '''

        assert email and key

        url = f"{Consts.IDENTITY_SERVER_URI}/v3/account/login/api"
        return CopyleaksHttpClient.send('POST', url, json={'email': email, 'key': key}, timeout=timeout).json()

    @staticmethod
    def verify_auth_token(auth_token):
        '''Raise `AuthExipredError` when the token has expired or expires within 5 minutes; then log in again.'''
        CopyleaksClientHelper.verify_auth_token(auth_token)

    @staticmethod
    def __submit(url, auth_token, scan_id, submission, timeout):
        assert url and scan_id and submission

        CopyleaksHttpClient.send('PUT', url, auth_token=auth_token, json=submission, timeout=timeout)

    @staticmethod
    def submit_file(auth_token, scan_id, submission, timeout=None):
        '''
        Scan a file: `submission` is a `FileDocument`.
        Docs: https://docs.copyleaks.com/reference/actions/authenticity/submit-file
        '''

        url = f"{Consts.API_SERVER_URI}/v3/scans/submit/file/{scan_id}"
        Copyleaks.__submit(url, auth_token, scan_id, submission, timeout)

    @staticmethod
    def submit_file_ocr(auth_token, scan_id, submission, timeout=None):
        '''
        Scan an image file with OCR: `submission` is an `OcrFileDocument`.
        Docs: https://docs.copyleaks.com/reference/actions/authenticity/submit-ocr
        '''
        url = f"{Consts.API_SERVER_URI}/v3/scans/submit/ocr/{scan_id}"
        Copyleaks.__submit(url, auth_token, scan_id, submission, timeout)

    @staticmethod
    def submit_url(auth_token, scan_id, submission, timeout=None):
        '''
        Scan the content of a URL: `submission` is a `UrlDocument`.
        Docs: https://docs.copyleaks.com/reference/actions/authenticity/submit-url
        '''
        url = f"{Consts.API_SERVER_URI}/v3/scans/submit/url/{scan_id}"
        Copyleaks.__submit(url, auth_token, scan_id, submission, timeout)

    @staticmethod
    def export(auth_token, scan_id, export_id, model, timeout=None):
        '''
        Export the scan's artifacts to your endpoints. `model` is an `Export`; `export_id` is a new ID for this export.
        Docs: https://docs.copyleaks.com/reference/actions/downloads/export
        '''
        assert scan_id and export_id and model

        url = f"{Consts.API_SERVER_URI}/v3/downloads/{scan_id}/export/{export_id}"
        CopyleaksHttpClient.send('POST', url, auth_token=auth_token, json=model, timeout=timeout)

    @staticmethod
    def start(auth_token, model, timeout=None):
        '''
        Start scans submitted with `SubmitAction.CheckCredits`; `model` is a `Start`. Returns success and failure info.
        Docs: https://docs.copyleaks.com/reference/actions/authenticity/start
        '''
        assert model

        url = f"{Consts.API_SERVER_URI}/v3/scans/start"
        return CopyleaksHttpClient.send('PATCH', url, auth_token=auth_token, json=model, timeout=timeout).json()

    @staticmethod
    def delete(auth_token, delete_model, timeout=None):
        '''
        Delete scans: `delete_model` is a `Delete`.
        Docs: https://docs.copyleaks.com/reference/actions/authenticity/delete
        '''
        assert delete_model

        url = f"{Consts.API_SERVER_URI}/v3.1/scans/delete"
        CopyleaksHttpClient.send('PATCH', url, auth_token=auth_token, json=delete_model, timeout=timeout)

    @staticmethod
    def resend_webhook(auth_token, scan_id, timeout=None):
        '''
        Resend the status webhooks of an existing scan.
        Docs: https://docs.copyleaks.com/reference/actions/authenticity/resend-webhook
        '''
        assert scan_id

        url = f"{Consts.API_SERVER_URI}/v3/scans/{scan_id}/webhooks/resend"
        CopyleaksHttpClient.send('POST', url, auth_token=auth_token, content_type='application/json', timeout=timeout)

    @staticmethod
    def credits_balance(auth_token, timeout=None):
        '''
        Remaining credits of the account.
        Docs: https://docs.copyleaks.com/reference/actions/admin/check-credits
        '''
        url = f"{Consts.API_SERVER_URI}/v3/scans/credits"
        return CopyleaksHttpClient.send('GET', url, auth_token=auth_token, timeout=timeout).json()

    @staticmethod
    def usages_history_csv(auth_token, start_date, end_date, timeout=None):
        '''
        Usage history between two dates (`dd-MM-yyyy`), as CSV bytes.
        Docs: https://docs.copyleaks.com/reference/actions/admin/usage-history
        '''
        assert start_date and end_date

        url = f"{Consts.API_SERVER_URI}/v3/scans/usages/history?start={start_date}&end={end_date}"
        return CopyleaksHttpClient.send('GET', url, auth_token=auth_token, content_type='application/json',
                                        timeout=timeout).content

    @staticmethod
    def release_notes(timeout=None):
        '''
        Release notes of the API.
        Docs: https://api.copyleaks.com/documentation/v3/release-notes
        '''

        url = f"{Consts.API_SERVER_URI}/v3/release-logs.json"
        return CopyleaksHttpClient.send('GET', url, timeout=timeout).json()

    @staticmethod
    def supported_file_types(timeout=None):
        '''
        File types supported by plagiarism scans: a dict with `textual` and `ocr` lists. No login needed.
        Docs: https://docs.copyleaks.com/reference/actions/miscellaneous/supported-plagiarism-file-types
        '''

        url = f"{Consts.API_SERVER_URI}/v3/miscellaneous/supported-plagiarism-file-types"
        return CopyleaksHttpClient.send('GET', url, timeout=timeout).json()

    @staticmethod
    def supported_ai_text_detection_file_types(timeout=None):
        '''
        File types supported by AI Text Detection. No login needed.
        Docs: https://docs.copyleaks.com/reference/actions/miscellaneous/supported-ai-text-detection-file-types
        '''

        url = f"{Consts.API_SERVER_URI}/v3/miscellaneous/supported-ai-text-detection-file-types"
        return CopyleaksHttpClient.send('GET', url, timeout=timeout,
                                        response_model=CopyleaksSupportedAiTextDetectionFileTypesResponseModel)

    @staticmethod
    def allowed_cross_languages(timeout=None):
        '''
        Languages for cross-language detection, see `Scanning.set_cross_languages`. No login needed.
        Docs: https://docs.copyleaks.com/reference/actions/miscellaneous/supported-cross-languages
        '''

        url = f"{Consts.API_SERVER_URI}/v3/miscellaneous/allowed-cross-languages"
        return CopyleaksHttpClient.send('GET', url, timeout=timeout,
                                        response_model=CopyleaksAllowedCrossLanguagesResponseModel)

    @staticmethod
    def ocr_supported_langauges(timeout=None):
        '''
        Languages supported by OCR scans (not by the API in general).
        Docs: https://docs.copyleaks.com/reference/actions/miscellaneous/ocr-supported-languages
        '''

        url = f"{Consts.API_SERVER_URI}/v3/miscellaneous/ocr-languages-list"
        return CopyleaksHttpClient.send('GET', url, timeout=timeout).json()

    @staticmethod
    def repository_info(auth_token, repository_id, timeout=None):
        '''
        Info on a Private Cloud Hub repository (ID from the Admin Dashboard). Needs the "Admin" or "Super Admin" role.
        Docs: https://docs.copyleaks.com/reference/actions/private-cloud-hub/info
        '''
        assert repository_id

        url = f"{Consts.API_SERVER_URI}/v3/repositories/repository/{repository_id}/info"
        return CopyleaksHttpClient.send('GET', url, auth_token=auth_token, timeout=timeout,
                                        response_model=CopyleaksRepositoryInfoResponseModel)
