# most of these helper functions need to be integrated into jinja2 (see app/__init__.py), so it's easier just to put them here

import os
import re

import fitz # PyMuPDF for saving pdf thumbnails

from flask import flash
from flask_login import current_user

from docx2pdf import convert
from comtypes import client # used for converting pptx to pdfs
from PIL import Image, ImageDraw, ImageFont

from app.models.query_engine import QueryEngine
from app.models.model_document import Document

from ..config import ALLOWED_EXTENSIONS, UPLOAD_FOLDER, DOCUMENT_THUMBNAIL_FOLDER, USER_AVATAR_FOLDER

def check_email_availability(email, msg="Email này đã được sử dụng, vui lòng chọn email khác"):
    user_by_email = QueryEngine.query_User_by("email", email)

    if user_by_email != None:
        flash(msg, category='error')
        return False
    
    return True

def check_username_availability(username, msg="Tên đăng nhập đã tồn tại, vui lòng chọn tên đăng nhập khác"):
    user_by_username = QueryEngine.query_User_by("username", username)

    if user_by_username != None:
        flash(msg, category="error")
        return False
    
    return True

def validate_email(email, msg="Email không hợp lệ, vui lòng thử lại"):
    email_pattern = r'^[\w\-\.]+@([\w-]+\.)+[\w-]{2,4}$'

    if re.match(email_pattern, email) == None:
        flash(msg, category='error')
        return False
    
    return True

def validate_username(username, minlen=5, maxlen=24):
    if len(username) < minlen or len(username) > maxlen:
        flash("Tên đăng nhập phải chứa từ {minlen} đến {maxlen} ký tự".format(minlen=minlen, maxlen=maxlen), category="error")
        return False
    
    return True
    
def validate_password(password, repeat_password, minlen=7):
    if password != repeat_password:
        flash("Mật khẩu nhập lại không khớp", category="error")
        return False

    if len(password) < minlen:
        flash("Mật khẩu phải chứa ít nhất {minlen} ký tự".format(minlen=minlen), category="error")
        return False

    return True

def allowed_file(filename: str):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def get_file_extension(filename: str):
    file_extension = filename.split('.')[-1].lower()

    return file_extension

def create_and_save_thumbmail(filename: str):
    file_extension = get_file_extension(filename)

    if file_extension == "pdf":
        document = fitz.open(os.path.join(UPLOAD_FOLDER, filename))
        thumbnail = document[0].get_pixmap()

        thumbnail_filename = filename[:11] + "_thumbnail.jpg" # format: [krm-00003]_thumbnail.jpg

        thumbnail.save(os.path.join(DOCUMENT_THUMBNAIL_FOLDER, thumbnail_filename))
        document.close()

        return True
    
    if file_extension == "docx":
        # convert the "docx" file into a pdf file (then delete the pdf file later)
        convert(input_path=os.path.join(UPLOAD_FOLDER, filename), 
                                    output_path=DOCUMENT_THUMBNAIL_FOLDER)
        
        pdf_document_path = os.path.join(DOCUMENT_THUMBNAIL_FOLDER, filename)
        pdf_document_path = pdf_document_path[:-5] + ".pdf"

        # do the same stuffs like the "pdf" case
        document = fitz.open(pdf_document_path)
        thumbnail = document[0].get_pixmap()

        thumbnail_filename = filename[:11] + "_thumbnail.jpg" # format: [krm-00003]_thumbnail.jpg

        thumbnail.save(os.path.join(DOCUMENT_THUMBNAIL_FOLDER, thumbnail_filename))

        # delete the pdf file
        document.close()
        os.remove(pdf_document_path)

        return True
    
    # using this method: https://stackoverflow.com/a/51952043
    if file_extension == "pptx":
        # initialize Com in python
        import pythoncom
        pythoncom.CoInitialize()

        # converting pptx file to pdf file
        powerpoint_obj = client.CreateObject("Powerpoint.Application")
        powerpoint_obj.Visible = 1

        pdf_document_path = os.path.join(DOCUMENT_THUMBNAIL_FOLDER, filename)
        pdf_document_path = pdf_document_path[:-5] + ".pdf"

        deck = powerpoint_obj.Presentations.Open(os.path.join(UPLOAD_FOLDER, filename))
        deck.SaveAs(pdf_document_path, 32)
        deck.Close()
        powerpoint_obj.Quit()

        # do the same stuffs like the "pdf" case
        document = fitz.open(pdf_document_path)
        thumbnail = document[0].get_pixmap()

        thumbnail_filename = filename[:11] + "_thumbnail.jpg" # format: [krm-00003]_thumbnail.jpg

        thumbnail.save(os.path.join(DOCUMENT_THUMBNAIL_FOLDER, thumbnail_filename))

        # delete the pdf file
        document.close()
        os.remove(pdf_document_path)

        return True
    
    # using this method: https://stackoverflow.com/a/43566438
    if file_extension == "txt":
        # initialize image 
        thumbnail = Image.new("RGB", (800, 800), "white")
        
        # loading pillow objects
        draw = ImageDraw.Draw(thumbnail)
        font = ImageFont.truetype(os.path.join(os.path.dirname(__file__), "..\\..\\static\\font", "consola.ttf"), 24, encoding='unic')

        # getting save path
        thumbnail_filename = filename[:11] + "_thumbnail.jpg" # format: [krm-00003]_thumbnail.jpg

        # read and write on the thumbnail the contents of the file
        with open(os.path.join(UPLOAD_FOLDER, filename), 'r') as txt_file:
            line =  txt_file.readline()
            y_position = 16
            
            while line:
                draw.text((16, y_position), line, "black", font=font)
                y_position += 24
                line =  txt_file.readline()
            
            thumbnail.save(os.path.join(DOCUMENT_THUMBNAIL_FOLDER, thumbnail_filename))
        
        return True
    
    return False

def byte_to_kilobyte(in_bytes):
    return float(in_bytes / 1024)

def kilobyte_to_megabyte(in_kilobytes):
    return round(in_kilobytes / 1024, 2)

def get_uploader(document: Document):
    uploader = QueryEngine.query_User_by("id", document.uploader_id)

    return uploader

def is_bookmarked_by_current_user(document_id):
    query = QueryEngine.query_Bookmarking_Table(current_user.id, document_id)
    
    if query == None:
        return False
    
    return True

def get_thumbnail_path(document_id):
    thumbnail_filename = "[krm-{id:0>5}]_thumbnail.jpg".format(id=str(document_id))

    return "images/document_thumbnails/{}".format(thumbnail_filename)

def get_num_uploaded(user_id):
    num_uploaded = QueryEngine.query_Documents_by("uploader_id", user_id).count()

    return num_uploaded

def get_total_views(user_id):
    uploaded = QueryEngine.query_Documents_by("uploader_id", user_id)

    total_views = 0

    for document in uploaded:
        total_views += document.view_count

    return total_views

def get_total_downloaded(user_id):
    uploaded = QueryEngine.query_Documents_by("uploader_id", user_id)

    total_downloaded = 0

    for document in uploaded:
        total_downloaded += document.download_count

    return total_downloaded

def get_average_rating(user_id):
    uploaded = QueryEngine.query_Documents_by("uploader_id", user_id)

    sum_rating = 0
    total_rating_count = 0

    for document in uploaded:
        sum_rating += document.rating * document.rating_count
        total_rating_count += document.rating_count

    if total_rating_count != 0:
        return round(sum_rating / total_rating_count, 2)

    return 0

def round_float(value, num_places_after_decimal_point):
    return round(value, num_places_after_decimal_point)

def get_current_avatar_path(user_id):
    avatar_filename = "[user-{id:0>5}]_avatar.jpg".format(id=str(user_id)) # format "[user-00001]_avatar.jpg"
    
    if os.path.exists(os.path.join(USER_AVATAR_FOLDER, avatar_filename)):
        return "/static/images/user_avatars/{}".format(avatar_filename)
    
    return "/static/images/defaut_user.jpg"