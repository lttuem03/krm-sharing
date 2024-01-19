import os

# consts
MAX_CONTENT_LENGTH_IN_MB = 32
SEARCH_RESULTS_DISPLAY_LIMIT = 10

# database
DB_NAME = "database.db"
DB_SECRET_KEY = 'WGluIHRow6LMgHkgY2hvIHR1zKNpIGVtIHF1YSBtw7Ru'

# paths (all paths are relative to the '/src' folder)
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'file_server') # '.../src/file_server'
DOCUMENT_THUMBNAIL_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'static', 'images', 'document_thumbnails') # '.../src/static/images/document_thumbnails'
USER_AVATAR_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'static', 'images', 'user_avatars') # '.../src/static/images/user_avatars'

# allowed extensions
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx', 'pptx', 'png', 'jpeg', 'jpg'}