from flask import (request,
                   flash,
                   render_template,
                   redirect,
                   url_for)

from flask.views import MethodView
from flask_login import current_user

from app.controllers import UserProfileController
from app.controllers import AuthenticationController

class MyProfileView(MethodView):
    def get(self):
        return render_template("user_profile.html", user=current_user)
    
    def post(self):
        if "change_avatar_request" in request.form:
            return redirect(url_for("change_avatar"))

        if "change_password_request" in request.form:
            return redirect(url_for("change_password"))

        return render_template("user_profile.html", user=current_user)

class UserProfileView(MethodView):
    def get(self, id):
        user = UserProfileController.get_user(id)

        return render_template("user_profile.html", user=user)
    
class ChangeAvatarView(MethodView):
    def get(self):
        return render_template("change_avatar.html", user=current_user)
    
    def post(self):
        change_avatar_succeeded = UserProfileController.process_change_avatar()

        if change_avatar_succeeded:
            return redirect(url_for('my_profile'))

        return render_template("change_avatar.html", user=current_user)
    
class ChangePasswordView(MethodView):
    def get(self):
        return render_template("change_password.html", user=current_user)
    
    def post(self):
        current_password = request.form.get("current_password")
        new_password = request.form.get("new_password")
        confirm_new_password = request.form.get("confirm_new_password")

        change_password_succeeded = UserProfileController.process_change_password(current_password,
                                                                                  new_password,
                                                                                  confirm_new_password)

        if change_password_succeeded:
            # log user out
            AuthenticationController.process_logout()
            # request user to re-login with new password
            flash("Đổi mật khẩu thành công, vui lòng đăng nhập lại", category="success")
            return redirect(url_for("login"))

        return render_template("change_password.html", user=current_user)