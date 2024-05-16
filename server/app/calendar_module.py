from flask import Flask, request, jsonify
from flask_login import login_required
from app.models import Calendar
from app import db, app


@app.route('/calendar/<int:user_id>/<int:contact_id>', methods=['GET'])
@login_required
def get_calendar_items(user_id, contact_id):
    # Retrieve calendar items belonging to the contact id belonging to the user id
    calendar_items = Calendar.query.filter_by(user_id=user_id, contact_id=contact_id).all()
    
    # Convert calendar items to a list of dictionaries
    calendar_items_dict = [item.to_dict() for item in calendar_items]
    
    return jsonify(calendar_items_dict)

# Add other CRUD routes for create, update, and delete operations
@app.route('/calendar', methods=['POST'])
@login_required
def create_calendar_item():
    # Get the request data
    data = request.get_json()
    
    # Create a new calendar item
    new_item = Calendar(user_id=data['user_id'], contact_id=data['contact_id'], title=data['title'], description=data['description'])
    
    # Add the new item to the database
    db.session.add(new_item)
    db.session.commit()
    
    return jsonify(new_item.to_dict()), 201


@app.route('/calendar/<int:item_id>', methods=['PUT'])
@login_required
def update_calendar_item(item_id):
    # Get the request data
    data = request.get_json()
    
    # Find the calendar item to update
    item = Calendar.query.get(item_id)
    
    # Update the item properties
    item.title = data['title']
    item.description = data['description']
    
    # Commit the changes to the database
    db.session.commit()
    
    return jsonify(item.to_dict())


@app.route('/calendar/<int:item_id>', methods=['DELETE'])
@login_required
def delete_calendar_item(item_id):
    # Find the calendar item to delete
    item = Calendar.query.get(item_id)
    
    # Delete the item from the database
    db.session.delete(item)
    db.session.commit()
    
    return '', 204

if __name__ == '__main__':
    app.run()