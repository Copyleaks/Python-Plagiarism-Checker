import threading
import sys
from WebhookExamples import start_flask_server

exit_event = threading.Event()

def signal_handler(sig, frame):
    """Ctrl+C handler: shut down the webhook server and exit."""
    print("\n🛑 Ctrl+C detected. Shutting down server.")
    server_thread.shutdown()
    exit_event.set()
    sys.exit(0)  # Forcefully exit even if main is still executing

def run():
    """Start the Flask webhook server in the background, on port 5000 (the port to expose with ngrok)."""
    global server_thread
    server_thread = start_flask_server()
    server_thread.start()
    print("🚀 Flask server is running and listening for webhooks.")
    print("🔴 Press Ctrl+C to shut down the server.")
    return exit_event, server_thread, signal_handler
