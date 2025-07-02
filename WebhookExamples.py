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
import logging
import threading
from typing import Optional, List, Any, Dict
from copyleaks.models.submit.Webhooks.CompletedWebhookModel import CompletedWebhookModel
from copyleaks.models.submit.Webhooks.CreditsCheckedWebhookModel import CreditsCheckedWebhookModel
from copyleaks.models.submit.Webhooks.ErrorWebhookModel import ErrorWebhookModel
from copyleaks.models.submit.Webhooks.HelperModels.CompletedModels.NotificationsModel import NotificationsModel
from copyleaks.models.submit.Webhooks.HelperModels.CompletedModels.ResultsModel import ResultsModel
from copyleaks.models.submit.Webhooks.HelperModels.CompletedModels.ScannedDocumentModel import ScannedDocumentModel
from copyleaks.models.submit.Webhooks.IndexedWebhookModel import IndexedWebhookModel
from copyleaks.models.submit.Webhooks.NewResultWebhookModel import NewResultWebhookModel
from flask import Flask, request, jsonify 
from pydantic import *
from flask import Flask, request, jsonify
import logging
from werkzeug.serving import make_server

#This server listens for Copyleaks webhook events and handles each type at a separate endpoint.
#
#Webhooks handled:
#- /webhook/completed         --> Triggered when scan is completed
#- /webhook/error             --> Triggered when a scan errors
#- /webhook/indexed           --> Triggered when scan is indexed
#- /webhook/creditsChecked    --> Triggered after credit check
#
#Usage with Ngrok (example):
#    ngrok http 5000
#    -> Update your Copyleaks scan properties to use: https://<your-ngrok>.ngrok.io/webhook/{{event}}

class ServerThread(threading.Thread):
    """
    A thread-based wrapper to run a Flask application using Werkzeug's development server.
    
    This allows the Flask app to run in the background (non-blocking), while the main thread
    continues with other logic (e.g., API calls, event waiting, etc.).
    """

    def __init__(self, app):
        """
        Initializes the server thread with a Flask app.

        Args:
            app (Flask): The Flask application instance to be served.
        """
        threading.Thread.__init__(self)
        self.server = make_server('0.0.0.0', 5000, app)  # Bind to all interfaces on port 5000
        self.ctx = app.app_context()  # Create application context
        self.ctx.push()  

    def run(self):
        """
        Starts the Flask development server. This method is called when `start()` is invoked.
        """
        logging.info("Starting Flask server...")
        self.server.serve_forever()  # Blocking call that runs the server until shutdown is called

    def shutdown(self):
        """
        Shuts down the Flask server gracefully.
        """
        logging.info("Shutting down Flask server...")
        self.server.shutdown()

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

# === Webhook: Scan Completed ===
@app.route('/webhook/completed', methods=['POST'])
def webhook_completed():
    logging.info("[Webhook] COMPLETED")
    logging.info("Payload:")
    logging.info(request.json)

    # Deserialize JSON into CompletedWebhook object
    completed_data = CompletedWebhookModel(**request.json)

    # Additional processing can be done here
    return jsonify({'message': f'Completed received:{completed_data}'}), 200

# === Webhook: Scan Error ===
@app.route('/webhook/error', methods=['POST'])
def webhook_error():
    logging.info("[Webhook] ERROR")
    logging.info("Payload:")
    logging.info(request.json)

    # Deserialize JSON into ErrorWebhook object
    error_data = ErrorWebhookModel(**request.json)

    # Additional processing can be done here
    return jsonify({'message': f'Error received - {error_data}'}), 200

# === Webhook: Scan Indexed ===
@app.route('/webhook/indexed', methods=['POST'])
def webhook_indexed():
    logging.info("[Webhook] INDEXED")
    logging.info("Payload:")
    logging.info(request.json)

    # Deserialize JSON into IndexedWebhook object
    indexed_data = IndexedWebhookModel(**request.json)

    # Additional processing can be done here
    return jsonify({'message': f'Indexed received - {indexed_data}'}), 200

# === Webhook: Credits Checked ===
@app.route('/webhook/creditsChecked', methods=['POST'])
def webhook_credits_checked():
    logging.info("[Webhook] CREDITS CHECKED")
    logging.info("Payload:")
    logging.info(request.json)

    # Deserialize JSON into CreditsCheckedWebhook object
    credits_checked_data = CreditsCheckedWebhookModel(**request.json)

    # Additional processing can be done here
    return jsonify({'message': f'CreditsChecked received - {credits_checked_data}'}), 200


# === Webhook: Credits Checked ===
@app.route('/webhook/new-results', methods=['POST'])
def webhook_new_results():
    logging.info("[Webhook] NEW-RESULTS")
    logging.info("Payload:")
    logging.info(request.json)

    # Deserialize JSON into CreditsCheckedWebhook object
    new_results_data = NewResultWebhookModel(**request.json)

    # Additional processing can be done here
    return jsonify({'message': f'new-results received - {new_results_data}'}), 200


def start_flask_server():
    return ServerThread(app)