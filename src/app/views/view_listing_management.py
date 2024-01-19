from flask import (request,
                   render_template,
                   redirect,
                   url_for,
                   flash)
from flask.typing import ResponseReturnValue

from flask.views import View
from flask_login import (current_user,
                         login_required)

from app.controllers import ListingManagementController

class ListingView(View):
    decorators = [login_required]
    methods = ["GET", "POST"]

    def dispatch_request(self):
        if request.method == "POST":
            new_document = ListingManagementController.process_upload(
                request=request)

            if new_document != None:
                # redirect to the listing detail page for the newly uploaded listing
                # we'll leave this here for now (until I implement the DocumentDetailsView)
                return redirect(url_for("listing_details", id=new_document.id))

        return render_template("create_listing.html", user=current_user)
