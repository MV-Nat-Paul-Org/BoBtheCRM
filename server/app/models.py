<<<<<<< HEAD
# database models
=======
from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from . import db

class Contact(db.Model):
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    status = Column(String(80), nullable=False)
    name = Column(String(100), nullable=False)
    addresses = db.relationship('Address', backref='contact', cascade='all, delete-orphan')
    email = Column(String(255))
    phone_number = Column(String(20))
    details = Column(Text)
    events = db.relationship('CalendarEvent', backref='contact', cascade='all, delete-orphan')
    permissions = Column(String(20), nullable=False, default='Private')

    def to_json(self):
        return {
            "id": self.id,
            "status": self.status,
            "name": self.name,
            "address": self.address,
            "email": self.email,
            "phone_number": self.phone_number,
            "meetings": self.meetings,
            "details": self.details,
            "permissions": self.permissions
        }
        
class Address(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'), nullable=False)
    street = db.Column(db.String(200))
    apt_number = db.Column(db.String(20))
    city = db.Column(db.String(100))
    state = db.Column(db.String(50))
    zip_code = db.Column(db.String(20))
        

class Transaction(db.Model):
    id = Column(Integer, primary_key=True)
    contact_id = Column(Integer, ForeignKey('contact.id'), nullable=False)
    date = Column(String(20), nullable=False)
    amount = Column(Integer, nullable=False)
    description = Column(Text)
    category = Column(String(50))
    payment_method = Column(String(50))
    notes = Column(Text)

class User(db.Model):
    id = Column(Integer, primary_key=True)    
    email = Column(String(255), nullable=False, unique=True)
    # using OAuth, need password_hash field
    password_hash = Column(String(80), nullable=False)

    def get_user_id(self):
        return self.id


class CalendarEvent(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, db.ForeignKey('contact.id'), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    location = db.Column(db.String(200))
>>>>>>> 11d89ac (Refactor code structure and add comments)
