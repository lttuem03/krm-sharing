# All Views are implemented as class-based View, as specified here: https://flask.palletsprojects.com/en/3.0.x/views/
from .view_home import HomeView
from .view_authentication import LoginView, LogoutView, RegisterView
from .view_document_management import UploadView, DocumentManagementView
from .view_document_details import DocumentDetailsView
from .view_listing_management import ListingView
from .view_listing_details import ListingDetailsView
from .view_user_profile import MyProfileView, UserProfileView, ChangeAvatarView, ChangePasswordView
from .view_search import LiveSearchProcessingView, SearchResults
