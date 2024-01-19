from app.models.query_engine import QueryEngine

from app.controllers.utils import get_num_uploaded

class HomeController():
    @staticmethod
    def get_top_downloaded(amount):
        """
        Returns top [amount] downloaded documents on the whole platform
        """

        top_downloaded = QueryEngine.query_top_Documents_by("download_count", amount)

        return top_downloaded
    
    @staticmethod
    def get_top_viewed(amount):
        """
        Returns top [amount] viewed documents on the whole platform
        """

        top_viewed = QueryEngine.query_top_Documents_by("view_count", amount)

        return top_viewed
    
    @staticmethod
    def get_top_user_upload_count(amount):
        all_users = QueryEngine.query_all_Users()

        # yes, this sucks, i know
        upload_count_dict = {}

        for user in all_users:
            upload_count_dict[user] = get_num_uploaded(user.id)

        # sort the dictionary to get top user with most upload count
        top_user_upload_count = sorted(upload_count_dict.items(), key=lambda x:x[1], reverse=True)

        if len(top_user_upload_count) > amount:
            return dict(top_user_upload_count[:amount])
        
        return dict(top_user_upload_count)