from typing import Union
import os
from datetime import datetime, timezone
from sqlalchemy import Column, Integer, DateTime, event
from sqlalchemy.orm import declared_attr
from imgserve import db
from imgserve.utils import download_image, get_image_path

class Image(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc))

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

    @property
    def type(self):
        raise NotImplementedError("Subclasses must implement this property")

    @declared_attr
    def __mapper_args__(cls):
        return {
            'polymorphic_identity': cls.type.fget(None),
        }

    def __iter__(self):
        yield 'id', self.id
        yield 'type', self.type
        yield 'created_at', self.created_at.isoformat()
        yield 'updated_at', self.updated_at.isoformat()

    def __str__(self):
        return f"<{self.__class__.__name__}(id={self.id}, type={self.type}, created_at={self.created_at.isoformat()}, updated_at={self.updated_at.isoformat()})>"

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id!r}, type={self.type!r}, created_at={self.created_at!r}, updated_at={self.updated_at!r})"

class CV(Image):
    @property
    def type(self):
        return 'cv'

class SF(Image):
    @property
    def type(self):
        return 'sf'

class CVT(Image):
    @property
    def type(self):
        return 'cv.t'

class SFT(Image):
    @property
    def type(self):
        return 'sf.t'

class CH(Image):
    @property
    def type(self):
        return 'ch'
    
def receive_before_load(target, context):
    """
    Trigger function to be executed when an image is loaded (including get operations).
    Ensures that the image file exists on the filesystem.
    If it doesn't exist, it attempts to download it.
    """
    image_path = get_image_path(target.type, target.id)
    if not os.path.exists(image_path):
        os.makedirs(os.path.dirname(image_path), exist_ok=True)

        image_data = download_image(target.type, target.id)
        if image_data is None:
            raise ValueError(f"Failed to download image of type {target.type} with id {target.id}")
        
        with open(image_path, 'wb') as f:
            f.write(image_data.getvalue())
        print(f"Image file recreated for: {target}")

def receive_before_insert(mapper, connection, target):
    """
    Trigger function to be executed before an image is inserted.
    Attempts to download the image. If download fails, raises an exception to prevent insertion.
    """
    image_path = get_image_path(target.type, target.id)
    os.makedirs(os.path.dirname(image_path), exist_ok=True)

    image_data = download_image(target.type, target.id)
    if image_data is None:
        raise ValueError(f"Failed to download image of type {target.type} with id {target.id}")
   
    with open(image_path, 'wb') as f:
        f.write(image_data.getvalue())

def receive_before_update(mapper, connection, target):
    """
    Trigger function to be executed before an image is updated.
    Attempts to re-download the image. If successful, it overwrites the old image.
    Always updates the last_modified_at timestamp.
    """
    image_path = get_image_path(target.type, target.id)
    os.makedirs(os.path.dirname(image_path), exist_ok=True)

    image_data = download_image(target.type, target.id)
    if image_data is None:
        raise ValueError(f"Failed to download image of type {target.type} with id {target.id}")
    
    with open(image_path, 'wb') as f:
        f.write(image_data.getvalue())

def receive_after_delete(mapper, connection, target):
    """
    Trigger function to be executed after an image is deleted.
    Removes the image file from the file system.
    """
    image_path = get_image_path(target.type, target.id)
    if os.path.exists(image_path):
        os.remove(image_path)
    print(f"Image deleted: {target}")

for cls in [CV, SF, CVT, SFT, CH]:
    event.listen(cls, 'load', receive_before_load)
    event.listen(cls, 'before_insert', receive_before_insert)
    event.listen(cls, 'before_update', receive_before_update)
    event.listen(cls, 'after_delete', receive_after_delete)

ImageType = Union[CV, SF, CVT, SFT, CH]

IMAGE_MODEL = {'cv': CV, 'sf': SF, 'cv.t': CVT, 'sf.t': SFT, 'ch': CH}
