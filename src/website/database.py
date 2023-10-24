import datetime

from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()
DB_NAME = "database.db"

class User(db.Model, UserMixin):
    id = db.Column("id", db.Integer, nullable=False, primary_key=True) # _id means id is the primary key of the User table, is automatically created
    name = db.Column(db.Unicode(150), nullable=False, unique=False)
    role = db.Column(db.Unicode(26), nullable=True, unique=False)
    school = db.Column(db.Unicode(150), nullable=True, unique=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    username = db.Column(db.String(24), nullable=False, unique=True) # constraint: must be in between 5 to 24 characters
    hpassword = db.Column(db.String(64), nullable=False) # sha256 hashed passwords will always be 64 characters long
    
    # relationships
    documents = db.relationship('Document', backref='user', lazy=True)

class Document(db.Model):
    id = db.Column("id", db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.Unicode(120), nullable=False, unique=False)
    uploader_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_uploaded = db.Column(db.DateTime, nullable=False, unique=False, default=datetime.datetime.now())
    type = db.Column(db.Unicode(24), nullable=True, unique=False)
    subject = db.Column(db.Unicode(128), nullable=True, unique=False)
    school = db.Column(db.Unicode(150), nullable=True, unique=False)
    year = db.Column(db.Integer, nullable=True, unique=False)
    url = db.Column(db.String(256), nullable=False, unique=True)
    # statistics
    file_size = db.Column(db.Float, nullable=False, unique=False)
    view_count = db.Column(db.Integer, nullable=False, unique=False, default=0)
    download_count = db.Column(db.Integer, nullable=False, unique=False, default=0)
    one_star_rating = db.Column(db.Integer, nullable=False, unique=False, default=0)
    two_star_rating = db.Column(db.Integer, nullable=False, unique=False, default=0)
    three_star_rating = db.Column(db.Integer, nullable=False, unique=False, default=0)
    four_star_rating = db.Column(db.Integer, nullable=False, unique=False, default=0)
    five_star_rating = db.Column(db.Integer, nullable=False, unique=False, default=0)