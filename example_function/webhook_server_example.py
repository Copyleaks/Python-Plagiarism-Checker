import threading
import sys
from WebhookExamples import start_flask_server

# Create a shutdown event for gracefully shutting down the Flask server using Ctrl+C
exit_event = threading.Event()

def signal_handler(sig, frame):
    """
    Signal handler for Ctrl+C to gracefully shut down the Flask webhook server.
    """
    print("\n🛑 Ctrl+C detected. Shutting down server.")
    server_thread.shutdown()
    exit_event.set()
    sys.exit(0)  # Forcefully exit even if main is still executing

def run():
    """
    Start the Flask webhook server in the background.
    If you are using ngrok, run it on port 5000.
    """
    global server_thread
    server_thread = start_flask_server()
    server_thread.start()
    print("🚀 Flask server is running and listening for webhooks.")
    print("🔴 Press Ctrl+C to shut down the server.")
    return exit_event, server_thread, signal_handler
