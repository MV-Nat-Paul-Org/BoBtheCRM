# Import necessary modules
from flask import jsonify, request, session, redirect, url_for
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from . import app, db  # Import Flask app and SQLAlchemy instance
from .models import User, Contact  # Import your User and Contact models

# Define routes
@app.route('/dashboard', methods=['GET'])
@login_required
def client_dashboard():
    # Fetch all contacts for the current user
    contacts = Contact.query.filter_by(user_id=current_user.id).all()
    return jsonify([contact.to_dict() for contact in contacts])

@app.route('/contacts', methods=['GET'])
@login_required
def get_all_contacts():
    # Fetch all contacts for the current user
    contacts = Contact.query.filter_by(user_id=current_user.id).all()
    return jsonify([contact.to_dict() for contact in contacts])

@app.route('/user', methods=['GET'])
@login_required
def get_user_with_token():
    # Return the current user's information
    return jsonify(current_user.to_dict())

@app.route('/contacts/<int:id>', methods=['GET'])
@login_required
def get_contact_by_id(id):
    # Fetch the contact with the given ID
    contact = Contact.query.get(id)
    return jsonify(contact.to_dict())

@app.route('/contacts', methods=['POST'])
@login_required
def create_contact():
    # Extract data from the request
    data = request.json
    name = data.get('name')
    email = data.get('email')
    phone_number = data.get('phone_number')
    details = data.get('details')
    status = data.get('status')
    permissions = data.get('permissions')

    # Check if required fields are provided
    if not name or not email:
        return jsonify({"message": "Name and email are required"}), 400

    # Create a new contact
    new_contact = Contact(
        user_id=current_user.id,
        name=name,
        email=email,
        phone_number=phone_number,
        details=details,
        status=status,
        permissions=permissions
    )

    # Add the new contact to the database
    db.session.add(new_contact)
    db.session.commit()

    return jsonify({"message": "Contact created successfully", "contact_id": new_contact.id}), 201

@app.route('/contacts/<int:id>', methods=['DELETE'])
@login_required
def delete_contact(id):
    # Fetch the contact from the database
    contact = Contact.query.get(id)

    # Check if the contact exists
    if not contact:
        return jsonify({"message": "Contact not found"}), 404

    # Check if the logged-in user is the owner of the contact
    if contact.user_id != current_user.id:
        abort(403, "You are not authorized to delete this contact")

    # Delete the contact
    db.session.delete(contact)
    db.session.commit()

    return jsonify({"message": "Contact deleted successfully"}), 200

@app.route('/admin/users', methods=['GET'])
@login_required
def get_all_users():
    # Fetch all users (admin only)
    if not current_user.is_admin:
        abort(403, "You are not authorized to view this page.")
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])
