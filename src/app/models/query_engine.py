from flask_sqlalchemy.query import Query

from app.models.model_user import User
from app.models.model_document import Document
from app.models.model_listing import Listing
from app.models.table_bookmarking import BookmarkingTable

User_column_map = {"id": User.id,
                   "name": User.name,
                   "email": User.email,
                   "username": User.username,
                   "hashed_password": User.hashed_password}

Document_column_map = {"id": Document.id,
                       "name": Document.name,
                       "uploader_id": Document.uploader_id,
                       "date_uploaded": Document.date_uploaded,
                       "type": Document.type,
                       "subject": Document.subject,
                       "school": Document.school,
                       "author": Document.author,
                       "year": Document.year,
                       "description": Document.description,
                       "filename": Document.filename,
                       "file_size": Document.file_size,
                       "view_count": Document.view_count,
                       "download_count": Document.download_count,
                       "rating": Document.rating,
                       "rating_count": Document.rating_count}

Listing_column_map = {"id": Listing.id,
                      "name": Listing.name,
                      "post_id": Listing.post_id,
                      "date_posted": Listing.date_posted,
                      "doc_type": Listing.doc_type,
                      "subject": Listing.subject,
                      "school": Listing.school,
                      "author": Listing.author,
                      "year": Listing.year,
                      "description": Listing.description,
                      "status": Listing.status,
                      "price": Listing.price,
                      "location": Listing.location,
                      "filename": Listing.foldername,
                      "view_count": Listing.view_count,
                      "buy_count": Listing.buy_count,
                      "rating": Listing.rating,
                      "rating_count": Listing.rating_count}


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

    @staticmethod
    def query_Listing_by(column, value) -> Listing:
        """ Return row of the Listing query result """
        if column not in Listing_column_map:
            print("Listing query : Column not exists!")
            return None
        return Listing.query.filter(Listing_column_map[column] == value).first()

    @staticmethod
    def query_all_Listing_by(column, value) -> Query:
        """ Return all rows of the Listing query result """
        if column not in Listing_column_map:
            print("All Listing query: Column not exists!")
            return None

        return Listing.query.filter(Listing_column_map[column] == value)

    @staticmethod
    def query_Bookmarking_Table(user_id_value, document_id_value):
        return BookmarkingTable.query.filter(BookmarkingTable.user_id == user_id_value,
                                             BookmarkingTable.document_id == document_id_value).first()

    @staticmethod
    def query_Bookmarking_Table_filter_by_user_id(user_id_value):
        return BookmarkingTable.query.filter(BookmarkingTable.user_id == user_id_value)
