from flask import (request, 
                   render_template, 
                   redirect, 
                   url_for
                   )
from flask.views import View
from flask_login import (current_user,
                        login_required
                        )

from ..controllers import AuthenticationController

class LoginView(View):
    decorators = []
    methods = ["GET", "POST"]

    def dispatch_request(self):
        if request.method == "POST":
            username_email = request.form.get("username_email")
            password = request.form.get("password")
            remember_me = request.form.get("remember_me", type=bool)

            user = AuthenticationController.process_login(username_email, password, remember_me)

            if user != None: # login successful
                return redirect(url_for("home"))
                 
        return render_template("login.html", user=current_user)
    
class LogoutView(View):
    decorators = [login_required]
    methods = ["GET"]

    def dispatch_request(self):
        AuthenticationController.process_logout()
        
        return redirect(url_for("home"))
    
class RegisterView(View):
    decorators = []
    methods = ["GET", "POST"]

    def dispatch_request(self):
        if request.method == "POST":
            name = request.form.get("name")
            email = request.form.get("email")
            username = request.form.get("username")
            password = request.form.get("password")
            repeat_password = request.form.get("repeat_password")

            user = AuthenticationController.process_register()

            if user != None: # registering was successfull, redirect to login page
                return redirect(url_for("login"))
            
        return render_template("register.html", user=current_user)