import json

from flask import (request)

from flask.views import MethodView

from app.controllers import SearchController

class LiveSearchProcessingView(MethodView):
    def get(self):
        search_text = request.args['search_text']
        suggestions = SearchController.process_live_searching(search_text)
        return json.dumps({"suggestions": suggestions})