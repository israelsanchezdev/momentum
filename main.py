# /home/ubuntu/dashboard_with_admin/dashboard_backend/main.py

import os
from flask import Flask, jsonify
from flask_cors import CORS

# Extensions and Blueprints
from extensions import db
from admin_api import admin_bp
from dashboard_models import DashboardCategory, DashboardItem

def create_app():
    app = Flask(__name__)

    # --- Configuration ---
    app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "a_very_secret_key_for_dev")

    # ✅ Use SQLite for now — easier to deploy; change if needed
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dashboard_data.db"
    # If you’re ready for MySQL, uncomment this:
    # app.config["SQLALCHEMY_DATABASE_URI"] = (
    #     f"mysql+pymysql://{os.getenv('DB_USERNAME')}:{os.getenv('DB_PASSWORD')}@"
    #     f"{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '3306')}/{os.getenv('DB_NAME')}"
    # )

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # --- Init Extensions ---
    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # --- Register Blueprints ---
    app.register_blueprint(admin_bp)

    # --- Create Tables ---
    with app.app_context():
        try:
            db.create_all()
            print("✅ Database initialized")
        except Exception as e:
            print(f"❌ Error checking or creating tables: {e}")

    # --- Root route ---
    @app.route("/")
    def index():
        return jsonify({"message": "Welcome to the Dashboard API"})

    return app

# ✅ Export app for Gunicorn
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)), debug=True)
