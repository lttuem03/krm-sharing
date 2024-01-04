# All Views are implemented as class-based View, as specified here: https://flask.palletsprojects.com/en/3.0.x/views/
from .view_home import HomeView
from .view_authentication import LoginView, LogoutView, RegisterView