import unittest
import json
from app import app, db
from models import User, Contact

class TestRoutes(unittest.TestCase):
    def setUp(self):
        # Set up the app context and create a test database
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
        app.config['TESTING'] = True
        self.app = app.test_client()
        with app.app_context():
            db.create_all()

    def tearDown(self):
        # Clean up the test database
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def test_user_registration(self):
        # Test user registration route
        data = {'email': 'test@example.com', 'password': 'password'}
        response = self.app.post('/users', json=data)
        self.assertEqual(response.status_code, 200)

        # Check if the user was created in the database
        user = User.query.filter_by(email='test@example.com').first()
        self.assertIsNotNone(user)

    def test_contact_creation(self):
        # Create a user for authentication
        user = User(email='test@example.com', password='password')
        db.session.add(user)
        db.session.commit()

        # Test contact creation route
        data = {'status': 'Active', 'name': 'John Doe', 'address': '123 Main St', 'number': '123-456-7890'}
        headers = {'Authorization': 'Bearer token'}  # Replace 'token' with a valid JWT token
        response = self.app.post('/contacts', json=data, headers=headers)
        self.assertEqual(response.status_code, 201)

        # Check if the contact was created in the database
        contact = Contact.query.filter_by(name='John Doe').first()
        self.assertIsNotNone(contact)

if __name__ == '__main__':
    unittest.main()

#NOTES REGARDING MY CODE : 
# These test cases cover registering a new user and creating a new contact via the API routes. 
# Make sure to replace 'token' in the headers dictionary with a valid JWT token for authenticated routes. 
