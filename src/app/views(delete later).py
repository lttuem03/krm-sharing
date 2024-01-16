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

#
#
#@views.route('/createlisting/')
#def createlisting():
#    if not current_user.is_authenticated:
#        redirect(url_for('views.login'))
#    return render_template('create_listing.html')
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