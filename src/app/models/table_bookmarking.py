from app.models import db
from app.models.model_user import User
from app.models.model_document import Document

# KNOW THE DIFFERENCE BETWEEN A MODEL AND A TABLE

# This table is used to track which User has bookmarked which Document
# Relationship: Many to Many

class BookmarkingTable(db.Model):
    __tablename__ = "bookmarking_user_document"
    user_id = db.Column("user_id", db.Integer, db.ForeignKey(User.id), primary_key=True)
    document_id = db.Column("document_id", db.Integer, db.ForeignKey(Document.id), primary_key=True)