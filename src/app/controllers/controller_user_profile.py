
from app.models.model_user import User
from app.models.query_engine import QueryEngine

class UserProfileController():
    @staticmethod
    def get_user(user_id) -> (None | User):
        return QueryEngine.query_User_by("id", user_id)