from app.models import Image

def user_owns_image(user_id, image_id):
    image = Image.query.get(image_id)
    return image is not None and image.user_id == user_id