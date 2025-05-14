from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS
import json
import os

def create_app():
    app = Flask(__name__)
    CORS(app)

    @app.route('/')
    def home():
        return jsonify({"message": "Welcome to the Momentum Dashboard API"})

    @app.route('/data')
    def dashboard_data():
        try:
            with open('dashboard_data.json') as f:
                data = json.load(f)
            return jsonify(data)
        except FileNotFoundError:
            return jsonify({"error": "dashboard_data.json not found"}), 404
        except json.JSONDecodeError:
            return jsonify({"error": "Error decoding dashboard_data.json"}), 500

    return app

app = create_app()
