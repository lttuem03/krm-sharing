from flask_login import current_user

from app.models import db
from app.models.model_document import Document
from app.models.table_bookmarking import BookmarkingTable
from app.models.query_engine import QueryEngine

from .utils import is_bookmarked_by_current_user

class DocumentDetailsController():
    @staticmethod
    def get_document(id):
        document = QueryEngine.query_Document_by("id", id)

        return document
    
    @staticmethod
    def update_viewcount(document: Document):
        document.view_count += 1

        db.session.commit()

    @staticmethod
    def update_downloadcount(document: Document):
        document.download_count += 1

        db.session.commit()

    @staticmethod
    def change_bookmark_state(document: Document):
        bookmark_entry = QueryEngine.query_Bookmarking_Table(current_user.id, document.id)

        # bookmarked -> unbookmarking
        if bookmark_entry != None:
            db.session.delete(bookmark_entry)
            db.session.commit()
            return
        
        # unbookmarked -> bookmarking
        db.session.add(BookmarkingTable(user_id=current_user.id, document_id=document.id))
        db.session.commit()
        return

    @staticmethod
    def update_rating(document, added_rating_value):
        new_rating = (document.rating * document.rating_count + added_rating_value) / (document.rating_count + 1)
        document.rating = new_rating
        document.rating_count = document.rating_count + 1

        db.session.commit()