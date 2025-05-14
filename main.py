import os
from flask import Flask, jsonify
from flask_cors import CORS

from extensions import db
from auth import auth
from admin_api import admin_bp
from dashboard_models import DashboardCategory, DashboardItem

def create_app():
    app = Flask(__name__)

    # Config
    app.config["SECRET_KEY"] = os.environ.get("FLASK_SECRET_KEY", "dev_secret")
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f"mysql+pymysql://{os.getenv('DB_USERNAME', 'root')}:"
        f"{os.getenv('DB_PASSWORD', 'password')}@"
        f"{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '3306')}/"
        f"{os.getenv('DB_NAME', 'mydb')}"
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Extensions
    db.init_app(app)
    CORS(app, resources={r"/api/*": {"origins": "*"}})

    # Routes
    app.register_blueprint(admin_bp)

    @app.route("/")
    def index():
        return jsonify({"message": "Welcome to the Dashboard API"})

    with app.app_context():
        try:
            if not db.engine.dialect.has_table(db.engine.connect(), DashboardCategory.__tablename__):
                db.create_all()
        except Exception as e:
            print(f"Error checking or creating tables: {e}")
            try:
                db.create_all()
            except Exception as e2:
                print(f"Table creation failed: {e2}")

    return app

# Gunicorn entrypoint
app = create_app()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5001)), debug=True)
