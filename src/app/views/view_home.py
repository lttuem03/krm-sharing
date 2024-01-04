from flask import render_template
from flask.views import View
from flask_login import current_user

class HomeView(View):
    decorators = []
    methods = ["GET", "POST"]

    def dispatch_request(self):
        return render_template("home.html", user=current_user)
    
# old one
# @views.route('/', methods=['GET', 'POST'])
# def index():
#     search = request.form.get('search')
# 
#     if search != "":
#         print(search)
# 
#     return render_template('index.html', user=current_user)