import os
import json
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/api/climate", methods=["POST"])
def climate():
    try:
        # Récupération des paramètres depuis la requête POST JSON
        data = request.get_json()
        email = data.get("email") or os.environ.get("KIA_EMAIL")
        password = data.get("password") or os.environ.get("KIA_PASSWORD")
        vin = data.get("vin") or os.environ.get("KIA_VIN")

        if not email or not password or not vin:
            return jsonify({"error": "Email, password, or VIN missing"}), 400

        # --- LOGIN Kia Europe ---
        url_login = "https://prd.eu-ccapi.kia.com:8090/v1.0/account/login"
        payload = {
            "email": email,
            "password": password,
            "country": "FR",
            "language": "fr"
        }
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "Mobile/1.0"
        }

        response = requests.post(url_login, json=payload, headers=headers, timeout=10)
        login_json = response.json()

        # Vérifier si sessionId/token est présent
        token = login_json.get("sessionId") or login_json.get("accessToken")
        if not token:
            return jsonify({"error": "Login failed", "details": login_json}), 401

        # --- Commande clim ---
        url_climate = f"https://prd.eu-ccapi.kia.com:8090/v1.0/vehicles/{vin}/hvac"
        headers_climate = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }
        payload_climate = {"action": "start"}

        climate_response = requests.post(url_climate, json=payload_climate, headers=headers_climate, timeout=10)

        return jsonify({
            "status": "success",
            "climate_response": climate_response.json()
        })

    except requests.exceptions.RequestException as e:
        return jsonify({"error": "Request failed", "details": str(e)}), 500
