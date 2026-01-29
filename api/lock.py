from http.server import BaseHTTPRequestHandler
import json
import os

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # (optionnel) protection par PIN
        pin = self.headers.get("X-PIN")
        if pin != os.environ.get("APP_PIN"):
            self.send_response(401)
            self.end_headers()
            self.wfile.write(b"Invalid PIN")
            return

        # Réponse OK (on simulera le lock pour l'instant)
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

        response = {
            "action": "lock",
            "status": "success"
        }

        self.wfile.write(json.dumps(response).encode())
