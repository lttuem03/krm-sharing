from flask import (request, 
                   render_template, 
                   redirect, 
                   url_for,
                   send_from_directory)
from flask.typing import ResponseReturnValue

from flask.views import View
from flask_login import (current_user,
                        login_required)

from app.controllers import DocumentManagementController

class UploadView(View):
    decorators = [login_required]
    methods = ["GET", "POST"]

    def dispatch_request(self):
        if request.method == "POST":
            document_name = request.form.get("document_name")
            document_description = request.form.get("document_description")
            document_type = request.form.get("document_type")
            document_subject = request.form.get("document_subject")
            document_author = request.form.get("document_author")
            document_year = request.form.get("document_year")
            document_school = request.form.get("document_school")
            
            new_document = DocumentManagementController.process_upload(request=request, 
                                                                       document_name=document_name,
                                                                       document_description=document_description,
                                                                       document_type=document_type,
                                                                       document_subject=document_subject,
                                                                       document_author=document_author,
                                                                       document_school=document_school,
                                                                       document_year=document_year)
            
            if new_document != None:
                # redirect to the document detail page for the newly uploaded document
                return redirect(url_for("document_details", id=new_document.id)) # we'll leave this here for now (until I implement the DocumentDetailsView)

        return render_template("upload.html", user=current_user)
    
class DocumentManagementView(View):
    decorators = [login_required]
    methods = ["GET"]

    def dispatch_request(self):
        uploaded = DocumentManagementController.get_uploaded(user_id=current_user.id)
        bookmarked = DocumentManagementController.get_bookmarked(user_id=current_user.id)

        return render_template("document_management.html", user=current_user, uploaded=uploaded, bookmarked=bookmarked)