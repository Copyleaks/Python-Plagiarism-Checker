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


# --- Webhook Server Example ---
# This will start the Flask webhook server in the background and handle Ctrl+C shutdown gracefully.
from example_function import webhook_server_example
exit_event, server_thread, signal_handler = webhook_server_example.run()


# Authentication example
from example_function import authentication_example
auth_token = authentication_example.run(EMAIL_ADDRESS, KEY)

def get_random_scan_id():
    return str(random.randint(100, 100000))


# Generate a random scan ID for this session
scan_id = get_random_scan_id()
print(f"\n--- Running all product examples with scan_id: {scan_id} ---\n")

# 1. Plagiarism scan example
plagiarism_scan_example.run(auth_token, scan_id)

# 2. AI text detection example
ai_detection_example.run(auth_token, scan_id)

# 3. Writing assistant feedback example
writing_assistant_example.run(auth_token, scan_id)

# 4. Text moderation example
text_moderation_example.run(auth_token, scan_id)

# 5. AI image detection example
ai_image_detection_example.run(auth_token, scan_id)

exit_event.wait()
