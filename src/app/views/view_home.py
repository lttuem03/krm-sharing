from flask import (render_template)

from flask.views import MethodView
from flask_login import current_user

from app.controllers import HomeController

class HomeView(MethodView):
    def get(self):
        top_downloaded = HomeController.get_top_downloaded(5)
        top_viewed = HomeController.get_top_viewed(5)
        top_user_upload_count = HomeController.get_top_user_upload_count(5)

        return render_template("home.html", 
                               user=current_user, 
                               top_downloaded=top_downloaded,
                               top_viewed=top_viewed,
                               top_user_upload_count=top_user_upload_count)