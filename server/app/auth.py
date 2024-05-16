import re 
from flask import Blueprint, jsonify, request, session, redirect, url_for, app
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from .models import db, User
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

limiter = Limiter(app, key_func=get_remote_address)

auth = Blueprint('auth', __name__)

# Regular expression pattern to match at least one special character
SPECIAL_CHAR_PATTERN = r'[!@#$%^&*()_+{}|:"<>?]'

@limiter.limit("10 per minute")
@auth.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Retrieve the user from the database by email
        user = User.query.filter_by(email=email).first()
        
        # Verify Pw using Bcrypt
        if user and check_password_hash(user.password_hash, password):
            login_user(user)  # Log in the user
            return redirect(url_for('api.client_dashboard'))  # Redirect to client dashbaord endpoint
        else:
            return jsonify({"message": "Invalid email or password"}), 401

@limiter.limit("5 per minute")
@auth.route('/signup', methods=['POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
         # Check if email and password are provided
        if not email or not password:
            return jsonify({"message": "Email and password are required"}), 400
        
         # Check if the password meets the strength requirements
        if len(password) < 8 or not re.search(SPECIAL_CHAR_PATTERN, password):
            return jsonify({"message": "Password must be at least 8 characters long and contain at least one special character"}), 400
        
        # Check if the user already exists
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            return jsonify({"message": "User already exists"}), 400
        
        # Hash PW using Bcrypt
        hashed_password = generate_password_hash(password)
        
        # Create a new user with hashed PW
        new_user = User(email=email, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        
        login_user(new_user)  # Log in the newly created user
        
        return redirect(url_for('api.client_dashboard'))  # Redirect to client dashboard endpoint

@auth.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()  # Log out the current user
    return jsonify({"message": "Logged out successfully"})