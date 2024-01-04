from flask import flash
from flask_login import (LoginManager,
                         login_user, 
                         logout_user)

from werkzeug.security import (check_password_hash,
                               generate_password_hash)

from app.models import db
from app.models.query_engine import QueryEngine
from app.models.model_user import User
from app.models.model_document import Document

from .utils import (check_email_availability,
                   check_username_availability,
                   validate_email,
                   validate_username,
                   validate_password)

# use for flask-login
login_manager = LoginManager()

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class AuthenticationController():
    @staticmethod
    def process_login(username_or_email, password, remember_me):
        """
        Validate a login attempt.
        
        Return an instance of logged in user if login was successful, otherwise return None
        """

        user = QueryEngine.query_User_by("username", username_or_email)

        if user == None:
            user = QueryEngine.query_User_by("email", username_or_email)

        if user == None:
            flash("Tên đăng nhập hoặc email không tồn tại", category="error")
            return None
    
        if check_password_hash(user.hased_password, password) == False:
            flash("Sai mật khẩu", category="error")
            return None
            
        flash("Đăng nhập thành công", category="success")
        login_user(user, remember=remember_me)
        
        return user
    
    @staticmethod
    def process_logout():
        """Log an user out"""
        logout_user()

    @staticmethod
    def process_register(name, email, username, password, repeat_password):
        """
        Validate a registration attempt

        Return an instance of new user if registering was successful, otherwise return None
        """
        
        all_checks_pass = validate_email(email) \
                            and check_email_availability(email) \
                            and validate_username(username) \
                            and check_username_availability(username) \
                            and validate_password(password, repeat_password)
        
        if all_checks_pass:
            new_user = User(name=name, email=email, username=username,
                            hased_password=generate_password_hash(password, method='pbkdf2'))
            db.session.add(new_user)
            db.session.commit()

            flash("Tạo tài khoản thành công! Xin hãy đăng nhập vào tài khoản mới của bạn.", category='success')
            
            return new_user

        return None