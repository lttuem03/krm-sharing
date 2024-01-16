import os

from flask import (flash,
                   Request)
from flask_login import current_user

from werkzeug.utils import secure_filename

from app.models import db
from app.models.model_document import Document
from app.models.query_engine import QueryEngine

from .utils import (allowed_file,
                    byte_to_kilobyte,
                    create_and_save_thumbmail)

from ..config import UPLOAD_FOLDER

class DocumentManagementController():
    @staticmethod
    def process_upload(request: Request, document_name, document_description, document_type, document_subject, document_author, document_year, document_school) -> bool:
        """
        Process a file upload attempt.
        
        Return the instance of the newly uploaded Document if successful, otherwise return None 
        """

        if "file" not in request.files:
            flash("No file part in request")
            return None
        
        file = request.files["file"]

        # Check whether the user has selected a file from their local machine
        if file.filename == "":
            flash("Xin hãy chọn một tài liệu để tải lên.", category="error")
            return None
        
        # Check whether the required fields are empty
        if document_name == "":
            flash("Vui lòng nhập tên tài liệu.", category="error")
            return None

        if document_type == "Chọn loại tài liệu":
            flash("Vui lòng chọn loại tài liệu.", category="error")
            return None
        
        if document_subject == "":
            flash("Vui lòng điền tên môn học/chủ đề của tài liệu.", category="error")
            return None

        # Setting the unrequired fields None if they are empty
        if document_description == "":
            document_description = None

        if document_school == "":
            document_school = None
        
        if document_year == "":
            document_year = None

        if document_author == "":
            document_author = None

        # Attempt upload
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            new_document = Document(name=document_name,
                                    description=document_description,
                                    uploader_id=current_user.id, 
                                    type=document_type,
                                    subject=document_subject,
                                    author=document_author,
                                    school=document_school,
                                    year=document_year)
            
            db.session.add(new_document)
            db.session.commit()

            # padding filename with id (to distinguish between documents with the same file name)
            filename = "[krm-{id:0>5}] {original}".format(id=str(new_document.id), original=filename)

            # actually saving the file to the file server
            save_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(save_path)

            # try creating thumbnail for preview (if fail, use the 'preview not available' thumbnail)
            try:
                create_and_save_thumbmail(filename)
            except:
                pass
                
            # update values in database
            new_document.filename = filename

            document_filesize = byte_to_kilobyte(os.stat(save_path).st_size)
            new_document.file_size = document_filesize

            db.session.commit()

            flash("Tải tài liệu lên thành công!", category="success")
            return new_document
        
        flash("Tải tài liệu lên thất bại. Đã có lỗi xảy ra.", category="error")
        return None
    
    def get_uploaded(user_id):
        return QueryEngine.query_Documents_by("uploader_id", user_id)

    def get_bookmarked(user_id):
        bookmark_entrys = QueryEngine.query_Bookmarking_Table_filter_by_user_id(user_id)

        bookmarked = []
        for entry in bookmark_entrys:
            query_document = QueryEngine.query_Document_by("id", entry.document_id)

            if query_document != None:
                bookmarked.append(query_document)

        return bookmarked