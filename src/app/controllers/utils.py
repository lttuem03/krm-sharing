import re

from flask import flash

from app.models.query_engine import QueryEngine
from app.models.model_document import Document
from ..config import ALLOWED_EXTENSIONS

def check_email_availability(email, msg="Email này đã được sử dụng, vui lòng chọn email khác"):
    user_by_email = QueryEngine.query_User_by("email", email)

    if user_by_email != None:
        flash(msg, category='error')
        return False
    
    return True

def check_username_availability(username, msg="Tên đăng nhập đã tồn tại, vui lòng chọn tên đăng nhập khác"):
    user_by_username = QueryEngine.query_User_by("username", username)

    if user_by_username != None:
        flash(msg, category="error")
        return False
    
    return True

def validate_email(email, msg="Email không hợp lệ, vui lòng thử lại"):
    email_pattern = r'^[\w\-\.]+@([\w-]+\.)+[\w-]{2,4}$'

    if re.match(email_pattern, email) == None:
        flash(msg, category='error')
        return False
    
    return True

def validate_username(username, minlen=5, maxlen=24):
    if len(username) < minlen or len(username) > maxlen:
        flash("Tên đăng nhập phải chứa từ {minlen} đến {maxlen} ký tự".format(minlen=minlen, maxlen=maxlen), category="error")
        return False
    
    return True
    
def validate_password(password, repeat_password, minlen=7):
    if password != repeat_password:
        flash("Mật khẩu nhập lại không khớp", category="error")
        return False

    if len(password) < minlen:
        flash("Mật khẩu phải chứa ít nhất {minlen} ký tự".format(minlen=minlen), category="error")
        return False

    return True

def allowed_file(filename: str):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def byte_to_kilobyte(in_bytes):
    return float(in_bytes / 1024)

def get_uploader(document: Document):
    uploader = QueryEngine.query_User_by("id", document.uploader_id)

    return uploader