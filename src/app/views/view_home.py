from flask import (request,
                   redirect,
                   url_for,
                   render_template)

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
    
    def post(self):
        search_text = request.form['search_text']

        return redirect(url_for("search_results", search_text=search_text))