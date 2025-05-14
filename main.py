import sys
import os

# Ensure that the base directory is in the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, jsonify
from flask_cors import CORS

from extensions import db
from auth import auth
from admin_api import admin_bp
from dashboard_models import DashboardCategory, DashboardItem

def create_app():
    app = Flask(__name__) 

    # --- Configuration ---
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///dashboard_data.db"

    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # --- Extensions ---
    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # --- Blueprints ---
    app.register_blueprint(admin_bp)

    # --- Database Initialization ---
    with app.app_context():
        try:
            if not db.engine.dialect.has_table(db.engine.connect(), DashboardCategory.__tablename__):
                print("Creating database tables...")
                db.create_all()
                print("Database tables created.")
            else:
                print("Database tables already exist.")
        except Exception as e:
            print(f"Error during database check/creation: {e}")
            print("Attempting to create tables anyway...")
            try:
                db.create_all()
                print("Database tables created after error.")
            except Exception as e_inner:
                print(f"Failed to create tables: {e_inner}")

    # --- Basic Route ---
    @app.route("/")
    def index():
        return jsonify({"message": "Welcome to the Dashboard API"})

    return app

# This is what Gunicorn expects:
app = create_app()

# Only used for local testing (not in production)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5001)), debug=True)
