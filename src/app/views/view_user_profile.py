from flask import (request,
                   flash,
                   render_template,
                   redirect,
                   url_for)

from flask.views import MethodView
from flask_login import current_user

from app.controllers import UserProfileController

class MyProfileView(MethodView):
    def get(self):
        return render_template("user_profile.html", user=current_user)
    
    def post(self):
        if "change_avatar_request" in request.form:
            return redirect(url_for("change_avatar"))

        if "change_name_request" in request.form:
            pass

        if "change_password_request" in request.form:
            pass

        return render_template("user_profile.html", user=current_user)

class UserProfileView(MethodView):
    def get(self, id):
        user = UserProfileController.get_user(id)

        return render_template("user_profile.html", user=user)
    
class ChangeAvatarView(MethodView):
    def get(self):
        return render_template("change_avatar.html", user=current_user)
    
    def post(self):
        change_avatar_succeed = UserProfileController.process_change_avatar()

        if change_avatar_succeed:
            return redirect(url_for('my_profile'))

        return render_template("change_avatar.html", user=current_user)