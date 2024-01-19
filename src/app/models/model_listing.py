import datetime


from app.models import db


class Listing(db.Model):
    id = db.Column("id", db.Integer, nullable=False, primary_key=True)
    name = db.Column(db.Unicode(120), nullable=False, unique=False)
    post_id = db.Column(
        db.Integer, db.ForeignKey('user.id'), nullable=False)
    date_posted = db.Column(
        db.DateTime, nullable=False, unique=False, default=datetime.datetime.now())
    subject = db.Column(db.Unicode(100), nullable=True, unique=False)
    school = db.Column(db.Unicode(100), nullable=True, unique=False)
    author = db.Column(db.Unicode(64), nullable=True, unique=False)
    year = db.Column(db.Integer, nullable=True, unique=False)
    description = db.Column(db.Unicode(200), nullable=True,
                            unique=False, default="<Mô tả trống>")
    amount = db.Column(db.Integer,nullable=False,unique=False,default=1)
    status = db.Column(db.Unicode(12), nullable=False, unique=False, default="Mới")
    price = db.Column(db.Integer, nullable=False, unique=False, default=0)
    location = db.Column(db.Unicode(50), nullable=False, unique=False, default='')
    # image folder [krm-id] + (tên tài liệu)
    foldername = db.Column(db.String(256), nullable=False,
                           unique=True, default='')
    # statistics
    view_count = db.Column(db.Integer, nullable=False, unique=False, default=0)

    # update rating:
    #   rating = (rating * rating_count + new rate value) / (rating_count + 1)
    #   rating_count = rating_count + 1
    rating = db.Column(db.Float, nullable=False, unique=False, default=0)
    rating_count = db.Column(
        db.Integer, nullable=False, unique=False, default=0)
