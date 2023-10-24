import os

from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, current_user, login_required, logout_user
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash

from .database import db, User
from .utils import (UPLOAD_FOLDER, 
                    check_email_availability, 
                    check_username_availability, 
                    validate_email, 
                    validate_username, 
                    validate_password, 
                    allowed_file
                )

views = Blueprint('views', __name__)

@views.route('/')
def index():
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
            user = User.query.filter_by(username=user_input)
        if user:
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
def upload():
    if not current_user.is_authenticated:
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
            file.save(os.path.join(UPLOAD_FOLDER, filename))

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
    return render_template('my_document.html', user=current_user)


@views.route('/profile/')
@login_required
def profile():
    return render_template('profile.html', user=current_user)
