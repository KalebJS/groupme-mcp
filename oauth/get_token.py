"""
Local OAuth helper for GroupMe.

GroupMe uses the OAuth 2.0 implicit flow:
  1. User is sent to https://oauth.groupme.com/oauth/authorize?client_id=CLIENT_ID
  2. After approval, GroupMe redirects to your registered callback URL with
     ?access_token=TOKEN appended.

This script starts a temporary HTTP server on localhost, opens the authorize
URL in your browser, and prints the token once GroupMe redirects back.

Before running, register http://localhost:<PORT>/callback as your application's
callback URL at https://dev.groupme.com/applications.

Usage:
    python get_token.py --client-id YOUR_CLIENT_ID
    python get_token.py --client-id YOUR_CLIENT_ID --port 8080
    GROUPME_CLIENT_ID=YOUR_CLIENT_ID python get_token.py
"""

import argparse
import os
import threading
import webbrowser
from http.server import BaseHTTPRequestHandler
from http.server import HTTPServer
from urllib.parse import parse_qs
from urllib.parse import urlparse

AUTHORIZE_URL = "https://oauth.groupme.com/oauth/authorize"

# Shared state written by the handler, read by the main thread.
_token: str | None = None
_server: HTTPServer | None = None


class _CallbackHandler(BaseHTTPRequestHandler):
    def do_GET(self) -> None:
        global _token, _server

        parsed = urlparse(self.path)
        params = parse_qs(parsed.query)
        token = params.get("access_token", [None])[0]

        if token:
            _token = token
            body = b"<h2>Token received! You can close this tab.</h2>"
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        else:
            body = b"<h2>No access_token found in the redirect. Check your app's callback URL.</h2>"
            self.send_response(400)
            self.send_header("Content-Type", "text/html")
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)

        # Shut down the server from a background thread so handle_request() can return.
        threading.Thread(target=_server.shutdown, daemon=True).start()  # type: ignore[union-attr]

    def log_message(self, format: str, *args: object) -> None:
        pass  # silence request logs


def main() -> None:
    global _server

    parser = argparse.ArgumentParser(description="Obtain a GroupMe access token via OAuth.")
    parser.add_argument(
        "--client-id",
        default=os.environ.get("GROUPME_CLIENT_ID", ""),
        help="Your GroupMe application client ID (or set GROUPME_CLIENT_ID env var).",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=8080,
        help="Local port to listen on (default: 8080).",
    )
    args = parser.parse_args()

    if not args.client_id:
        parser.error("--client-id is required (or set GROUPME_CLIENT_ID)")

    callback_url = f"http://localhost:{args.port}/callback"
    authorize_url = f"{AUTHORIZE_URL}?client_id={args.client_id}"

    _server = HTTPServer(("localhost", args.port), _CallbackHandler)

    print(f"Listening on {callback_url}")
    print(f"Make sure '{callback_url}' is registered as your app's callback URL at")
    print("  https://dev.groupme.com/applications")
    print()
    print(f"Opening browser: {authorize_url}")
    webbrowser.open(authorize_url)

    _server.serve_forever()

    if _token:
        print(f"\nAccess token:\n\n  {_token}\n")
        print("Set it with:  export GROUPME_TOKEN=" + _token)
    else:
        print("\nNo token received.")


if __name__ == "__main__":
    main()
