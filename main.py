# /home/ubuntu/dashboard_with_admin/dashboard_backend/src/main.py
import sys
import os

# This line is crucial for the Flask template to work correctly.
# It ensures that the `src` directory is in the Python path,
# allowing for absolute imports like `from src.extensions import db`.
# DO NOT CHANGE OR REMOVE THIS LINE.
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

from flask import Flask, jsonify
from flask_cors import CORS # Import CORS

from extensions import db
from auth import auth
from admin_api import admin_bp
from dashboard_models import DashboardCategory, DashboardItem

def create_app():
    app = Flask(__name__) 

    # --- Configuration --- 
    # In a real application, use environment variables for sensitive data.
    app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "a_very_secret_key_for_dev")
    
    # Database Configuration (MySQL)
    # The template provides this, uncomment and adjust if you are using a local/remote MySQL instance.
    # For SQLite for simpler setup initially (can be changed later):
    # app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///./dashboard_data.db"
    # Using the default MySQL from the template:
    app.config["SQLALCHEMY_DATABASE_URI"] = f"mysql+pymysql://{os.getenv('DB_USERNAME', 'root')}:{os.getenv('DB_PASSWORD', 'password')}@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '3306')}/{os.getenv('DB_NAME', 'mydb')}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # --- Extensions --- 
    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}}) # Enable CORS for all /api routes

    # --- Blueprints --- 
    app.register_blueprint(admin_bp)
    # You might add a simple public API blueprint later for the dashboard if needed, 
    # or use the admin_bp GET routes if they are public.

    # --- Database Initialization --- 
    with app.app_context():
        # Check if the database needs to be created
        # This is a simple check; for more robust migrations, use Flask-Migrate.
        try:
            # Attempt a simple query to see if tables exist
            # This is not foolproof but can prevent re-creating tables on every start
            # if they are already there.
            # A more robust solution is to use Alembic/Flask-Migrate.
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

    # --- Basic Routes (Optional) ---
    @app.route("/")
    def index():
        return jsonify({"message": "Welcome to the Dashboard API"})

    return app

if __name__ == "__main__":
    app = create_app()
    # Host 0.0.0.0 makes it accessible externally if not behind another proxy
    # Debug should be False in production
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5001)), debug=True)

