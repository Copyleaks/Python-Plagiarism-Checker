from copyleaks.consts import Consts
import requests
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

import json
from datetime import datetime, timedelta
import dateutil.parser
import pytz
from copyleaks.exceptions.command_error import CommandError
from copyleaks.exceptions.under_maintenance_error import UnderMaintenanceError
from copyleaks.exceptions.rate_limit_error import RateLimitError
from copyleaks.exceptions.auth_expired_error import AuthExipredError
from enum import Enum


class Copyleaks(object):

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
    def login(email, key):
        '''
            Login to Copyleaks authentication server.
            For more info: https://api.copyleaks.com/documentation/v3/account/login

            Parameters:
                email: string. Copyleaks account email address.
                key: string. Copyleaks account secret key.

            Raises:
                `CommandError`: Server reject the request. See response status code, headers and content for more info.
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

        headers = {
            'Content-Type': 'application/json',
            'User-Agent': Consts.USER_AGENT
        }

        response = requests.post(url, headers=headers, data=json.dumps(payload))
        if response.ok:
            return response.json()
        elif response.status_code == 503:
            raise UnderMaintenanceError()
        else:
            raise CommandError(response)

    @staticmethod
    def verify_auth_token(auth_token):
        '''
            Verify that Copyleaks authentication token is exists and not expired.

            Parameters:
                auth_token: Copyleaks authentication token

            Raises:
                `AuthExipredError`: authentication expired. Need to login again.
        '''
        assert auth_token and auth_token['.expires'] and auth_token['access_token']

        now = pytz.UTC.localize(datetime.utcnow() + timedelta(0, 5 * 60))  # adds 5 minutes ahead for a safety shield.
        upTo = dateutil.parser.parse(auth_token['.expires'])

        if upTo <= now:
            raise AuthExipredError()  # expired

    @staticmethod
    def __submit(url, auth_token, scan_id, submission):
        assert url and scan_id and submission

        Copyleaks.verify_auth_token(auth_token)

        headers = {
            'Content-Type': 'application/json',
            'User-Agent': Consts.USER_AGENT,
            'Authorization': f"Bearer {auth_token['access_token']}"
        }

        response = requests.put(url, headers=headers, data=submission.toJSON())
        if response.ok:
            return  # Completed successfully
        elif response.status_code == 503:
            raise UnderMaintenanceError()
        else:
            raise CommandError(response)

    @staticmethod
    def submit_file(auth_token, scan_id, submission):
        '''
            Starting a new process by providing a file to scan.
            For more info: 
            https://api.copyleaks.com/documentation/v3/scans/submit/file

            Raises:
                `CommandError`: Server reject the request. See response status code, headers and content for more info.
                `UnderMaintenanceError`: Copyleaks servers are unavailable for maintenance. We recommend to implement exponential backoff algorithm as described here: https://api.copyleaks.com/documentation/v3/exponential-backoff
        '''
        url = f"{Consts.API_SERVER_URI}/v3/scans/submit/file/{scan_id}"
        Copyleaks.__submit(url, auth_token, scan_id, submission)

    @staticmethod
    def submit_file_ocr(auth_token, scan_id, submission):
        '''
            Starting a new process by providing a OCR image file to scan.
            For more info: 
            https://api.copyleaks.com/documentation/v3/scans/submit/ocr

            Raises:
                `CommandError`: Server reject the request. See response status code, headers and content for more info.
                `UnderMaintenanceError`: Copyleaks servers are unavailable for maintenance. We recommend to implement exponential backoff algorithm as described here: https://api.copyleaks.com/documentation/v3/exponential-backoff
        '''
        url = f"{Consts.API_SERVER_URI}/v3/scans/submit/file/ocr/{scan_id}"
        Copyleaks.__submit(url, auth_token, scan_id, submission)

    @staticmethod
    def submit_url(auth_token, scan_id, submission):
        '''
            Starting a new process by providing a URL to scan.
            For more info: 
            https://api.copyleaks.com/documentation/v3/scans/submit/url

            Raises:
                `CommandError`: Server reject the request. See response status code, headers and content for more info.
                `UnderMaintenanceError`: Copyleaks servers are unavailable for maintenance. We recommend to implement exponential backoff algorithm as described here: https://api.copyleaks.com/documentation/v3/exponential-backoff
        '''
        url = f"{Consts.API_SERVER_URI}/v3/scans/submit/url/{scan_id}"
        Copyleaks.__submit(url, auth_token, scan_id, submission)

    @staticmethod
    def export(auth_token, scan_id, export_id, model):
        '''
            Exporting scans artifact into your server. 
            For more info: 
            https://api.copyleaks.com/documentation/v3/downloads/export

            Parameters: 
                auth_token: Your login token to Copyleaks server.
                scan_id: String. The scan ID of the specific scan to export.
                export_id: String. A new Id for the export process.
                model: `Export`. Request of which artifact should be exported.

            Raises:
                `CommandError`: Server reject the request. See response status code, headers and content for more info.
                `UnderMaintenanceError`: Copyleaks servers are unavailable for maintenance. We recommend to implement exponential backoff algorithm as described here: https://api.copyleaks.com/documentation/v3/exponential-backoff
        '''
        assert scan_id and export_id and model

        Copyleaks.verify_auth_token(auth_token)

        url = f"{Consts.API_SERVER_URI}/v3/downloads/{scan_id}/export/{export_id}"

        headers = {
            'Content-Type': 'application/json',
            'User-Agent': Consts.USER_AGENT,
            'Authorization': f"Bearer {auth_token['access_token']}"
        }

        response = requests.post(url, headers=headers, data=model.toJSON())
        if response.ok:
            return  # Completed successfully
        elif response.status_code == 503:
            raise UnderMaintenanceError()
        else:
            raise CommandError(response)

    @staticmethod
    def start(auth_token, model):
        '''
            Start scanning all the files you submitted for a price-check.
            For more info: 
            https://api.copyleaks.com/documentation/v3/scans/start

            Parameters: 
                auth_token: Your login token to Copyleaks server.
                model: `Start` object. Include information about which scans should be started.

            Raises:
                `CommandError`: Server reject the request. See response status code, headers and content for more info.
                `UnderMaintenanceError`: Copyleaks servers are unavailable for maintenance. We recommend to implement exponential backoff algorithm as described here: https://api.copyleaks.com/documentation/v3/exponential-backoff

            Returns: 
                Server response including success/failed info.
        '''
        assert model

        Copyleaks.verify_auth_token(auth_token)

        url = f"{Consts.API_SERVER_URI}/v3/scans/start"

        headers = {
            'Content-Type': 'application/json',
            'User-Agent': Consts.USER_AGENT,
            'Authorization': f"Bearer {auth_token['access_token']}"
        }

        response = requests.patch(url, headers=headers, data=model.toJSON())
        if response.ok:
            return response.json()  # Completed successfully
        elif response.status_code == 503:
            raise UnderMaintenanceError()
        else:
            raise CommandError(response)

    @staticmethod
    def delete(auth_token, delete_model):
        '''
            Delete the specific process from the server.
            For more info: 
            https://api.copyleaks.com/documentation/v3/scans/delete

            Raises:
                `CommandError`: Server reject the request. See response status code, headers and content for more info.
                `UnderMaintenanceError`: Copyleaks servers are unavailable for maintenance. We recommend to implement exponential backoff algorithm as described here: https://api.copyleaks.com/documentation/v3/exponential-backoff
        '''
        assert delete_model

        Copyleaks.verify_auth_token(auth_token)

        url = f"{Consts.API_SERVER_URI}/v3.1/scans/delete"

        headers = {
            'Content-Type': 'application/json',
            'User-Agent': Consts.USER_AGENT,
            'Authorization': f"Bearer {auth_token['access_token']}"
        }

        response = requests.patch(url, headers=headers, data=delete_model.toJSON())
        if response.ok:
            return  # Completed successfully
        elif response.status_code == 503:
            raise UnderMaintenanceError()
        else:
            raise CommandError(response)

    @staticmethod
    def resend_webhook(auth_token, scan_id):
        '''
            Resend status webhooks for existing scans.
            For more info: 
            https://api.copyleaks.com/documentation/v3/scans/webhook-resend

            Raises:
                `CommandError`: Server reject the request. See response status code, headers and content for more info.
                `UnderMaintenanceError`: Copyleaks servers are unavailable for maintenance. We recommend to implement exponential backoff algorithm as described here: https://api.copyleaks.com/documentation/v3/exponential-backoff
        '''
        assert scan_id

        Copyleaks.verify_auth_token(auth_token)

        url = f"{Consts.API_SERVER_URI}/v3/scans/{scan_id}/webhooks/resend"

        headers = {
            'Content-Type': 'application/json',
            'User-Agent': Consts.USER_AGENT,
            'Authorization': f"Bearer {auth_token['access_token']}"
        }

        response = requests.post(url, headers=headers)
        if response.ok:
            return  # Completed successfully
        elif response.status_code == 503:
            raise UnderMaintenanceError()
        else:
            raise CommandError(response)

    @staticmethod
    def credits_balance(auth_token):
        '''
            Get current credits balance for the Copyleaks account
            For more info: 
            https://api.copyleaks.com/documentation/v3/scans/credits

            Raises:
                `CommandError`: Server reject the request. See response status code, headers and content for more info.
                `UnderMaintenanceError`: Copyleaks servers are unavailable for maintenance. We recommend to implement exponential backoff algorithm as described here: https://api.copyleaks.com/documentation/v3/exponential-backoff
                `RateLimitError`: Too many requests. Please wait before calling again.

            Returns:
                Number of remaining credits on the account.
        '''
        Copyleaks.verify_auth_token(auth_token)

        url = f"{Consts.API_SERVER_URI}/v3/scans/credits"
        headers = {
            'User-Agent': Consts.USER_AGENT,
            'Authorization': f"Bearer {auth_token['access_token']}"
        }

        response = requests.get(url, headers=headers)
        if response.ok:
            return response.json()
        elif response.status_code == 503:
            raise UnderMaintenanceError()
        elif response.status_code == 429:
            raise RateLimitError()
        else:
            raise CommandError(response)

    @staticmethod
    def usages_history_csv(auth_token, start_date, end_date):
        '''
            This endpoint allows you to export your usage history between two dates.
            The output results will be exported to a csv file and it will be attached to the response.
            For more info: 
            https://api.copyleaks.com/documentation/v3/scans/usages/history

            Parameters: 
                auth_token: Your login token to Copyleaks server.
                start_date: String. The start date to collect usage history from. Date Format: `dd-MM-yyyy`
                end_date: String. The end date to collect usage history from. Date Format: `dd-MM-yyyy`

            Raises:
                `CommandError`: Server reject the request. See response status code, headers and content for more info.
                `UnderMaintenanceError`: Copyleaks servers are unavailable for maintenance. We recommend to implement exponential backoff algorithm as described here: https://api.copyleaks.com/documentation/v3/exponential-backoff
                `RateLimitError`: Too many requests. Please wait before calling again.

            Returns: 
                Server response including success/failed info.
        '''
        assert start_date and end_date

        Copyleaks.verify_auth_token(auth_token)

        url = f"{Consts.API_SERVER_URI}/v3/scans/usages/history?start={start_date}&end={end_date}"

        headers = {
            'Content-Type': 'application/json',
            'User-Agent': Consts.USER_AGENT,
            'Authorization': f"Bearer {auth_token['access_token']}"
        }

        response = requests.get(url, headers=headers)
        if response.ok:
            return response.content  # Completed successfully
        elif response.status_code == 503:
            raise UnderMaintenanceError()
        elif response.status_code == 429:
            raise RateLimitError()
        else:
            raise CommandError(response)

    @staticmethod
    def release_notes():
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
        headers = {
            'User-Agent': Consts.USER_AGENT
        }

        response = requests.get(url, headers=headers)
        if response.ok:
            return response.json()
        elif response.status_code == 503:
            raise UnderMaintenanceError()
        else:
            raise CommandError(response)

    @staticmethod
    def supported_file_types():
        '''
            Get a list of the supported file types.
            For more info: https://api.copyleaks.com/documentation/v3/specifications/supported-file-types

            Raises:
                `CommandError`: Server reject the request. See response status code, headers and content for more info.
                `UnderMaintenanceError`: Copyleaks servers are unavailable for maintenance. We recommend to implement exponential backoff algorithm as described here: https://api.copyleaks.com/documentation/v3/exponential-backoff

            Returns:
                List of supported file types.
        '''

        url = f"{Consts.API_SERVER_URI}/v3/miscellaneous/supported-file-types"
        headers = {
            'User-Agent': Consts.USER_AGENT
        }

        response = requests.get(url, headers=headers)
        if response.ok:
            return response.json()
        elif response.status_code == 503:
            raise UnderMaintenanceError()
        else:
            raise CommandError(response)

    @staticmethod
    def ocr_supported_langauges():
        '''
        Get a list of the supported languages for OCR (this is not a list of supported languages for the api, but only for the OCR files scan).
        For more info: https://api.copyleaks.com/documentation/v3/specifications/ocr-languages/list

        Raises:
            `CommandError`: Server reject the request. See response status code, headers and content for more info.
            `UnderMaintenanceError`: Copyleaks servers are unavailable for maintenance. We recommend to implement exponential backoff algorithm as described here: https://api.copyleaks.com/documentation/v3/exponential-backoff

        Returns: 
            List of supported OCR languages.
        '''

        url = f"{Consts.API_SERVER_URI}/v3/miscellaneous/ocr-languages-list"
        headers = {
            'User-Agent': Consts.USER_AGENT
        }

        response = requests.get(url, headers=headers)
        if response.ok:
            return response.json()
        elif response.status_code == 503:
            raise UnderMaintenanceError()
        else:
            raise CommandError(response)
