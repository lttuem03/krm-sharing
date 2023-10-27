from os import path
from flask import Flask

from .views import views
from .database import db, DB_NAME, User
from .auth import login_manager
from .config import UPLOAD_FOLDER
from .utils import get_uploader

def app_instance():
    app = Flask(__name__)
    
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # handle up to 16Mb per upload

    app.config['SECRET_KEY'] = 'IEkgYW0gdGhlIGJvbmUgb2YgbXkgc3dvcmQKIFN0ZWVsIGlzIG15IGJvZHkgYW5kIGZpcmUgaXMgbXkgYmxvb2QKIEkgaGF2ZSBjcmVhdGVkIG92ZXIgYSB0aG91c2FuZCBibGFkZXMKIFVua25vd24gdG8gRGVhdGgsCiBOb3Iga25vd24gdG8gTGlmZS4KIEhhdmUgd2l0aHN0b29kIHBhaW4gdG8gY3JlYXRlIG1hbnkgd2VhcG9ucwogQnV0IHlldCwgdGhvc2UgaGFuZHMgd2lsbCBuZXZlciBob2xkIGFueXRoaW5nCiBTbyBhcyBJIHByYXksIFVubGltaXRlZCBCbGFkZSBXb3Jrcy4='
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)
    with app.app_context():
        db.create_all()

    app.register_blueprint(views, url_prefix='/')
    app.jinja_env.globals.update(get_uploader=get_uploader)

    login_manager.login_view = 'views.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app