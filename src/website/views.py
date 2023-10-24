from flask import Blueprint, render_template, flash, redirect, url_for, request
from flask_login import login_user, current_user, login_required, logout_user
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy

from .database import db, User
from .utils import check_email_availability, check_username_availability, validate_email, validate_username, validate_password

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

            new_user = User(name, role, school, email, username,
                            hpassword=generate_password_hash(password, method='pbkdf2'))
            db.session.add(new_user)
            db.session.commit()

            login_user(new_user, remember=True)
            flash('Tạo tài khoản thành công!', category='success')
            return redirect(url_for('views.index'))

    return render_template('register.html', user=current_user)


@views.route('/upload/')
def upload():
    if not current_user.is_authenticated:
        redirect(url_for('views.login'))
    return render_template('upload.html')


@views.route('/createlisting/')
def createlisting():
    if not current_user.is_authenticated:
        redirect(url_for('views.login'))
    return render_template('create_listing.html')


@views.route('/mydocument/')
def mydocument():
    if not current_user.is_authenticated:
        redirect(url_for('views.login'))
    return render_template('my_document.html')
