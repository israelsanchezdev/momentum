import sys
import os

# Ensure the project root is in Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, jsonify, render_template
from flask_cors import CORS

from extensions import db
from auth import auth
from admin_api import admin_bp
from dashboard_models import DashboardCategory, DashboardItem

def create_app():
    app = Flask(__name__, template_folder='templates', static_folder='static')

    # --- Configuration ---
    app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "a_very_secret_key_for_dev")
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+pymysql://{os.getenv('DB_USERNAME', 'root')}:"
        f"{os.getenv('DB_PASSWORD', 'password')}@"
        f"{os.getenv('DB_HOST', 'localhost')}:"
        f"{os.getenv('DB_PORT', '3306')}/"
        f"{os.getenv('DB_NAME', 'mydb')}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # --- Extensions ---
    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # --- Blueprints ---
    app.register_blueprint(admin_bp)
    app.register_blueprint(auth)

    # --- Database Initialization ---
    with app.app_context():
        try:
            if not db.engine.dialect.has_table(db.engine.connect(), DashboardCategory.__tablename__):
                print("Creating database tables...")
                db.create_all()
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

    # --- Routes ---
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/api/data")
    def get_data():
        # This should eventually query your real DB
        dummy_data = [
            {"category": "Community & Placemaking Initiatives", "title": "Topeka-Shawnee County Housing Strategies", "value": 33},
            {"category": "Community & Placemaking Initiatives", "title": "Housing Advocacy Task Force", "value": 20},
            {"category": "Economic Development & Business Growth", "title": "Career Connections Program", "value": 27},
            {"category": "Talent Development & Workforce Support", "title": "Washburn Now", "value": 55},
            {"category": "Community Identity & Engagement", "title": "Choose Topeka 2.0", "value": 40}
        ]
        return jsonify(dummy_data)

    return app

# Required only for local development
if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5001)), debug=True)
