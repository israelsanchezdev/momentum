from flask import Flask, jsonify, render_template
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import json
import os

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    CORS(app)

    # Config – update this with real database info later
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL", "sqlite:///local.db")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)

    # Route for homepage
    @app.route("/")
    def index():
        return render_template("index.html")  # looks inside /templates

    # Route to serve the JSON data
    @app.route("/data")
    def get_data():
        try:
            with open("data.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            return jsonify(data)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    # Optional: Fallback or simple API route
    @app.route("/api")
    def welcome():
        return jsonify({"message": "Welcome to the Dashboard API"})

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
