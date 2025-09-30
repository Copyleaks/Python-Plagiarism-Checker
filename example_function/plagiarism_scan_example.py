import base64
from copyleaks.models.submit.document import FileDocument
from copyleaks.models.submit.properties.submit_webhooks import SubmitWebhooks
from copyleaks.models.submit.properties.scan_properties import ScanProperties
from copyleaks.copyleaks import Copyleaks

def run(auth_token, scan_id):
    
    print("Submitting a new file for plagiarism scan...")
    BASE64_FILE_CONTENT = base64.b64encode(b'Hello world').decode('utf8')
    FILENAME = "hello.txt"
    
    file_submission = FileDocument(BASE64_FILE_CONTENT, FILENAME)
    webhooks = SubmitWebhooks()
    webhooks.set_status('https://your.server/webhook/{STATUS}')
    
    webhooks.set_new_result('https://your.server/webhook/new-results')
    scan_properties = ScanProperties(status_webhook='https://your.server/webhook/{STATUS}')
    scan_properties.set_webhooks(webhooks)
    scan_properties.set_sandbox(True)
    
    file_submission.set_properties(scan_properties)
    Copyleaks.submit_file(auth_token, scan_id, file_submission)
    print("Send to scanning")
    print("You will be notified, using your webhook, once the scan is completed.")
