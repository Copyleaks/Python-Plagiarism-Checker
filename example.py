import random
from copyleaks.copyleaks import Copyleaks
from copyleaks.exceptions.command_error import CommandError
import threading
from WebhookExamples import start_flask_server
import signal
import sys
from example_function import plagiarism_scan_example, ai_detection_example, writing_assistant_example, text_moderation_example, ai_image_detection_example
# Register on https://api.copyleaks.com and grab your secret key (from the dashboard page).
EMAIL_ADDRESS = 'your@email.addresss'
KEY = '00000000-0000-0000-0000-000000000000'


# Start the webhook server in the background; Ctrl+C shuts it down.
from example_function import webhook_server_example
exit_event, server_thread, signal_handler = webhook_server_example.run()


from example_function import authentication_example
auth_token = authentication_example.run(EMAIL_ADDRESS, KEY)

def get_random_scan_id():
    return str(random.randint(100, 100000))


scan_id = get_random_scan_id()
print(f"\n--- Running all product examples with scan_id: {scan_id} ---\n")

plagiarism_scan_example.run(auth_token, scan_id)

ai_detection_example.run(auth_token, scan_id)

writing_assistant_example.run(auth_token, scan_id)

text_moderation_example.run(auth_token, scan_id)

ai_image_detection_example.run(auth_token, scan_id)

exit_event.wait()
