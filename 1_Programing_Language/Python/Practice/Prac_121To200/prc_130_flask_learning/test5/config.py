import os

class Config:
    # Base directory of the application
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    
    # Upload folder
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
    
    # Allowed file extensions
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
    
    # Maximum file size (5 MB)
    MAX_CONTENT_LENGTH = 5 * 1024 * 1024