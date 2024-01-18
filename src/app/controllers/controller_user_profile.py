import os

from flask import (request,
                   flash)

from flask_login import current_user

from werkzeug.utils import secure_filename
from werkzeug.security import (check_password_hash,
                               generate_password_hash)

from app.models import db
from app.models.model_user import User
from app.models.query_engine import QueryEngine

from .utils import allowed_file

from ..config import USER_AVATAR_FOLDER

class UserProfileController():
    @staticmethod
    def get_user(user_id) -> (None | User):
        return QueryEngine.query_User_by("id", user_id)
    
    @staticmethod
    def process_change_avatar():
        """
        Process an attempt to change user's avatar

        Return True if succeed, otherwise return False
        """
        if "file" not in request.files:
            flash("No file part in request")
            return False
        
        file = request.files["file"]

        if file.filename == "":
            flash("Xin hãy chọn một file ảnh đại diện để tải lên.", category="error")
            return False
        
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)

            id_padded_filename = "[user-{id:0>5}]_avatar.jpg".format(id=str(current_user.id)) # format: "[user-00001]_avatar.jpg"

            file.save(os.path.join(os.path.dirname(__file__), USER_AVATAR_FOLDER, filename))

            if os.path.exists(os.path.join(os.path.dirname(__file__), USER_AVATAR_FOLDER, id_padded_filename)):
                os.remove(os.path.join(os.path.dirname(__file__), USER_AVATAR_FOLDER, id_padded_filename))

            os.rename(os.path.join(os.path.dirname(__file__), USER_AVATAR_FOLDER, filename), 
                      os.path.join(os.path.dirname(__file__), USER_AVATAR_FOLDER, id_padded_filename))

            flash("Đổi ảnh đại diện thành công", category="success")
            return True
        
    @staticmethod
    def process_change_password(current_password, new_password, confirm_new_password):
        """
        Process an attempt to change user's password

        Return True if succeed, otherwise return False
        """
        user = QueryEngine.query_User_by("email", current_user.email)

        if check_password_hash(user.hashed_password, current_password) == False:
            flash("Sai mật khẩu", category="error")
            return False
        
        if new_password != confirm_new_password:
            flash("Mật khẩu nhập lại không khớp", category="error")
            return False
        
        # success
        user.hashed_password = generate_password_hash(new_password, method='pbkdf2')
        db.session.commit()
        return True