import os

from flask import (request,
                   flash)

from flask_login import current_user

from werkzeug.utils import secure_filename

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