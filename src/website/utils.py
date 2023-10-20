import re

from flask import flash 

from .database import db, User

def check_email_availability(email, msg="Email này đã được sử dụng, vui lòng chọn email khác"):
    print("Checking email availability")
    user_by_email = User.query.filter_by(email=email).first()

    if user_by_email != None:
        flash(msg, category='error')
        print(msg)
        return False
    
    return True

def check_username_availability(username, msg="Tên đăng nhập đã tồn tại, vui lòng chọn tên đăng nhập khác"):
    print("Checking username availability")
    user_by_username = User.query.filter_by(username=username).first()

    if user_by_username != None:
        flash(msg, category="error")
        print(msg)
        return False
    
    return True

def validate_email(email, msg="Email không hợp lệ, vui lòng thử lại"):
    print("Validating email")
    email_pattern = r'^[\w\-\.]+@([\w-]+\.)+[\w-]{2,4}$'

    if re.match(email_pattern, email) == None:
        flash(msg, category='error')
        print(msg)
        return False
    
    return True

def validate_username(username):
    print("Validating username")
    if len(username) < 5 or len(username) > 24:
        flash("Tên đăng nhập phải chứa từ 5 đến 24 ký tự", category="error")
        return False
    
    return True
    
def validate_password(password, repeat_password):
    print("Validating password")
    if password != repeat_password:
        flash("Mật khẩu nhập lại không khớp", category="error")
        return False

    if len(password) < 7:
        flash("Mật khẩu phải chứa ít nhất 7 ký tự", category="error")
        return False

    return True