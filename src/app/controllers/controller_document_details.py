
from app.models import db
from app.models.model_document import Document
from app.models.query_engine import QueryEngine

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