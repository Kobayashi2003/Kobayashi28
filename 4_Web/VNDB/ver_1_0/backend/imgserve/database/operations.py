from imgserve import db
from .models import IMAGE_MODEL, ImageType
from .common import save_db_operation

@save_db_operation
def exists(type: str, id: str) -> bool:
    model = IMAGE_MODEL[type]
    image = model.query.get(id)
    return image is not None

@save_db_operation
def get(type: str, id: str) -> ImageType | None:
    model = IMAGE_MODEL[type]
    return model.query.get(id)

@save_db_operation
def create(type: str, id: str) -> ImageType | None:
    if exists(type, id):
        return None
    model = IMAGE_MODEL[type]
    image = model(id=id)
    db.session.add(image)
    db.session.commit()
    return image

@save_db_operation
def update(type: str, id: str) -> ImageType | None:
    image = get(type, id)
    if not image:
        return None
    db.session.add(image)
    db.session.commit()
    return image

@save_db_operation
def delete(type: str, id: str) -> ImageType | None:
    image = get(type, id)
    if not image:
        return None
    db.session.delete(image)
    db.session.commit()
    return image