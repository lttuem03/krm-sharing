import os
from flask import Flask, render_template


app = Flask(__name__,
            static_url_path='', 
            static_folder='resources/static',
            template_folder='resources/templates')

@app.route("/")
def welcome():
    return render_template('index.html')

@app.route("/upload/")
def upload():
    return render_template('upload.html')

@app.route("/createlisting/")
def createlisting():
    return render_template('create_listing.html')

@app.route("/mydocument/")
def mydocument():
    return render_template('my_document.html')

@app.route('/register/')
def register():
    return render_template('register.html')

@app.route('/login/')
def login():
    return render_template('login.html')

if __name__ == "__main__":
    app.run()