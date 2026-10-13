'''
Unit tests for Copyleaks.submit_file_ocr.
The HTTP layer (`requests`) is mocked, so no network calls are made.

Run from the repository root:
    python -m unittest discover -s tests -v
'''
import unittest
from unittest.mock import MagicMock, patch

from copyleaks.consts import Consts
from copyleaks.copyleaks import Copyleaks
from copyleaks.models.submit.document import OcrFileDocument
from copyleaks.models.submit.properties.scan_properties import ScanProperties

AUTH_TOKEN = {'access_token': 'token', '.expires': '2999-01-01T00:00:00Z'}


class SubmitOcrTest(unittest.TestCase):
    def test_submit_file_ocr_uses_the_ocr_endpoint(self):
        # The API route is PUT /v3/scans/submit/ocr/{scanId}
        # (https://docs.copyleaks.com/reference/actions/authenticity/submit-ocr).
        # The SDK used /v3/scans/submit/file/ocr/{scanId}, which does not exist and returns 404.
        document = OcrFileDocument('aW1hZ2U=', 'scan.png')
        document.set_language('en')
        document.set_properties(ScanProperties('https://example.com/webhook/{STATUS}'))
        response = MagicMock(ok=True, status_code=201)

        with patch('requests.put', return_value=response) as put:
            Copyleaks.submit_file_ocr(AUTH_TOKEN, 'my-scan-1', document)

        put.assert_called_once()
        self.assertEqual(put.call_args.args[0], f'{Consts.API_SERVER_URI}/v3/scans/submit/ocr/my-scan-1')


if __name__ == '__main__':
    unittest.main()
