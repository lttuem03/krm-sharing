import re

from flask import Blueprint, render_template, flash, redirect, url_for, request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, current_user

from .database import db, User

views = Blueprint('views', __name__)

@views.route('/')
def index():
    return render_template('index.html')

@views.route('/login/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Đăng nhập thành công!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Sai mật khẩu.', category='error')
        else:
            flash('Email không tồn tại.', category='error')

    return render_template("login.html", user=current_user)

@views.route('/register/', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        emailpattern = '^[\w-\.]+@([\w-]+\.)+[\w-]{2,4}$'
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email đã được đăng ký.', category='error')
        elif not re.match(emailpattern, email):
            flash('Định dạng email sai.', category='error')
        elif len(username) < 2:
            flash('Không cho phép username 1 ký tự.', category='error')
        elif password1 != password2:
            flash('Mật khẩu không khớp.', category='error')
        elif len(password1) < 7:
            flash('Mật khẩu phải chứa ít nhất 7 ký tự.', category='error')
        else:
            new_user = User(email=email, username=username, password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Tạo tài khoản thành công!', category='success')
            return redirect(url_for('views.home'))

    return render_template('register.html', user=current_user)

@views.route('/upload/')
def upload():
    return render_template('upload.html')

@views.route('/createlisting/')
def createlisting():
    return render_template('create_listing.html')

@views.route('/mydocument/')
def mydocument():
    return render_template('my_document.html')