from flask import Blueprint, render_template

views = Blueprint('views', __name__)


@views.route('/')
def welcome():
    return render_template('index.html')


@views.route('/upload/')
def upload():
    return render_template('upload.html')


@views.route('/createlisting/')
def createlisting():
    return render_template('create_listing.html')


@views.route('/mydocument/')
def mydocument():
    return render_template('my_document.html')
