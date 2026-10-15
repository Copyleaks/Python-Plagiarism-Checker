'''
Unit tests for the deprecated PDF report version (BAC-6814).
The HTTP layer (`requests`) is mocked, so no network calls are made.

Run from the repository root:
    python -m unittest discover -s tests -v
'''
import json
import unittest
import warnings
from unittest.mock import MagicMock, patch

from copyleaks.copyleaks import Copyleaks
from copyleaks.models.submit.document import FileDocument
from copyleaks.models.submit.properties.pdf import Pdf
from copyleaks.models.submit.properties.pdf_version import PdfVersion
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
    def test_set_version_emits_deprecation_warning(self):
        pdf = Pdf()
        with self.assertWarns(DeprecationWarning) as caught:
            pdf.set_version(PdfVersion.V2)
        self.assertIn("set_report_version('v3')", str(caught.warning))
        self.assertEqual(caught.filename, __file__)
        self.assertEqual(pdf.get_version(), PdfVersion.V2)

    def test_set_report_version_does_not_warn(self):
        pdf = Pdf()
        with warnings.catch_warnings():
            warnings.simplefilter('error')
            pdf.set_report_version('v3')
        self.assertEqual(pdf.get_report_version(), 'v3')

    def test_version_is_not_sent_unless_set(self):
        pdf = Pdf()
        pdf.set_create(True)
        pdf.set_report_version('v3')
        self.assertEqual(submitted_pdf(pdf), {'create': True, 'reportVersion': 'v3'})

    def test_version_is_still_sent_when_set(self):
        pdf = Pdf()
        pdf.set_create(True)
        with self.assertWarns(DeprecationWarning):
            pdf.set_version(PdfVersion.V2)
        self.assertEqual(submitted_pdf(pdf), {'create': True, 'version': 2})


if __name__ == '__main__':
    unittest.main()
