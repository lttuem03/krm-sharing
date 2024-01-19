import os

from flask import (flash,
                   Request)
from flask_login import current_user

from werkzeug.utils import secure_filename

from app.models import db
from app.models.model_listing import Listing
from app.models.query_engine import QueryEngine

from .utils import (allowed_file)

from ..config import UPLOAD_FOLDER


class ListingManagementController():
    @staticmethod
    def process_upload(request: Request) -> bool:
        """
        Process a file upload attempt.

        Return the instance of the newly uploaded listing if successful, otherwise return None 
        """
        listing_name = request.form.get("listing_name")
        listing_description = request.form.get("listing_description")
        listing_subject = request.form.get("listing_subject")
        listing_author = request.form.get("listing_author")
        listing_year = request.form.get("listing_year")
        listing_school = request.form.get("listing_school")
        listing_status = request.form.get("listing_status")
        listing_price = request.form.get("listing_price")
        listing_location = request.form.get("listing_location")

        if "image" not in request.files:
            flash("No file part in request")
            return None

        files = request.files.getlist("image")

        # Check whether the user has selected a file from their local machine

        # Check whether the required fields are empty
        if listing_name == "":
            flash("Vui lòng nhập tên tài liệu.", category="error")
            return None

        if listing_subject == "":
            flash("Vui lòng điền tên môn học/chủ đề của tài liệu.",
                  category="error")
            return None

        if listing_status == '':
            flash("Vui lòng mô tả trạng thái của tài liệu.", category="error")
            return None

        if listing_price == '':
            flash("Vui lòng điền giá của tài liệu.", category="error")
            return None

        if listing_location == '':
            flash("Vui lòng cho vị trí của đơn hàng.", category="error")
            return None
        # Setting the unrequired fields None if they are empty
        if listing_description == "":
            listing_description = None

        if listing_school == "":
            listing_school = None

        if listing_year == "":
            listing_year = None

        if listing_author == "":
            listing_author = None

        # Attempt upload
        if files:
            new_listing = Listing(name=listing_name,
                                  description=listing_description,
                                  uploader_id=current_user.id,
                                  subject=listing_subject,
                                  author=listing_author,
                                  school=listing_school,
                                  year=listing_year,
                                  status=listing_status,
                                  price=listing_price,
                                  location=listing_location)

            db.session.add(new_listing)
            db.session.commit()
            # update values in database
            new_listing.filename = filename
            folder_name = f'[krm-{new_listing.id}] {listing_name}'
            save_folder = os.path.join(UPLOAD_FOLDER, folder_name)
            if not os.path.exists(save_folder):
                os.makedirs(save_folder)
            for file in files:
                if allowed_file(file.filename):
                    filename = secure_filename(file.filename)

                    # padding filename with id (to distinguish between listings with the same file name)
                    filename = "[{id:0>5}] {original}".format(
                        id=str(new_listing.id), original=filename)

                    # actually saving the file to the file server
                    save_path = os.path.join(save_folder, filename)
                    file.save(save_path)
            flash("Đăng bán thành công!", category="success")
            return new_listing
        flash("Không có ảnh preview sản phẩm", category="error")
        return None

    @staticmethod
    def get_uploaded(user_id):
        return QueryEngine.query_listings_by("uploader_id", user_id)

    @staticmethod
    def get_bookmarked(user_id):
        bookmark_entrys = QueryEngine.query_Bookmarking_Table_filter_by_user_id(
            user_id)

        bookmarked = []
        for entry in bookmark_entrys:
            query_listing = QueryEngine.query_listing_by(
                "id", entry.listing_id)

            if query_listing != None:
                bookmarked.append(query_listing)

        return bookmarked

    @staticmethod
    def delete_listing(listing: Listing):
        """
        Process an attempt to remove a listing from the platform.

        Return True if successful, otherwise return False
        """
        # Remove from the file server
        try:
            os.remove(os.path.join(UPLOAD_FOLDER, listing.foldername))
        except OSError:
            pass

        # Remove from the database
        db.session.delete(listing)
        db.session.commit()

        return True
