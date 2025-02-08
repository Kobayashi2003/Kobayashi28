from flask import current_app

def get_image_path(type: str, id: int) -> str:

    if id < 1:
        raise ValueError("Invalid ID")
    
    dir = str(id).zfill(2)[-2:]

    return f"{current_app.config['IMAGE_FOLDER']}/{type}/{dir}/{id}.jpg"