#import os
#import re
#
#from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
#from flask_login import login_user, current_user, login_required, logout_user
#from flask_sqlalchemy import SQLAlchemy
#from werkzeug.utils import secure_filename
#from werkzeug.security import generate_password_hash, check_password_hash
#
#from .database import db, User, Document
#from .utils import (check_email_availability,
#                    check_username_availability,
#                    validate_email,
#                    validate_username,
#                    validate_password,
#                    allowed_file,
#                    byte_to_kilobyte
#                    )
#from .config import UPLOAD_FOLDER, SEARCH_RESULTS_DISPLAY_LIMIT
#
#views = Blueprint('views', __name__)
#
#
#
#
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
#            return redirect(url_for('views.index'))
#
#    return render_template('upload.html', user=current_user)
#
#
#@views.route('/createlisting/')
#def createlisting():
#    if not current_user.is_authenticated:
#        redirect(url_for('views.login'))
#    return render_template('create_listing.html')
#
#
#@views.route('/mydocument/')
#@login_required
#def mydocument():
#
#    uploaded_documents = Document.query.filter_by(uploader_id=current_user.id).all()
#
#    return render_template('my_document.html', user=current_user, uploaded=uploaded_documents)
#
#
#@views.route('/document/<id>')
#def document(id):
#    doc_query_result = Document.query.filter_by(id=id).first()
#
#    return render_template('document.html', user=current_user, document=doc_query_result)
#
#
#@views.route('/profile/')
#@login_required
#def profile():
#    return render_template('profile.html', user=current_user)
#
#@views.route('/changepw/', methods=['GET', 'POST'])
#@login_required
#def changepassword():
#    if request.method == 'POST':
#        newpw = request.form.get('newpw')
#        confirmpw = request.form.get('newpw2')
#        password = request.form.get('password')
#
#        user = User.query.filter_by(email=current_user.email).first()
#
#        if newpw != confirmpw:
#            flash('Mật khẩu xác nhận không khớp', category='error')
#        else:
#            if check_password_hash(user.hpassword, password):
#                flash('Đổi mật khẩu thành công', category='success')
#                user.hpassword = generate_password_hash(
#                    password, method='pbkdf2')
#                db.session.commit()
#                return redirect(url_for('views.profile'))
#            else:
#                flash('Sai mật khẩu', category='error')
#    return render_template('changepw.html', user=current_user)
#