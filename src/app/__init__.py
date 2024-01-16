from os import path
from flask import Flask

from app.controllers.controller_authentication import login_manager
#from .utils import get_uploader

from app.views import (HomeView,
                       LoginView,
                       LogoutView,
                       RegisterView,
                       UploadView,
                       DocumentManagementView,
                       DocumentDetailsView)

from app.models import db

from app.controllers.utils import get_uploader, kilobyte_to_megabyte, is_bookmarked_by_current_user, get_thumbnail_path

from .config import *

krm_app_instance = Flask(__name__, template_folder=".\\views\\templates",
                                    static_folder=".\\..\\static")

# Configs
krm_app_instance.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
krm_app_instance.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH_IN_MB * 1024 * 1024 # in bytes
krm_app_instance.config['SECRET_KEY'] = DB_SECRET_KEY
krm_app_instance.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'

# Init database instance
db.init_app(krm_app_instance)
with krm_app_instance.app_context():
    db.create_all()

# Registering views
krm_app_instance.add_url_rule("/", endpoint="home", view_func=HomeView.as_view("home"))
krm_app_instance.add_url_rule("/login/", endpoint="login", view_func=LoginView.as_view("login"))
krm_app_instance.add_url_rule("/logout/", endpoint="logout", view_func=LogoutView.as_view("logout"))
krm_app_instance.add_url_rule("/register/", endpoint="register", view_func=RegisterView.as_view("register"))
krm_app_instance.add_url_rule("/upload/", endpoint="upload", view_func=UploadView.as_view("upload"))
krm_app_instance.add_url_rule("/document/<int:id>", endpoint="document_details", view_func=DocumentDetailsView.as_view("document_details"))
krm_app_instance.add_url_rule("/managedocuments/", endpoint="document_management", view_func=DocumentManagementView.as_view("document_management"))

# Setting up flask-login
login_manager.login_view = "login"
login_manager.init_app(krm_app_instance)

# Registering utility function to use in the html templates
krm_app_instance.jinja_env.globals.update(get_uploader=get_uploader)
krm_app_instance.jinja_env.globals.update(kilobyte_to_megabyte=kilobyte_to_megabyte)
krm_app_instance.jinja_env.globals.update(is_bookmarked_by_current_user=is_bookmarked_by_current_user)
krm_app_instance.jinja_env.globals.update(get_thumbnail_path=get_thumbnail_path)