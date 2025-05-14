import os
import sys
from flask import Flask, jsonify
from flask_cors import CORS

# Add the current directory to the Python path to fix imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from extensions import db
from admin_api import admin_bp
from dashboard_api import dashboard_bp  # ✅ Import the new blueprint


def create_app():
    app = Flask(__name__)

    # --- Configuration ---
    app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "a_very_secret_key_for_dev")

    # --- Database Configuration ---
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+pymysql://{os.getenv('DB_USERNAME', 'root')}:{os.getenv('DB_PASSWORD', 'password')}"
        f"@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '3306')}/{os.getenv('DB_NAME', 'mydb')}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # --- Initialize Extensions ---
    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # --- Register Blueprints ---
    app.register_blueprint(admin_bp)
    app.register_blueprint(dashboard_bp)  # ✅ Register the new dashboard API blueprint

    # --- Database Initialization ---
    with app.app_context():
        try:
            if not db.engine.dialect.has_table(db.engine.connect(), "dashboard_item"):
                print("Creating database tables...")
                db.create_all()
                print("Database tables created.")
            else:
                print("Database tables already exist.")
        except Exception as e:
            print(f"Error checking or creating tables: {e}")
            try:
                db.create_all()
                print("Database tables created after error.")
            except Exception as e_inner:
                print(f"Table creation failed: {e_inner}")

    # --- Health Check Route ---
    @app.route("/")
    def index():
        return jsonify({"message": "Welcome to the Dashboard API"})

    return app


# --- App Entrypoint ---
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5001)), debug=True)

# --- Gunicorn expects this ---
app = create_app()
