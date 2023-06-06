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

import base64
import random
from copyleaks.copyleaks import Copyleaks
from copyleaks.exceptions.command_error import CommandError
from copyleaks.models.submit.document import FileDocument, UrlDocument, OcrFileDocument
from copyleaks.models.submit.properties.scan_properties import ScanProperties
from copyleaks.models.export import *
# Register on https://api.copyleaks.com and grab your secret key (from the dashboard page).
EMAIL_ADDRESS = 'your@email.addresss'
KEY = '00000000-0000-0000-0000-000000000000'

try:
    auth_token = Copyleaks.login(EMAIL_ADDRESS, KEY)
except CommandError as ce:
    response = ce.get_response()
    print(f"An error occurred (HTTP status code {response.status_code}):")
    print(response.content)
    exit(1)

print("Logged successfully!\nToken:")
print(auth_token)


# This example is going to scan a FILE for plagiarism.
# Alternatively, you can scan a URL using the class `UrlDocument`.

print("Submitting a new file...")
BASE64_FILE_CONTENT = base64.b64encode(b'Hello world').decode('utf8')  # or read your file and convert it into BASE64 presentation.
FILENAME = "hello.txt"
scan_id = random.randint(100, 100000)  # generate a random scan id
file_submission = FileDocument(BASE64_FILE_CONTENT, FILENAME)
# Once the scan completed on Copyleaks servers, we will trigger a webhook that notify you.
# Write your public endpoint server address. If you testing it locally, make sure that this endpoint
# is publicly available.
scan_properties = ScanProperties('https://your.server/webhook?event={{STATUS}}')
scan_properties.set_sandbox(True)  # Turn on sandbox mode. Turn off on production.
file_submission.set_properties(scan_properties)
Copyleaks.submit_file(auth_token, scan_id, file_submission)  # sending the submission to scanning
print("Send to scanning")
print("You will notify, using your webhook, once the scan was completed.")

# Wait for completion webhook arrival...
# Read more: https://api.copyleaks.com/documentation/v3/webhooks
# Uncomment the following code to create an export task:
# # Once the webhooks arrived and the scan was completed successfully (see the `status` flag) you can
# # proceed to exporting all the artifacts related to your scan.
# export = Export()
# export.set_completion_webhook('https://your.server/webhook/export/completion')
# crawled = ExportCrawledVersion()  # Uncomment if you want to download the crawled version of your submitted document.
# crawled.set_endpoint('https://your.server/webhook/export/crawled')
# crawled.set_verb('POST')
# crawled.set_headers([['key', 'value'], ['key2', 'value2']])  # optional
# export.set_crawled_version(crawled)

# # For each of the results in the Completed Webhook, you will get a unique `id`.
# # In the following example we will export 2 results from Copyleaks's servers:
# results1 = ExportResult()
# results1.set_id('2b42c39fba')  # change with your result id
# results1.set_endpoint('https://your.server/webhook/export/result/2b42c39fba')
# results1.set_verb('POST')
# results1.set_headers([['key', 'value'], ['key2', 'value2']])

# results2 = ExportResult()
# results2.set_id('08338e505d')  # change with your result id
# results2.set_endpoint('https://your.server/webhook/export/result/08338e505d')
# results2.set_verb('POST')
# results2.set_headers([['key', 'value'], ['key2', 'value2']])

# export.set_results([results1, results2])

# Copyleaks.export(auth_token, scan_id, 'export-id', export)  # 'export-id' value determind by you.

# Wait while Copyleaks servers exporting artifacts...
# Once process completed, you will get the "Export Completed" webhook.
# Read more: https://api.copyleaks.com/documentation/v3/webhooks/export-completed

# # For Repositories:
# repo = SearchRepository()
# repo.set_include_my_submissions(True)
# repo.set_include_others_submissions(True)
# repo.set_id("ID_FETCHED_DASHBOARD")
# scan_properties.set_scanning(Scanning().set_repositories(repo))

# # generate a pdf report:
#pdf = Pdf() # Creating instance of Pdf.
#pdf.set_create(True) # Setting the create pdf to True to generate PDF report.
#scan_properties.set_pdf(pdf) # Will generate PDF report.