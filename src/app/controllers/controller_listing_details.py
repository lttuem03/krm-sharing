from flask_login import current_user

from app.models import db
from app.models.model_listing import Listing
from app.models.table_bookmarking import BookmarkingTable
from app.models.query_engine import QueryEngine


class ListingDetailsController():
    @staticmethod
    def get_listing(id):
        listing = QueryEngine.query_Listing_by("id", id)

        return listing

    @staticmethod
    def update_viewcount(listing: Listing):
        listing.view_count += 1

        db.session.commit()

    @staticmethod
    def update_amount(listing: Listing):
        listing.amount -= 1

        db.session.commit()

    @staticmethod
    def change_bookmark_state(listing: Listing):
        bookmark_entry = QueryEngine.query_Bookmarking_Table(
            current_user.id, listing.id)

        # bookmarked -> unbookmarking
        if bookmark_entry != None:
            db.session.delete(bookmark_entry)
            db.session.commit()
            return

        # unbookmarked -> bookmarking
        db.session.add(BookmarkingTable(
            user_id=current_user.id, listing_id=listing.id))
        db.session.commit()
        return

    @staticmethod
    def update_rating(listing, added_rating_value):
        new_rating = (listing.rating * listing.rating_count +
                      added_rating_value) / (listing.rating_count + 1)
        listing.rating = new_rating
        listing.rating_count = listing.rating_count + 1

        db.session.commit()
