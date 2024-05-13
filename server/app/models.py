from config import db

class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    status = db.Column(db.String(80), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200))
    number = db.Column(db.String(20))
    meetings = db.Column(db.String(200))
    transactions = db.Column(db.String(200))
    details = db.Column(db.Text)
 
    def to_json(self):
        return {
            "id": self.id,
            "status": self.status,
            "name": self.name,
            "address": self.address,
            "number": self.number,
            "meetings": self.meetings,
            "transactions": self.transactions,
            "details": self.details
        }

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)    
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    database_owner_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    # Add a relationship to represent the user's database
    database = db.relationship('User', remote_side=[id])

    def to_json(self):
        return {
            "id": self.id,
            "email": self.email,
            "password": self.password,
            "is_admin": self.is_admin
        }

# NOTES REGARDING MY CODE : 
# Each User has a database_owner_id field, which refers to the user who owns the database. This allows for separating databases between different users.
# A relationship database is established in the User model to represent the user's database. This allows for easy querying of a user's database.
# The Contact model has a user_id field, which refers to the user who owns the contact. This ensures that contacts are associated with their respective users.