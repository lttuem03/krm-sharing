import os

from flask import (flash,
                   Request)
from flask_login import current_user

from werkzeug.utils import secure_filename

from app.models.model_document import Document
from app.models import db

from .utils import (allowed_file,
                    byte_to_kilobyte)
from ..config import UPLOAD_FOLDER

class DocumentManagementController():
    @staticmethod
    def process_upload(request: Request, document_name, document_type, document_subject, document_year, document_school) -> bool:
        """
        Process a file upload attempt.
        
        Return a boolean as for whether the upload was successful or not 
        """

        if "file" not in request.files:
            flash("No file part in request")
            return False
        
        file = request.files["file"]

        # Check whether the user has selected a file from their local machine
        if file.filename == "":
            flash("Xin hãy chọn một tài liệu để tải lên.", category="error")
            return False
        
        # Check whether the required fields are empty
        if document_name == "":
            flash("Vui lòng nhập tên tài liệu.", category="error")
            return False

        if document_type == "Chọn loại tài liệu":
            flash("Vui lòng chọn loại tài liệu.", category="error")
            return False
        
        if document_subject == "":
            flash("Vui lòng điền tên môn học/chủ đề của tài liệu.", category="error")
            return False
        
        # Setting the unrequired fields None if they are empty
        if document_school == "":
            document_school = None
        
        if document_year == "":
            document_year = None

        # Attempt upload
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            new_document = Document(name=document_name, 
                                    uploader_id=current_user.id, 
                                    type=document_type,
                                    subject=document_subject,
                                    school=document_school,
                                    year=document_year)
            
            db.session.add(new_document)
            db.session.commit()

            # padding filename with id (to distinguish between documents with the same file name)
            filename = "[krm-{id:0>5}] {original}".format(id=str(new_document.id), original=filename)

            print("uploading " + filename)

            # actually saving the file to the file server
            save_path = os.path.join(UPLOAD_FOLDER, filename)
            file.save(save_path)

            # update values in database
            new_document.filename = filename

            document_filesize = byte_to_kilobyte(os.stat(save_path).st_size)
            new_document.file_size = document_filesize

            db.session.commit()

            flash("Tải tài liệu lên thành công!", category="success")
            return True
        
        flash("Tải tài liệu lên thất bài. Đã có lỗi xảy ra.", category="error")
        return False