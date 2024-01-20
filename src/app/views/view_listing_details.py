from flask import (request,
                   render_template,
                   send_from_directory)

from flask.views import MethodView
from flask_login import current_user

from app.controllers import ListingDetailsController

from ..config import LISTING_PREVIEW


class ListingDetailsView(MethodView):
    def get(self, id):
        listing = ListingDetailsController.get_listing(id)

        if listing != None:
            ListingDetailsController.update_viewcount(listing)
            return render_template("listing_details.html", user=current_user, listing=listing)

        return render_template("document_not_exists.html", user=current_user)

    def post(self, id):
        listing = ListingDetailsController.get_listing(id)

        if listing == None:
            return render_template("document_not_exists.html", user=current_user)

        if "rating_request" in request.form:
            rating = request.form.get("select_rating")
            ListingDetailsController.update_rating(listing, int(rating))
        
        return render_template("listing_details.html", user=current_user, listing=listing)
