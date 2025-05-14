from flask import Blueprint, jsonify
from extensions import db
from dashboard_models import DashboardItem, DashboardCategory

# Create a blueprint for dashboard routes
dashboard_bp = Blueprint("dashboard", __name__, url_prefix="/api")

@dashboard_bp.route("/dashboard", methods=["GET"])
def get_dashboard_data():
    data = {
        "total_items": DashboardItem.query.count(),
        "total_categories": DashboardCategory.query.count(),
        "active_users": 5  # TODO: Replace with real logic if needed
    }
    return jsonify(data)
