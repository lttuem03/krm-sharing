from flask import (request,
                   render_template)

from flask.views import MethodView
from flask_login import current_user

from app.controllers import UserProfileController

class MyProfileView(MethodView):
    def get(self):
        return render_template("user_profile.html", user=current_user)

class UserProfileView(MethodView):
    def get(self, id):
        user = UserProfileController.get_user(id)

        return render_template("user_profile.html", user=user)