from flask import Blueprint, jsonify, request
from flask_login import login_required, current_user
from .models import Contact, Transaction
from .models import db
# test_transactions.py
from server.bootstrap import app, db

# Create a blueprint for transactions
transactions_bp = Blueprint('transactions', __name__)

# Define the CRUD routes for transactions
@transactions_bp.route('/contact/<int:contact_id>/transactions', methods=['GET'])
@login_required
def get_transactions(contact_id):
    # Check if the contact belongs to the current user
    contact = Contact.query.filter_by(id=contact_id, user_id=current_user.id).first()
    if not contact:
        return jsonify({'message': 'Contact not found'}), 404

    # Retrieve transactions for the given contact_id
    transactions = Transaction.query.filter_by(contact_id=contact_id).all()
    return jsonify(transactions)

# Rest of the routes...
@transactions_bp.route('/contact/<int:contact_id>/transactions', methods=['POST'])
@login_required
def create_transaction(contact_id):
    # Check if the contact belongs to the current user
    contact = Contact.query.filter_by(id=contact_id, user_id=current_user.id).first()
    if not contact:
        return jsonify({'message': 'Contact not found'}), 404

    # Validate input data
    data = request.get_json()
    if not data or 'amount' not in data or 'description' not in data:
        return jsonify({'message': 'Invalid input data'}), 400

    # Create a new transaction
    transaction = Transaction(
        contact_id=contact_id,
        amount=data['amount'],
        description=data['description']
    )
    db.session.add(transaction)
    db.session.commit()
    return jsonify(transaction), 201

@transactions_bp.route('/transactions/<int:transaction_id>', methods=['GET'])
@login_required
def get_transaction(transaction_id):
    # Check if the transaction belongs to the current user
    transaction = Transaction.query.filter_by(id=transaction_id).first()
    if not transaction:
        return jsonify({'message': 'Transaction not found'}), 404
    return jsonify(transaction)

@transactions_bp.route('/transactions/<int:transaction_id>', methods=['PUT'])
@login_required
def update_transaction(transaction_id):
    # Check if the transaction belongs to the current user
    transaction = Transaction.query.filter_by(id=transaction_id).first()
    if not transaction:
        return jsonify({'message': 'Transaction not found'}), 404

    # Validate input data
    data = request.get_json()
    if not data or ('amount' not in data and 'description' not in data):
        return jsonify({'message': 'Invalid input data'}), 400

    # Update the transaction
    if 'amount' in data:
        transaction.amount = data['amount']
    if 'description' in data:
        transaction.description = data['description']
    db.session.commit()
    return jsonify(transaction)

@transactions_bp.route('/transactions/<int:transaction_id>', methods=['DELETE'])
@login_required
def delete_transaction(transaction_id):
    # Check if the transaction belongs to the current user
    transaction = Transaction.query.filter_by(id=transaction_id).first()
    if not transaction:
        return jsonify({'message': 'Transaction not found'}), 404

    # Delete the transaction
    db.session.delete(transaction)
    db.session.commit()
    return jsonify({'message': 'Transaction deleted'})
