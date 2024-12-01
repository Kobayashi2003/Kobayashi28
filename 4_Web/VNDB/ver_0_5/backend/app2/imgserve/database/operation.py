from typing import Optional
from imgserve import db
from .model import IMAGE_MODEL, ImageType
from .common import save_db_operation

def exists(type: str, id: str) -> bool:
    if type not in IMAGE_MODEL:
        return False
    model = IMAGE_MODEL[type]
    return db.session.query(model.query.filter_by(id=id).exists()).scalar()

@save_db_operation
def create(type: str, id: str) -> Optional[ImageType]:
    model = IMAGE_MODEL[type]
    image = model(id=id)
    db.session.add(image)
    db.session.commit()
    return image

@save_db_operation
def get(type: str, id: str) -> Optional[ImageType]:
    model = IMAGE_MODEL[type]
    return model.query.get(id)

@save_db_operation
def update(type: str, id: str) -> Optional[ImageType]:
    image = get(type, id)
    if not image:
        return None
    db.session.add(image)
    db.session.commit()
    return image

@save_db_operation
def delete(type: str, id: str) -> Optional[ImageType]:
    image = get(type, id)
    if not image:
        return None
    db.session.delete(image)
    db.session.commit()
    return image