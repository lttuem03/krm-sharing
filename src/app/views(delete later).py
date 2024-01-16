
#@views.route('/createlisting/')
#def createlisting():
#    if not current_user.is_authenticated:
#        redirect(url_for('views.login'))
#    return render_template('create_listing.html')
#
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