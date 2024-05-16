import unittest
from flask import Flask
from ..app import app, db
from server.app.models import User, Contact, Transaction  

class TransactionTestCase(unittest.TestCase):
    def setUp(self):
        self.app = app
        self.client = self.app.test_client()
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

        # Create a test user and contact
        self.user = User(email='test@test.com', password_hash='hashed_password')
        db.session.add(self.user)
        db.session.commit()

        self.contact = Contact(name='Test Contact', user_id=self.user.id)
        db.session.add(self.contact)
        db.session.commit()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_get_transactions(self):
        # Log in as the test user
        with self.client.session_transaction() as session:
            session['user_id'] = self.user.id

        response = self.client.get(f'/contact/{self.contact.id}/transactions')
        self.assertEqual(response.status_code, 200)

    def test_create_transaction(self):
        # Log in as the test user
        with self.client.session_transaction() as session:
            session['user_id'] = self.user.id

        response = self.client.post(f'/contact/{self.contact.id}/transactions', data={'amount': 100})
        self.assertEqual(response.status_code, 201)

if __name__ == '__main__':
    unittest.main()
