import datetime

from app.models import db

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

    # update rating: 
    #   rating = (rating * rating_count + new rate value) / (rating_count + 1)
    #   rating_count = rating_count + 1
    rating = db.Column(db.Float, nullable=False, unique=False, default=0)
    rating_count = db.Column(db.Integer, nullable=False, unique=False, default=0)