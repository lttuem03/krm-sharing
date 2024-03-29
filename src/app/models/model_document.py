import datetime

from app.models import db

class Document(db.Model):
    id = db.Column("id", db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.Unicode(120), nullable=False, unique=False)
    uploader_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_uploaded = db.Column(db.DateTime, nullable=False, unique=False, default=datetime.datetime.now())
    type = db.Column(db.Unicode(24), nullable=True, unique=False)
    subject = db.Column(db.Unicode(100), nullable=True, unique=False)
    school = db.Column(db.Unicode(100), nullable=True, unique=False)
    author = db.Column(db.Unicode(64), nullable=True, unique=False)
    year = db.Column(db.Integer, nullable=True, unique=False)
    description = db.Column(db.Unicode(200), nullable=True, unique=False, default="<Mô tả trống>")
    filename = db.Column(db.String(256), nullable=False, unique=True, default="") # format: "[krm-(id)] (the original file name)" 
                                                                      # we pad ids to distinguish files with the same name
    # statistics
    file_size = db.Column(db.Float, nullable=False, unique=False, default=0)
    view_count = db.Column(db.Integer, nullable=False, unique=False, default=0)
    download_count = db.Column(db.Integer, nullable=False, unique=False, default=0)

    # update rating: 
    #   rating = (rating * rating_count + new rate value) / (rating_count + 1)
    #   rating_count = rating_count + 1
    rating = db.Column(db.Float, nullable=False, unique=False, default=0)
    rating_count = db.Column(db.Integer, nullable=False, unique=False, default=0)