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
from pydantic import ValidationError
from flask import Flask, request, jsonify
import logging
from werkzeug.serving import make_server

# Flask server with one endpoint per Copyleaks webhook: /webhook/completed, /webhook/error, /webhook/indexed,
# /webhook/creditschecked (the {STATUS} placeholder is lowercase) and /webhook/new-results.
# With ngrok: run `ngrok http 5000` and set the status webhook to https://<your-ngrok>.ngrok.io/webhook/{STATUS}

class ServerThread(threading.Thread):
    """Runs a Flask app on Werkzeug's development server in a background thread."""

    def __init__(self, app):
        threading.Thread.__init__(self)
        self.server = make_server('0.0.0.0', 5000, app)
        self.ctx = app.app_context()
        self.ctx.push()  

    def run(self):
        logging.info("Starting Flask server...")
        self.server.serve_forever()

    def shutdown(self):
        logging.info("Shutting down Flask server...")
        self.server.shutdown()

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

@app.route('/webhook/completed', methods=['POST'])
def webhook_completed():
    logging.info("[Webhook] COMPLETED")
    logging.info("Payload:")
    logging.info(request.json)

    completed_data = CompletedWebhookModel(**request.json)

    # Read the AI alert. No "suspected-ai-text" alert means the scan produced no AI alert.
    ai_alert = completed_data.get_ai_detection_alert()
    if ai_alert is not None:
        try:
            ai_result = ai_alert.get_ai_detection_result()
        except ValidationError:
            logging.exception("Could not parse the AI alert additional data")
            ai_result = None
        if ai_result is not None and ai_result.summary is not None:
            logging.info(f"AI text detected: ai={ai_result.summary.ai}, human={ai_result.summary.human}, model={ai_result.model_version}")

    return jsonify({'message': f'Completed received:{completed_data}'}), 200

@app.route('/webhook/error', methods=['POST'])
def webhook_error():
    logging.info("[Webhook] ERROR")
    logging.info("Payload:")
    logging.info(request.json)

    error_data = ErrorWebhookModel(**request.json)

    return jsonify({'message': f'Error received - {error_data}'}), 200

@app.route('/webhook/indexed', methods=['POST'])
def webhook_indexed():
    logging.info("[Webhook] INDEXED")
    logging.info("Payload:")
    logging.info(request.json)

    indexed_data = IndexedWebhookModel(**request.json)

    return jsonify({'message': f'Indexed received - {indexed_data}'}), 200

@app.route('/webhook/creditschecked', methods=['POST'])
def webhook_credits_checked():
    logging.info("[Webhook] CREDITS CHECKED")
    logging.info("Payload:")
    logging.info(request.json)

    credits_checked_data = CreditsCheckedWebhookModel(**request.json)

    return jsonify({'message': f'CreditsChecked received - {credits_checked_data}'}), 200


@app.route('/webhook/new-results', methods=['POST'])
def webhook_new_results():
    logging.info("[Webhook] NEW-RESULTS")
    logging.info("Payload:")
    logging.info(request.json)

    new_results_data = NewResultWebhookModel(**request.json)

    return jsonify({'message': f'new-results received - {new_results_data}'}), 200


def start_flask_server():
    return ServerThread(app)