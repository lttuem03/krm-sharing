from flask_sqlalchemy.query import Query

from app.models.model_user import User
from app.models.model_document import Document

User_column_map = { "id": User.id,
                    "name": User.name,
                    "email": User.email,
                    "username": User.username,
                    "hased_password": User.hased_password }

Document_column_map = { "id": Document.id,
                        "name": Document.name,
                        "uploader_id": Document.uploader_id,
                        "date_uploaded": Document.date_uploaded,
                        "type": Document.type,
                        "subject": Document.subject,
                        "school": Document.school,
                        "year": Document.year,
                        "file_size": Document.file_size,
                        "view_count": Document.view_count,
                        "download_count": Document.download_count,
                        "rating": Document.rating,
                        "rating_count": Document.rating_count}

class QueryEngine():
    @staticmethod
    def query_User_by(column, value) -> User:
        """ Return the first row of the User query result """
        if column not in User_column_map:
            print("User query: Column not exists!")
            return None
        
        return User.query.filter(User_column_map[column] == value).first()

    @staticmethod
    def query_Users_by(column, value) -> Query:
        """ Return all rows of the User query result """
        if column not in User_column_map:
            print("Users query: Column not exists!")
            return None
        
        return User.query.filter(User_column_map[column] == value)

    @staticmethod
    def query_Document_by(column, value) -> Document:
        """ Return the first row of the Document query result """
        if column not in Document_column_map:
            print("Document query: Column not exists!")
            return None
        
        return Document.query.filter(Document_column_map[column] == value).first()
    
    @staticmethod
    def query_Documents_by(column, value) -> Query:
        """ Return all rows of the Document query result """
        if column not in Document_column_map:
            print("Documents query: Column not exists!")
            return None
        
        return Document.query.filter(Document_column_map[column] == value)