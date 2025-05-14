# main.py
import os
from flask import Flask, jsonify
from flask_cors import CORS

from extensions import db
from auth import auth
from admin_api import admin_bp
from dashboard_models import DashboardCategory, DashboardItem

def create_app():
    app = Flask(__name__)

    # --- Config ---
    app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "a_very_secret_key_for_dev")
    
    # ✅ Use SQLite for local / Render deployment (easiest option)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dashboard_data.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # --- Init Extensions ---
    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # --- Register Blueprints ---
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth)

    # --- Table Creation ---
    with app.app_context():
        try:
            db.create_all()
            print("✅ SQLite DB initialized")
        except Exception as e:
            print(f"❌ Error checking or creating tables: {e}")

    # --- Default Route ---
    @app.route("/")
    def index():
        return jsonify({"message": "Welcome to the Dashboard API"})

    return app

# Expose `app` directly for Gunicorn
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
