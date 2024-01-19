import os

from flask import Flask

from app.controllers.controller_authentication import login_manager

from app.views import (HomeView,
                       LoginView,
                       LogoutView,
                       RegisterView,
                       MyProfileView,
                       UserProfileView,
                       ChangeAvatarView,
                       ChangePasswordView,
                       UploadView,
                       DocumentManagementView,
                       DocumentDetailsView,
                       ListingView,
                       ListingDetailsView,
                       LiveSearchProcessingView,
                       SearchResults)

from app.models import db

from app.controllers.utils import (get_uploader,
                                   kilobyte_to_megabyte,
                                   is_bookmarked_by_current_user,
                                   get_thumbnail_path,
                                   get_num_uploaded,
                                   get_total_views,
                                   get_total_downloaded,
                                   get_average_rating,
                                   round_float,
                                   get_current_avatar_path,
                                   get_listing_thumbnail,
                                   get_image_list,get_postid)

from .config import *

# Create app instance
krm_app_instance = Flask(__name__, template_folder=".\\views\\templates",
                                    static_folder=".\\..\\static")

# Create neccessary paths
if os.path.exists(UPLOAD_FOLDER) == False:
    os.mkdir(UPLOAD_FOLDER)

if os.path.exists(DOCUMENT_THUMBNAIL_FOLDER) == False:
    os.mkdir(DOCUMENT_THUMBNAIL_FOLDER)

if os.path.exists(USER_AVATAR_FOLDER) == False:
    os.mkdir(USER_AVATAR_FOLDER)

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
krm_app_instance.add_url_rule("/profile/me", endpoint="my_profile", view_func=MyProfileView.as_view("my_profile"))
krm_app_instance.add_url_rule("/profile/<string:username>", endpoint="user_profile", view_func=UserProfileView.as_view("user_profile"))
krm_app_instance.add_url_rule("/profile/change_avatar", endpoint="change_avatar", view_func=ChangeAvatarView.as_view("change_avatar"))
krm_app_instance.add_url_rule("/profile/change_password", endpoint="change_password", view_func=ChangePasswordView.as_view("change_password"))

krm_app_instance.add_url_rule("/upload/", endpoint="upload", view_func=UploadView.as_view("upload"))
krm_app_instance.add_url_rule("/document/<int:id>", endpoint="document_details", view_func=DocumentDetailsView.as_view("document_details"))
krm_app_instance.add_url_rule("/manage_documents/", endpoint="document_management", view_func=DocumentManagementView.as_view("document_management"))
krm_app_instance.add_url_rule("/listing/", endpoint="create_listing", view_func=ListingView.as_view("create_listing"))
krm_app_instance.add_url_rule("/listing_details/<int:id>",endpoint='listing_details',view_func=ListingDetailsView.as_view("listing_details"))

krm_app_instance.add_url_rule("/livesearch", endpoint="livesearch", view_func=LiveSearchProcessingView.as_view("livesearch"))
krm_app_instance.add_url_rule("/search_results/keywords=<string:search_text>", endpoint="search_results", view_func=SearchResults.as_view("search_results"))

# Setting up flask-login
login_manager.login_view = "login"
login_manager.init_app(krm_app_instance)

# Registering utility function to use in the html templates
krm_app_instance.jinja_env.globals.update(get_uploader=get_uploader)
krm_app_instance.jinja_env.globals.update(kilobyte_to_megabyte=kilobyte_to_megabyte)
krm_app_instance.jinja_env.globals.update(is_bookmarked_by_current_user=is_bookmarked_by_current_user)
krm_app_instance.jinja_env.globals.update(get_thumbnail_path=get_thumbnail_path)
krm_app_instance.jinja_env.globals.update(get_num_uploaded=get_num_uploaded)
krm_app_instance.jinja_env.globals.update(get_total_views=get_total_views)
krm_app_instance.jinja_env.globals.update(get_total_downloaded=get_total_downloaded)
krm_app_instance.jinja_env.globals.update(get_average_rating=get_average_rating)
krm_app_instance.jinja_env.globals.update(round_float=round_float)
krm_app_instance.jinja_env.globals.update(get_current_avatar_path=get_current_avatar_path)
krm_app_instance.jinja_env.globals.update(get_listing_thumbnail=get_listing_thumbnail)
krm_app_instance.jinja_env.globals.update(get_listing_thumbnail=get_listing_thumbnail)
krm_app_instance.jinja_env.globals.update(get_image_list=get_image_list)
krm_app_instance.jinja_env.globals.update(
    get_postid=get_postid)
