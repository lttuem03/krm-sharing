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
    
    def update_viewcount(document: Document):
        document.view_count += 1

        db.session.commit()

    def update_downloadcount(document: Document):
        document.download_count += 1

        db.session.commit()

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
