# /home/ubuntu/dashboard_with_admin/dashboard_backend/src/models/dashboard_models.py
import sys
import os
# Ensure the parent directory of 'src' is in the Python path
# This allows for absolute imports like 'from src.extensions import db'
# Adjust if your project structure or entry point execution context is different.
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from src.extensions import db # Assuming db is initialized in extensions.py

class DashboardCategory(db.Model):
    __tablename__ = 'dashboard_categories'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False, unique=True)
    # Use a more descriptive name for the relationship, like 'items_in_category'
    # and specify lazy='dynamic' if you expect many items and want to query them efficiently.
    items = db.relationship('DashboardItem', backref='category', lazy='dynamic', cascade="all, delete-orphan")

    def __repr__(self):
        return f'<DashboardCategory {self.title}>'

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'items': [item.to_dict() for item in self.items]
        }

class DashboardItem(db.Model):
    __tablename__ = 'dashboard_items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    percentage = db.Column(db.Integer, nullable=False)
    category_id = db.Column(db.Integer, db.ForeignKey('dashboard_categories.id'), nullable=False)

    def __repr__(self):
        return f'<DashboardItem {self.name} - {self.percentage}%>'

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'percentage': self.percentage,
            'category_id': self.category_id
        }

