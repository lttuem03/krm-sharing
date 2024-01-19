import json

from flask import (request,
                   render_template)

from flask.views import MethodView

from flask_login import current_user

from app.controllers import SearchController

class LiveSearchProcessingView(MethodView):
    def get(self):
        search_text = request.args['search_text']
        suggestions = SearchController.process_live_searching(search_text)
        return json.dumps({"suggestions": suggestions})
    
class SearchResults(MethodView):
    def get(self, search_text):
        search_results = SearchController.search(search_text)

        return render_template("search_results.html", user=current_user, search_text=search_text, search_results=search_results)
    
class DocumentLibrary(MethodView):
    def get(self):
        all_documents = SearchController.get_all_documents()
        all_listing = SearchController.get_all_listing()

        return render_template("document_library.html", user=current_user, document_count=len(all_documents), all_documents=all_documents,listing_count = len(all_listing),all_listing=all_listing)