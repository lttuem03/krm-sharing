from app.models import db
from flask_login import UserMixin

class User(db.Model, UserMixin):
    id = db.Column("id", db.Integer, nullable=False, primary_key=True) # _id means id is the primary key of the User table, is automatically created
    name = db.Column(db.Unicode(150), nullable=False, unique=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    username = db.Column(db.String(24), nullable=False, unique=True) # constraint: must be in between 5 to 24 characters
    hased_password = db.Column(db.String(64), nullable=False) # sha256 hashed passwords will always be 64 characters long
    
    # relationships
    documents = db.relationship('Document', backref='user', lazy=True)