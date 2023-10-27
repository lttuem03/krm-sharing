import os
import re

from flask import Blueprint, render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_user, current_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from .database import db, User, Document
from .utils import (check_email_availability, 
                    check_username_availability, 
                    validate_email, 
                    validate_username, 
                    validate_password, 
                    allowed_file,
                    byte_to_kilobyte
                )
from .config import UPLOAD_FOLDER, SEARCH_RESULTS_DISPLAY_LIMIT

views = Blueprint('views', __name__)

@views.route('/', methods=['GET', 'POST'])
def index():
    search = request.form.get('search')

    if search != "":
        print(search)

    return render_template('index.html', user=current_user)


@views.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.index'))


@views.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user_input = request.form.get('userinput')
        password = request.form.get('password')

        user = User.query.filter_by(email=user_input).first()
        if user == None:
            user = User.query.filter_by(username=user_input).first()
        
        if user != None:
            if check_password_hash(user.hpassword, password):
                flash('Đăng nhập thành công!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.index'))
            else:
                flash('Sai mật khẩu.', category='error')
        else:
            flash('Email hoặc tên đăng nhập không tồn tại.', category='error')

    return render_template("login.html", user=current_user)


@views.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        role = request.form.get('role')
        school = request.form.get('school')
        username = request.form.get('username')
        password = request.form.get('password')
        repeat_password = request.form.get('repeat_password')

        all_checks_pass = validate_email(email) \
            and check_email_availability(email) \
            and validate_username(username) \
            and check_username_availability(username) \
            and validate_password(password, repeat_password)

        if all_checks_pass:
            if role == "Chọn công việc hiện tại":
                role = None

            if school == "":
                school = None

            new_user = User(name=name, role=role, school=school, email=email, username=username,
                            hpassword=generate_password_hash(password, method='pbkdf2'))
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user, remember=True)
            flash('Tạo tài khoản thành công!', category='success')
            return redirect(url_for('views.index'))

    return render_template('register.html', user=current_user)


# reference: https://flask.palletsprojects.com/en/2.3.x/patterns/fileuploads/
@views.route('/upload/', methods=['GET', 'POST'])
def upload(user=current_user):
    if not user.is_authenticated:
        flash('Bạn cần đăng nhập để thực hiện chức năng này', category='error')
        return redirect(url_for('views.login'))
  
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        
        file = request.files['file']

        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('Bạn chưa chọn tài liệu nào để tải lên!')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            
            current_entry_count = Document.query.count()

            filename = str(current_entry_count + 1) + '_' + filename

            document_url = os.path.join(UPLOAD_FOLDER, filename)
            
            document_name = request.form.get('document_name')
            if document_name == "":
                flash('Vui lòng nhập tên tài liệu')
                return redirect(request.url)

            document_type = request.form.get('document_type')
            if document_type == "Chọn loại tài liệu":
                flash('Vui lòng chọn loại tài liệu')
                return redirect(request.url)
            
            document_subject = request.form.get('document_subject')
            document_year = request.form.get('document_year')
            if document_year == "":
                document_year = None
            
            document_school = request.form.get('document_school')
            if document_school == "":
                document_school = None
            
            file.save(document_url)

            document_filesize = byte_to_kilobyte(os.stat(document_url).st_size)

            new_document = Document(name=document_name, uploader_id=user.id, type=document_type, subject=document_subject, school=document_school, year=document_year, url=document_url, file_size=document_filesize)
            db.session.add(new_document)
            db.session.commit()

            flash("Tải tài liệu lên thành công")
            return redirect(url_for('views.index'))

    return render_template('upload.html', user=current_user)


@views.route('/createlisting/')
def createlisting():
    if not current_user.is_authenticated:
        redirect(url_for('views.login'))
    return render_template('create_listing.html')


@views.route('/mydocument/')
@login_required
def mydocument():

    uploaded_documents = Document.query.filter_by(uploader_id=current_user.id).all()

    return render_template('my_document.html', user=current_user, uploaded=uploaded_documents)


@views.route('/document/<id>')
def document(id):
    doc_query_result = Document.query.filter_by(id=id).first()

    return render_template('document.html', user=current_user, document=doc_query_result)


@views.route('/profile/')
@login_required
def profile():
    return render_template('profile.html', user=current_user)