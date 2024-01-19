
from app.models.query_engine import QueryEngine

document_list = None

class SearchController():
    @staticmethod
    def process_live_searching(search_text):
        """
        Process when user enter text into the search bar.

        Return suggestions based on the list of documents found.
        """
        global document_list

        if document_list == None:
            document_list = QueryEngine.query_all_Documents()

        suggestions = [document.name + "|" + str(document.id) for document in document_list 
                       if str(search_text).lower() in str(document.name).lower()]

        return suggestions
    
    @staticmethod
    def search(search_text):
        """
        Perform a search query, return search results
        """
        global document_list

        if document_list == None:
            document_list = QueryEngine.query_all_Documents()

        search_results = [document for document in document_list 
                          if str(search_text).lower() in str(document.name).lower()]

        return search_results 

    @staticmethod
    def get_all_documents():
        return QueryEngine.query_all_Documents()
    
    def get_all_listing():
        return QueryEngine.query_all_Listing()