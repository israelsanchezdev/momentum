# /home/ubuntu/dashboard_with_admin/dashboard_backend/src/routes/admin_api.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from flask import Blueprint, request, jsonify
from extensions import db
from dashboard_models import DashboardCategory, DashboardItem
from src.auth import auth # Import the auth object

admin_bp = Blueprint("admin_api", __name__, url_prefix="/api/admin")

# --- Category Routes (Protected) ---
@admin_bp.route("/categories", methods=["POST"])
@auth.login_required
def create_category():
    data = request.get_json()
    if not data or not data.get("title"):
        return jsonify({"message": "Title is required"}), 400
    if DashboardCategory.query.filter_by(title=data["title"]).first():
        return jsonify({"message": "Category with this title already exists"}), 409
    
    new_category = DashboardCategory(title=data["title"])
    db.session.add(new_category)
    db.session.commit()
    return jsonify(new_category.to_dict()), 201

@admin_bp.route("/categories", methods=["GET"])
# Publicly accessible to fetch data for the main dashboard, so no auth needed here.
# If admin-only listing is needed, a separate endpoint or different auth logic would be required.
def get_categories():
    categories = DashboardCategory.query.all()
    return jsonify([category.to_dict() for category in categories]), 200

@admin_bp.route("/categories/<int:category_id>", methods=["GET"])
# Also public for dashboard display
def get_category(category_id):
    category = DashboardCategory.query.get_or_404(category_id)
    return jsonify(category.to_dict()), 200

@admin_bp.route("/categories/<int:category_id>", methods=["PUT"])
@auth.login_required
def update_category(category_id):
    category = DashboardCategory.query.get_or_404(category_id)
    data = request.get_json()
    if not data or not data.get("title"):
        return jsonify({"message": "Title is required"}), 400
    
    existing_category = DashboardCategory.query.filter(DashboardCategory.title == data["title"], DashboardCategory.id != category_id).first()
    if existing_category:
        return jsonify({"message": "Another category with this title already exists"}), 409
        
    category.title = data["title"]
    db.session.commit()
    return jsonify(category.to_dict()), 200

@admin_bp.route("/categories/<int:category_id>", methods=["DELETE"])
@auth.login_required
def delete_category(category_id):
    category = DashboardCategory.query.get_or_404(category_id)
    db.session.delete(category)
    db.session.commit()
    return jsonify({"message": "Category deleted successfully"}), 200

# --- Item Routes (Protected) ---
@admin_bp.route("/categories/<int:category_id>/items", methods=["POST"])
@auth.login_required
def create_item(category_id):
    category = DashboardCategory.query.get_or_404(category_id)
    data = request.get_json()
    if not data or not data.get("name") or data.get("percentage") is None:
        return jsonify({"message": "Name and percentage are required"}), 400
    try:
        percentage = int(data["percentage"])
        if not (0 <= percentage <= 100):
            raise ValueError("Percentage must be between 0 and 100")
    except ValueError as e:
        return jsonify({"message": str(e)}), 400

    new_item = DashboardItem(name=data["name"], percentage=percentage, category_id=category.id)
    db.session.add(new_item)
    db.session.commit()
    return jsonify(new_item.to_dict()), 201

@admin_bp.route("/items/<int:item_id>", methods=["GET"])
# Public for dashboard display
def get_item(item_id):
    item = DashboardItem.query.get_or_404(item_id)
    return jsonify(item.to_dict()), 200

@admin_bp.route("/items/<int:item_id>", methods=["PUT"])
@auth.login_required
def update_item(item_id):
    item = DashboardItem.query.get_or_404(item_id)
    data = request.get_json()
    if not data:
        return jsonify({"message": "No data provided"}), 400

    if "name" in data:
        item.name = data["name"]
    if "percentage" in data:
        try:
            percentage = int(data["percentage"])
            if not (0 <= percentage <= 100):
                raise ValueError("Percentage must be between 0 and 100")
            item.percentage = percentage
        except ValueError as e:
            return jsonify({"message": str(e)}), 400
    if "category_id" in data:
        if not DashboardCategory.query.get(data["category_id"]):
            return jsonify({"message": "Target category not found"}), 404
        item.category_id = data["category_id"]
        
    db.session.commit()
    return jsonify(item.to_dict()), 200

@admin_bp.route("/items/<int:item_id>", methods=["DELETE"])
@auth.login_required
def delete_item(item_id):
    item = DashboardItem.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"message": "Item deleted successfully"}), 200

