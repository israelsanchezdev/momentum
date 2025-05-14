import sys
import os

# Ensure the current directory is in the path for absolute imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask, jsonify
from flask_cors import CORS

from extensions import db
from auth import auth
from admin_api import admin_bp
from dashboard_models import DashboardCategory, DashboardItem

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "a_very_secret_key_for_dev")
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+pymysql://{os.getenv('DB_USERNAME', 'root')}:"
        f"{os.getenv('DB_PASSWORD', 'password')}@"
        f"{os.getenv('DB_HOST', 'localhost')}:"
        f"{os.getenv('DB_PORT', '3306')}/"
        f"{os.getenv('DB_NAME', 'mydb')}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize extensions
    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Register blueprints
    app.register_blueprint(admin_bp)

    # Create tables if necessary
    with app.app_context():
        try:
            if not db.engine.dialect.has_table(db.engine.connect(), DashboardCategory.__tablename__):
                print("Creating database tables...")
                db.create_all()
            else:
                print("Database tables already exist.")
        except Exception as e:
            print(f"Error checking/creating tables: {e}")
            try:
                db.create_all()
            except Exception as e2:
                print(f"Final table creation failed: {e2}")

    @app.route("/")
    def index():
        return jsonify({"message": "Welcome to the Dashboard API"})

    return app

# 🟢 Required for gunicorn (Render reads this line)
app = create_app()

# Optional for local dev
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5001)), debug=True)
