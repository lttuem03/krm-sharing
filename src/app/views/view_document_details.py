from flask import (request,
                   render_template,
                   send_from_directory)

from flask.views import MethodView
from flask_login import current_user

from app.controllers import DocumentDetailsController

from ..config import UPLOAD_FOLDER

class DocumentDetailsView(MethodView):
    def get(self, id):
        document = DocumentDetailsController.get_document(id)

        if document != None:
            DocumentDetailsController.update_viewcount(document)
            return render_template("document_details.html", user=current_user, document=document)
        
        return render_template("document_not_exists.html", user=current_user)
    
    def post(self, id):
        document = DocumentDetailsController.get_document(id)

        if document == None:
            return render_template("document_not_exists.html", user=current_user)
        
        if "download_request" in request.form:
            DocumentDetailsController.update_downloadcount(document)
            return send_from_directory(UPLOAD_FOLDER, document.filename, as_attachment=True)
        
        if "bookmark_request" in request.form:
            DocumentDetailsController.change_bookmark_state(document)
            return render_template("document_details.html", user=current_user, document=document)

        if "rating_request" in request.form:
            rating = request.form.get("select_rating")
            DocumentDetailsController.update_rating(document, int(rating))
            return render_template("document_details.html", user=current_user, document=document)
