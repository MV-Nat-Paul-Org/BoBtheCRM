import unittest
from app import app, db
from models import User, Contact

class TestModels(unittest.TestCase):
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

    def test_user_create(self):
        # Test creating a new user
        user = User(email='test@example.com', password='password')
        db.session.add(user)
        db.session.commit()

        # Retrieve the user from the database
        user = User.query.filter_by(email='test@example.com').first()
        self.assertIsNotNone(user)
        self.assertEqual(user.email, 'test@example.com')
        self.assertEqual(user.password, 'password')

    def test_contact_create(self):
        # Test creating a new contact
        user = User(email='test@example.com', password='password')
        db.session.add(user)
        db.session.commit()

        contact = Contact(user_id=user.id, status='Active', name='John Doe', address='123 Main St', number='123-456-7890')
        db.session.add(contact)
        db.session.commit()

        # Retrieve the contact from the database
        contact = Contact.query.filter_by(name='John Doe').first()
        self.assertIsNotNone(contact)
        self.assertEqual(contact.status, 'Active')
        self.assertEqual(contact.name, 'John Doe')
        self.assertEqual(contact.address, '123 Main St')
        self.assertEqual(contact.number, '123-456-7890')

if __name__ == '__main__':
    unittest.main()

# Notes regarding my code:
# These test cases cover creating new users and contacts, 
# and then retrieving them from the database to ensure they were created correctly.