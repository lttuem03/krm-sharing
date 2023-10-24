import re

from flask import flash 

from .database import db, User

UPLOAD_FOLDER = 'D:\krm_file_server_haha'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx', 'doc', 'pptx', 'ppt'}

def check_email_availability(email, msg="Email này đã được sử dụng, vui lòng chọn email khác"):
    user_by_email = User.query.filter_by(email=email).first()

    if user_by_email != None:
        flash(msg, category='error')
        print(msg)
        return False
    
    return True

def check_username_availability(username, msg="Tên đăng nhập đã tồn tại, vui lòng chọn tên đăng nhập khác"):
    user_by_username = User.query.filter_by(username=username).first()

    if user_by_username != None:
        flash(msg, category="error")
        print(msg)
        return False
    
    return True

def validate_email(email, msg="Email không hợp lệ, vui lòng thử lại"):
    email_pattern = r'^[\w\-\.]+@([\w-]+\.)+[\w-]{2,4}$'

    if re.match(email_pattern, email) == None:
        flash(msg, category='error')
        print(msg)
        return False
    
    return True

def validate_username(username):
    if len(username) < 5 or len(username) > 24:
        flash("Tên đăng nhập phải chứa từ 5 đến 24 ký tự", category="error")
        return False
    
    return True
    
def validate_password(password, repeat_password):
    if password != repeat_password:
        flash("Mật khẩu nhập lại không khớp", category="error")
        return False

    if len(password) < 7:
        flash("Mật khẩu phải chứa ít nhất 7 ký tự", category="error")
        return False

    return True

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS