from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
DB_NAME = "database.db"

def launch_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'IEkgYW0gdGhlIGJvbmUgb2YgbXkgc3dvcmQKIFN0ZWVsIGlzIG15IGJvZHkgYW5kIGZpcmUgaXMgbXkgYmxvb2QKIEkgaGF2ZSBjcmVhdGVkIG92ZXIgYSB0aG91c2FuZCBibGFkZXMKIFVua25vd24gdG8gRGVhdGgsCiBOb3Iga25vd24gdG8gTGlmZS4KIEhhdmUgd2l0aHN0b29kIHBhaW4gdG8gY3JlYXRlIG1hbnkgd2VhcG9ucwogQnV0IHlldCwgdGhvc2UgaGFuZHMgd2lsbCBuZXZlciBob2xkIGFueXRoaW5nCiBTbyBhcyBJIHByYXksIFVubGltaXRlZCBCbGFkZSBXb3Jrcy4='
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from website.models import User

    with app.app_context():
        db.create_all()

    from flask_login import LoginManager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app
