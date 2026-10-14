'''
 The MIT License(MIT)
 
 Copyright(c) 2016 Copyleaks LTD (https://copyleaks.com)
 
 Permission is hereby granted, free of charge, to any person obtaining a copy
 of this software and associated documentation files (the "Software"), to deal
 in the Software without restriction, including without limitation the rights
 to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
 copies of the Software, and to permit persons to whom the Software is
 furnished to do so, subject to the following conditions:
 
 The above copyright notice and this permission notice shall be included in all
 copies or substantial portions of the Software.
 
 THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
 IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
 FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
 AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
 LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
 OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
 SOFTWARE.
'''

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
    Copyleaks API client.

    Every call goes through one shared `requests.Session`, so connections are kept alive and reused,
    and every call has a timeout (see `set_timeout`). Each method that calls the API also accepts
    `timeout=`: seconds, or a (connect, read) tuple, for that call only.

    Errors raised by the API calls:
        `CommandError`: the server rejected the request. `get_response()` has the status code, headers and body.
        `RateLimitError`: too many requests (HTTP 429). `retry_after` has the server's `Retry-After` in seconds.
        `UnderMaintenanceError`: Copyleaks servers are unavailable for maintenance (HTTP 503).
        `requests.exceptions.Timeout` and `requests.exceptions.ConnectionError`: network errors.
    """

    WritingAssistantClient = _WritingAssistantClient
    AiDetectionClient = _AIDetectionClient
    TextModerationClient = _TextModerationClient
    ImageDetectionClient = _AiImageDetectionClient
    ImagePlagiarismClient = _ImagePlagiarismClient
    VideoDetectionClient = _AiVideoDetectionClient

    @staticmethod
    def set_identity_uri(uri):
        '''
            Set the Identity server URI.

            Parameters:
                uri: string.
        '''
        Consts.IDENTITY_SERVER_URI = uri

    @staticmethod
    def set_api_uri(uri):
        '''
            Set the API server URI.

            Parameters:
                uri: string.
        '''
        Consts.API_SERVER_URI = uri

    @staticmethod
    def set_timeout(timeout):
        '''
            Set the default timeout of every API call.
            The SDK default is 10 seconds to connect and 180 seconds to read the response.

            Parameters:
                timeout: seconds as a number, a (connect, read) tuple, or None for no timeout.
        '''
        CopyleaksHttpClient.set_timeout(timeout)

    @staticmethod
    def get_timeout():
        '''
            The default timeout of every API call: seconds, a (connect, read) tuple, or None.
        '''
        return CopyleaksHttpClient.get_timeout()

    @staticmethod
    def set_session(session):
        '''
            Send every API call through your own `requests.Session`, for example to set proxies,
            retries or connection pool sizes. Pass None to go back to the SDK's default session.

            The default session keeps connections alive. It retries only connection errors,
            never a request that may have reached the server.
        '''
        CopyleaksHttpClient.set_session(session)

    @staticmethod
    def get_session():
        '''
            The `requests.Session` used for every API call.
        '''
        return CopyleaksHttpClient.get_session()

    @staticmethod
    def login(email, key, timeout=None):
        '''
            Login to Copyleaks authentication server.
            For more info: https://docs.copyleaks.com/reference/actions/account/login

            Parameters:
                email: string. Copyleaks account email address.
                key: string. Copyleaks account secret key.

            Raises:
                `CommandError`: Server reject the request. See response status code, headers and content for more info.
                `RateLimitError`: Too many login attempts. Please wait before calling again.
                `UnderMaintenanceError`: Copyleaks servers are unavailable for maintenance. We recommend to implement exponential backoff algorithm as described here: https://api.copyleaks.com/documentation/v3/exponential-backoff

            Returns:
                A authentication token that being expired after certain amount of time.
        '''

        assert email and key

        url = f"{Consts.IDENTITY_SERVER_URI}/v3/account/login/api"
        payload = {
            'email': email,
            'key': key
        }

        response = CopyleaksHttpClient.request('POST', url, headers=CopyleaksClientHelper.headers(),
                                               data=CopyleaksClientHelper.to_json(payload).encode('utf-8'),
                                               timeout=timeout)
        return response.json()

    @staticmethod
    def verify_auth_token(auth_token):
        '''
            Verify that Copyleaks authentication token is exists and not expired.

            Parameters:
                auth_token: Copyleaks authentication token

            Raises:
                `AuthExipredError`: authentication expired. Need to login again.
        '''
        CopyleaksClientHelper.verify_auth_token(auth_token)

    @staticmethod
    def __submit(url, auth_token, scan_id, submission, timeout):
        assert url and scan_id and submission

        Copyleaks.verify_auth_token(auth_token)

        CopyleaksHttpClient.request('PUT', url, headers=CopyleaksClientHelper.headers(auth_token),
                                    data=CopyleaksClientHelper.to_json_bytes(submission), timeout=timeout)

    @staticmethod
    def submit_file(auth_token, scan_id, submission, timeout=None):
        '''
            Starting a new process by providing a file to scan.
            For more info:
            https://docs.copyleaks.com/reference/actions/authenticity/submit-file

            Raises:
                `CommandError`: Server reject the request. See response status code, headers and content for more info.
                `RateLimitError`: Too many requests. Please wait before calling again.
                `UnderMaintenanceError`: Copyleaks servers are unavailable for maintenance. We recommend to implement exponential backoff algorithm as described here: https://api.copyleaks.com/documentation/v3/exponential-backoff
        '''

        url = f"{Consts.API_SERVER_URI}/v3/scans/submit/file/{scan_id}"
        Copyleaks.__submit(url, auth_token, scan_id, submission, timeout)

    @staticmethod
    def submit_file_ocr(auth_token, scan_id, submission, timeout=None):
        '''
            Starting a new process by providing a OCR image file to scan.
            For more info:
            https://docs.copyleaks.com/reference/actions/authenticity/submit-ocr

            Raises:
                `CommandError`: Server reject the request. See response status code, headers and content for more info.
                `RateLimitError`: Too many requests. Please wait before calling again.
                `UnderMaintenanceError`: Copyleaks servers are unavailable for maintenance. We recommend to implement exponential backoff algorithm as described here: https://api.copyleaks.com/documentation/v3/exponential-backoff
        '''
        url = f"{Consts.API_SERVER_URI}/v3/scans/submit/ocr/{scan_id}"
        Copyleaks.__submit(url, auth_token, scan_id, submission, timeout)

    @staticmethod
    def submit_url(auth_token, scan_id, submission, timeout=None):
        '''
            Starting a new process by providing a URL to scan.
            For more info:
            https://docs.copyleaks.com/reference/actions/authenticity/submit-url

            Raises:
                `CommandError`: Server reject the request. See response status code, headers and content for more info.
                `RateLimitError`: Too many requests. Please wait before calling again.
                `UnderMaintenanceError`: Copyleaks servers are unavailable for maintenance. We recommend to implement exponential backoff algorithm as described here: https://api.copyleaks.com/documentation/v3/exponential-backoff
        '''
        url = f"{Consts.API_SERVER_URI}/v3/scans/submit/url/{scan_id}"
        Copyleaks.__submit(url, auth_token, scan_id, submission, timeout)

    @staticmethod
    def export(auth_token, scan_id, export_id, model, timeout=None):
        '''
            Exporting scans artifact into your server.
            For more info:
            https://docs.copyleaks.com/reference/actions/downloads/export

            Parameters:
                auth_token: Your login token to Copyleaks server.
                scan_id: String. The scan ID of the specific scan to export.
                export_id: String. A new Id for the export process.
                model: `Export`. Request of which artifact should be exported.

            Raises:
                `CommandError`: Server reject the request. See response status code, headers and content for more info.
                `RateLimitError`: Too many requests. Please wait before calling again.
                `UnderMaintenanceError`: Copyleaks servers are unavailable for maintenance. We recommend to implement exponential backoff algorithm as described here: https://api.copyleaks.com/documentation/v3/exponential-backoff
        '''
        assert scan_id and export_id and model

        Copyleaks.verify_auth_token(auth_token)

        url = f"{Consts.API_SERVER_URI}/v3/downloads/{scan_id}/export/{export_id}"

        CopyleaksHttpClient.request('POST', url, headers=CopyleaksClientHelper.headers(auth_token),
                                    data=CopyleaksClientHelper.to_json_bytes(model), timeout=timeout)

    @staticmethod
    def start(auth_token, model, timeout=None):
        '''
            Start scanning all the files you submitted for a price-check.
            For more info:
            https://docs.copyleaks.com/reference/actions/authenticity/start

            Parameters:
                auth_token: Your login token to Copyleaks server.
                model: `Start` object. Include information about which scans should be started.

            Raises:
                `CommandError`: Server reject the request. See response status code, headers and content for more info.
                `RateLimitError`: Too many requests. Please wait before calling again.
                `UnderMaintenanceError`: Copyleaks servers are unavailable for maintenance. We recommend to implement exponential backoff algorithm as described here: https://api.copyleaks.com/documentation/v3/exponential-backoff

            Returns:
                Server response including success/failed info.
        '''
        assert model

        Copyleaks.verify_auth_token(auth_token)

        url = f"{Consts.API_SERVER_URI}/v3/scans/start"

        response = CopyleaksHttpClient.request('PATCH', url, headers=CopyleaksClientHelper.headers(auth_token),
                                               data=CopyleaksClientHelper.to_json_bytes(model), timeout=timeout)
        return response.json()  # Completed successfully

    @staticmethod
    def delete(auth_token, delete_model, timeout=None):
        '''
            Delete the specific process from the server.
            For more info:
            https://docs.copyleaks.com/reference/actions/authenticity/delete

            Raises:
                `CommandError`: Server reject the request. See response status code, headers and content for more info.
                `RateLimitError`: Too many requests. Please wait before calling again.
                `UnderMaintenanceError`: Copyleaks servers are unavailable for maintenance. We recommend to implement exponential backoff algorithm as described here: https://api.copyleaks.com/documentation/v3/exponential-backoff
        '''
        assert delete_model

        Copyleaks.verify_auth_token(auth_token)

        url = f"{Consts.API_SERVER_URI}/v3.1/scans/delete"

        CopyleaksHttpClient.request('PATCH', url, headers=CopyleaksClientHelper.headers(auth_token),
                                    data=CopyleaksClientHelper.to_json_bytes(delete_model), timeout=timeout)

    @staticmethod
    def resend_webhook(auth_token, scan_id, timeout=None):
        '''
            Resend status webhooks for existing scans.
            For more info:
            https://docs.copyleaks.com/reference/actions/authenticity/resend-webhook

            Raises:
                `CommandError`: Server reject the request. See response status code, headers and content for more info.
                `RateLimitError`: Too many requests. Please wait before calling again.
                `UnderMaintenanceError`: Copyleaks servers are unavailable for maintenance. We recommend to implement exponential backoff algorithm as described here: https://api.copyleaks.com/documentation/v3/exponential-backoff
        '''
        assert scan_id

        Copyleaks.verify_auth_token(auth_token)

        url = f"{Consts.API_SERVER_URI}/v3/scans/{scan_id}/webhooks/resend"

        CopyleaksHttpClient.request('POST', url, headers=CopyleaksClientHelper.headers(auth_token), timeout=timeout)

    @staticmethod
    def credits_balance(auth_token, timeout=None):
        '''
            Get current credits balance for the Copyleaks account
            For more info:
            https://docs.copyleaks.com/reference/actions/admin/check-credits

            Raises:
                `CommandError`: Server reject the request. See response status code, headers and content for more info.
                `UnderMaintenanceError`: Copyleaks servers are unavailable for maintenance. We recommend to implement exponential backoff algorithm as described here: https://api.copyleaks.com/documentation/v3/exponential-backoff
                `RateLimitError`: Too many requests. Please wait before calling again.

            Returns:
                Number of remaining credits on the account.
        '''
        Copyleaks.verify_auth_token(auth_token)

        url = f"{Consts.API_SERVER_URI}/v3/scans/credits"

        response = CopyleaksHttpClient.request('GET', url, headers=CopyleaksClientHelper.headers(auth_token, None),
                                               timeout=timeout)
        return response.json()

    @staticmethod
    def usages_history_csv(auth_token, start_date, end_date, timeout=None):
        '''
            This endpoint allows you to export your usage history between two dates.
            The output results will be exported to a csv file and it will be attached to the response.
            For more info:
            https://docs.copyleaks.com/reference/actions/admin/usage-history

            Parameters:
                auth_token: Your login token to Copyleaks server.
                start_date: String. The start date to collect usage history from. Date Format: `dd-MM-yyyy`
                end_date: String. The end date to collect usage history from. Date Format: `dd-MM-yyyy`

            Raises:
                `CommandError`: Server reject the request. See response status code, headers and content for more info.
                `UnderMaintenanceError`: Copyleaks servers are unavailable for maintenance. We recommend to implement exponential backoff algorithm as described here: https://api.copyleaks.com/documentation/v3/exponential-backoff
                `RateLimitError`: Too many requests. Please wait before calling again.

            Returns:
                The CSV file content, as bytes.
        '''
        assert start_date and end_date

        Copyleaks.verify_auth_token(auth_token)

        url = f"{Consts.API_SERVER_URI}/v3/scans/usages/history?start={start_date}&end={end_date}"

        response = CopyleaksHttpClient.request('GET', url, headers=CopyleaksClientHelper.headers(auth_token),
                                               timeout=timeout)
        return response.content  # Completed successfully

    @staticmethod
    def release_notes(timeout=None):
        '''
            Get updates about copyleaks api release notes
            For more info: https://api.copyleaks.com/documentation/v3/release-notes

            Raises:
                `CommandError`: Server reject the request. See response status code, headers and content for more info.
                `UnderMaintenanceError`: Copyleaks servers are unavailable for maintenance. We recommend to implement exponential backoff algorithm as described here: https://api.copyleaks.com/documentation/v3/exponential-backoff

            Returns:
                List of release notes.
        '''

        url = f"{Consts.API_SERVER_URI}/v3/release-logs.json"
        response = CopyleaksHttpClient.request('GET', url, headers=CopyleaksClientHelper.headers(content_type=None),
                                               timeout=timeout)
        return response.json()

    @staticmethod
    def supported_file_types(timeout=None):
        '''
            Get the file types supported by plagiarism scans. Public: no login needed.
            For more info: https://docs.copyleaks.com/reference/actions/miscellaneous/supported-plagiarism-file-types

            Raises:
                `CommandError`: Server reject the request. See response status code, headers and content for more info.
                `UnderMaintenanceError`: Copyleaks servers are unavailable for maintenance. We recommend to implement exponential backoff algorithm as described here: https://api.copyleaks.com/documentation/v3/exponential-backoff

            Returns:
                Dict with the `textual` and `ocr` lists of supported file types.
        '''

        url = f"{Consts.API_SERVER_URI}/v3/miscellaneous/supported-plagiarism-file-types"
        response = CopyleaksHttpClient.request('GET', url, headers=CopyleaksClientHelper.headers(content_type=None),
                                               timeout=timeout)
        return response.json()

    @staticmethod
    def supported_ai_text_detection_file_types(timeout=None):
        '''
            Get the file types supported by AI Text Detection. Public: no login needed.
            For more info: https://docs.copyleaks.com/reference/actions/miscellaneous/supported-ai-text-detection-file-types

            Raises:
                `CommandError`: Server reject the request. See response status code, headers and content for more info.
                `UnderMaintenanceError`: Copyleaks servers are unavailable for maintenance. We recommend to implement exponential backoff algorithm as described here: https://api.copyleaks.com/documentation/v3/exponential-backoff

            Returns:
                `CopyleaksSupportedAiTextDetectionFileTypesResponseModel`, with the list in `supported_ai_file_types`.
        '''

        url = f"{Consts.API_SERVER_URI}/v3/miscellaneous/supported-ai-text-detection-file-types"
        response = CopyleaksHttpClient.request('GET', url, headers=CopyleaksClientHelper.headers(content_type=None),
                                               timeout=timeout)
        return CopyleaksSupportedAiTextDetectionFileTypesResponseModel.model_validate(response.json())

    @staticmethod
    def allowed_cross_languages(timeout=None):
        '''
            Get the languages supported by cross-language plagiarism detection, as ISO-639-1 codes.
            Use them with `Scanning.set_cross_languages`. Public: no login needed.
            For more info: https://docs.copyleaks.com/reference/actions/miscellaneous/supported-cross-languages

            Raises:
                `CommandError`: Server reject the request. See response status code, headers and content for more info.
                `UnderMaintenanceError`: Copyleaks servers are unavailable for maintenance. We recommend to implement exponential backoff algorithm as described here: https://api.copyleaks.com/documentation/v3/exponential-backoff

            Returns:
                `CopyleaksAllowedCrossLanguagesResponseModel`, with `document_languages` (supported languages of the
                scanned document) and `result_languages` (languages you can scan against), each a dict of
                language name to code. `document_language_codes` and `result_language_codes` list the codes.
        '''

        url = f"{Consts.API_SERVER_URI}/v3/miscellaneous/allowed-cross-languages"
        response = CopyleaksHttpClient.request('GET', url, headers=CopyleaksClientHelper.headers(content_type=None),
                                               timeout=timeout)
        return CopyleaksAllowedCrossLanguagesResponseModel.model_validate(response.json())

    @staticmethod
    def ocr_supported_langauges(timeout=None):
        '''
        Get a list of the supported languages for OCR (this is not a list of supported languages for the api, but only for the OCR files scan).
        For more info: https://docs.copyleaks.com/reference/actions/miscellaneous/ocr-supported-languages

        Raises:
            `CommandError`: Server reject the request. See response status code, headers and content for more info.
            `UnderMaintenanceError`: Copyleaks servers are unavailable for maintenance. We recommend to implement exponential backoff algorithm as described here: https://api.copyleaks.com/documentation/v3/exponential-backoff

        Returns:
            List of supported OCR languages.
        '''

        url = f"{Consts.API_SERVER_URI}/v3/miscellaneous/ocr-languages-list"
        response = CopyleaksHttpClient.request('GET', url, headers=CopyleaksClientHelper.headers(content_type=None),
                                               timeout=timeout)
        return response.json()

    @staticmethod
    def repository_info(auth_token, repository_id, timeout=None):
        '''
            Get the information of a Private Cloud Hub repository, such as credit consumption, masking policy
            and status. Requires the "Super Admin" or "Admin" role on the repository.
            For more info: https://docs.copyleaks.com/reference/actions/private-cloud-hub/info

            Parameters:
                auth_token: Your login token to Copyleaks server.
                repository_id: String. The repository ID, from the Copyleaks Admin Dashboard.

            Raises:
                `CommandError`: Server reject the request. See response status code, headers and content for more info.
                `RateLimitError`: Too many requests. Please wait before calling again.
                `UnderMaintenanceError`: Copyleaks servers are unavailable for maintenance. We recommend to implement exponential backoff algorithm as described here: https://api.copyleaks.com/documentation/v3/exponential-backoff

            Returns:
                `CopyleaksRepositoryInfoResponseModel`.
        '''
        assert repository_id

        Copyleaks.verify_auth_token(auth_token)

        url = f"{Consts.API_SERVER_URI}/v3/repositories/repository/{repository_id}/info"
        response = CopyleaksHttpClient.request('GET', url, headers=CopyleaksClientHelper.headers(auth_token, None),
                                               timeout=timeout)
        return CopyleaksRepositoryInfoResponseModel.model_validate(response.json())
