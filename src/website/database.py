from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()
DB_NAME = "database.db"

class User(db.Model, UserMixin):
    _id = db.Column("id", db.Integer, nullable=False, primary_key=True) # _id means id is the primary key of the User table, is automatically created
    name = db.Column(db.Unicode(150), nullable=False, unique=False)
    role = db.Column(db.Unicode(26), nullable=True, unique=False)
    school = db.Column(db.Unicode(150), nullable=True, unique=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    username = db.Column(db.String(24), nullable=False, unique=True) # constraint: must be in between 5 to 24 characters
    hpassword = db.Column(db.String(64), nullable=False) # sha256 hashed passwords will always be 64 characters long
    
    def __init__(self, name, role, school, email, username, hpassword):
        self.name = name
        self.role = role
        self.school = school
        self.email = email
        self.username = username
        self.hpassword = hpassword