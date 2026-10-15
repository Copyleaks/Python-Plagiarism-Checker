'''Unit tests for the PDF report version after the legacy version removal (BAC-6816); requests is mocked.'''
import importlib
import json
import unittest
from unittest.mock import MagicMock, patch

from copyleaks.copyleaks import Copyleaks
from copyleaks.models.submit.document import FileDocument
from copyleaks.models.submit.properties.pdf import Pdf
from copyleaks.models.submit.properties.scan_properties import ScanProperties

AUTH_TOKEN = {'access_token': 'token', '.expires': '2999-01-01T00:00:00Z'}


def submitted_pdf(pdf):
    properties = ScanProperties('https://example.com/webhook/{STATUS}')
    properties.set_pdf(pdf)
    document = FileDocument('aGVsbG8=', 'file.txt')
    document.set_properties(properties)
    with patch('requests.put', return_value=MagicMock(ok=True, status_code=201)) as put:
        Copyleaks.submit_file(AUTH_TOKEN, 'my-scan-1', document)
    return json.loads(put.call_args.kwargs['data'])['properties']['pdf']


class PdfVersionTest(unittest.TestCase):
    def test_legacy_version_accessors_are_removed(self):
        self.assertFalse(hasattr(Pdf, 'set_version'))
        self.assertFalse(hasattr(Pdf, 'get_version'))

    def test_legacy_pdf_version_module_is_removed(self):
        with self.assertRaises(ModuleNotFoundError):
            importlib.import_module('copyleaks.models.submit.properties.pdf_version')

    def test_report_version_v3_is_sent(self):
        pdf = Pdf()
        pdf.set_create(True)
        pdf.set_report_version('v3')
        self.assertEqual(pdf.get_report_version(), 'v3')
        self.assertEqual(submitted_pdf(pdf), {'create': True, 'reportVersion': 'v3'})


if __name__ == '__main__':
    unittest.main()
