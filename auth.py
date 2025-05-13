# /home/ubuntu/dashboard_with_admin/dashboard_backend/src/auth.py
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from flask_httpauth import HTTPBasicAuth
from werkzeug.security import generate_password_hash, check_password_hash

auth = HTTPBasicAuth()

# In a real application, store these securely, e.g., in environment variables or a database.
# For this example, we'll define them here. Consider this a placeholder.
ADMIN_USERNAME = os.environ.get("ADMIN_USERNAME", "admin")
ADMIN_PASSWORD_HASH = os.environ.get("ADMIN_PASSWORD_HASH", generate_password_hash("securepassword123"))

users = {
    ADMIN_USERNAME: ADMIN_PASSWORD_HASH
}

@auth.verify_password
def verify_password(username, password):
    if username in users and \
            check_password_hash(users.get(username), password):
        return username
    return None

