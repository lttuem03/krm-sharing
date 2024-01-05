from flask import (request, 
                   render_template, 
                   redirect, 
                   url_for)

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
            document_type = request.form.get("document_type")
            document_subject = request.form.get("document_subject")
            document_year = request.form.get("document_year")
            document_school = request.form.get("document_school")

            upload_successful = DocumentManagementController.process_upload(request=request, 
                                                                            document_name=document_name,
                                                                            document_subject=document_subject,
                                                                            document_type=document_type,
                                                                            document_school=document_school,
                                                                            document_year=document_year)
            
            if upload_successful:
                # redirect to the document detail page for the newly uploaded document
                return redirect(url_for("home")) # we'll leave this here for now (until I implement the DocumentDetailsView)

        return render_template("upload.html", user=current_user)

# old one    
## reference: https://flask.palletsprojects.com/en/2.3.x/patterns/fileuploads/
#@views.route('/upload/', methods=['GET', 'POST'])
#def upload(user=current_user):
#    if not user.is_authenticated:
#        flash('Bạn cần đăng nhập để thực hiện chức năng này', category='error')
#        return redirect(url_for('views.login'))
#
#    if request.method == 'POST':
#        # check if the post request has the file part
#        if 'file' not in request.files:
#            flash('No file part')
#            return redirect(request.url)
#
#        file = request.files['file']
#
#        # If the user does not select a file, the browser submits an
#        # empty file without a filename.
#        if file.filename == '':
#            flash('Bạn chưa chọn tài liệu nào để tải lên!')
#            return redirect(request.url)
#
#        if file and allowed_file(file.filename):
#            filename = secure_filename(file.filename)
#            
#            current_entry_count = Document.query.count()
#
#            filename = str(current_entry_count + 1) + '_' + filename
#
#            document_url = os.path.join(UPLOAD_FOLDER, filename)
#
#            document_name = request.form.get('document_name')
#            if document_name == "":
#                flash('Vui lòng nhập tên tài liệu')
#                return redirect(request.url)
#
#            document_type = request.form.get('document_type')
#            if document_type == "Chọn loại tài liệu":
#                flash('Vui lòng chọn loại tài liệu')
#                return redirect(request.url)
#
#            document_subject = request.form.get('document_subject')
#            document_year = request.form.get('document_year')
#            if document_year == "":
#                document_year = None
#
#            document_school = request.form.get('document_school')
#            if document_school == "":
#                document_school = None
#
#            file.save(document_url)
#
#            document_filesize = byte_to_kilobyte(os.stat(document_url).st_size)
#
#            new_document = Document(name=document_name, uploader_id=user.id, type=document_type, subject=document_subject,
#                                    school=document_school, year=document_year, url=document_url, file_size=document_filesize)
#            db.session.add(new_document)
#            db.session.commit()
#
#            flash("Tải tài liệu lên thành công")
#            return redirect(url_for('views.index')) # return the document details page
#
#    return render_template('upload.html', user=current_user)