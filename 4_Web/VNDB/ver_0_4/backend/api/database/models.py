from typing import Union

import os
from datetime import date, datetime, timezone

from sqlalchemy import event, inspect
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSON, JSONB, ARRAY
from sqlalchemy.ext.declarative import declared_attr

from api import db

# ----------------------------------------
# Resources Models
# ----------------------------------------

class VN(db.Model):
    __tablename__ = 'vn'

    id = db.Column(db.String(255), primary_key=True)
    title = db.Column(db.String(255))
    titles = db.Column(JSONB)
    aliases = db.Column(ARRAY(db.String))
    olang = db.Column(db.String(10))
    devstatus = db.Column(db.Enum('Finished', 'In development', 'Cancelled', name='devstatus_enum'))
    released = db.Column(db.Date)
    languages = db.Column(ARRAY(db.String))
    platforms = db.Column(ARRAY(db.String))
    image = db.Column(JSONB)
    length = db.Column(db.Integer)
    length_minutes = db.Column(db.Integer)
    description = db.Column(db.Text)
    screenshots = db.Column(ARRAY(JSONB))
    relations = db.Column(ARRAY(JSONB))
    tags = db.Column(ARRAY(JSONB))
    developers = db.Column(ARRAY(JSONB))
    staff = db.Column(ARRAY(JSONB))
    va = db.Column(ARRAY(JSONB))
    extlinks = db.Column(ARRAY(JSONB))
    # Relationships
    vn_metadata = db.relationship("VNMetadata", back_populates="parent", uselist=False, cascade="all, delete-orphan")
    images = db.relationship("VNImage", back_populates="vn", cascade="all, delete-orphan")
    savedatas = db.relationship("SaveData", back_populates="vn", cascade="all, delete-orphan")

class Tag(db.Model):
    __tablename__ = 'tag'

    id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255))
    aliases = db.Column(ARRAY(db.String))
    description = db.Column(db.Text)
    category = db.Column(db.Enum('cont', 'ero', 'tech', name='tag_category_enum'))
    searchable = db.Column(db.Boolean)
    applicable = db.Column(db.Boolean)
    vn_count = db.Column(db.Integer)
    # Relationships
    tag_metadata = db.relationship("TagMetadata", back_populates="parent", uselist=False, cascade="all, delete-orphan")

class Producer(db.Model):
    __tablename__ = 'producer'

    id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255))
    original = db.Column(db.String(255))
    aliases = db.Column(ARRAY(db.String))
    lang = db.Column(db.String(10))
    type = db.Column(db.Enum('co', 'in', 'ng', name='producer_type_enum'))
    description = db.Column(db.Text)
    # Relationships
    producer_metadata = db.relationship("ProducerMetadata", back_populates="parent", uselist=False, cascade="all, delete-orphan")

class Staff(db.Model):
    __tablename__ = 'staff'

    id = db.Column(db.String(255), primary_key=True)
    ismain = db.Column(db.Boolean)
    name = db.Column(db.String(255))
    original = db.Column(db.String(255))
    lang = db.Column(db.String(10))
    gender = db.Column(db.Enum('m', 'f', name='gender_enum'))
    description = db.Column(db.Text)
    aliases = db.Column(ARRAY(JSONB))
    # Relationships
    staff_metadata = db.relationship("StaffMetadata", back_populates="parent", uselist=False, cascade="all, delete-orphan")

class Character(db.Model):
    __tablename__ = 'character'

    id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255))
    original = db.Column(db.String(255))
    aliases = db.Column(ARRAY(db.String))
    description = db.Column(db.Text)
    image = db.Column(JSONB)
    blood_type = db.Column(db.Enum('a', 'b', 'ab', 'o', name='blood_type_enum'))
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    bust = db.Column(db.Integer)
    waist = db.Column(db.Integer)
    hips = db.Column(db.Integer)
    cup = db.Column(db.Enum('AAA', 'AA', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', name='cup_size_enum'))
    age = db.Column(db.Integer)
    birthday = db.Column(ARRAY(db.Integer))
    sex = db.Column(ARRAY(db.Enum('m', 'f', 'b', 'n', name='sex_enum')))
    vns = db.Column(ARRAY(JSONB))
    traits = db.Column(ARRAY(JSONB))
    # Relationships
    character_metadata = db.relationship("CharacterMetadata", back_populates="parent", uselist=False, cascade="all, delete-orphan")
    images = db.relationship("CharacterImage", back_populates="character", cascade="all, delete-orphan")

class Trait(db.Model):
    __tablename__ = 'trait'

    id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255))
    aliases = db.Column(ARRAY(db.String))
    description = db.Column(db.Text)
    searchable = db.Column(db.Boolean)
    applicable = db.Column(db.Boolean)
    group_id = db.Column(db.String(255))
    group_name = db.Column(db.String(255))
    char_count = db.Column(db.Integer)
    # Relationships
    trait_metadata = db.relationship("TraitMetadata", back_populates="parent", uselist=False, cascade="all, delete-orphan")

class Image(db.Model):
    __abstract__ = True

    id = db.Column(db.String(255), primary_key=True)
    image_type = db.Column(db.String(50))

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower().replace('image', '_image')

class VNImage(Image):
    vn_id = db.Column(db.String(255), db.ForeignKey('vn.id', ondelete="CASCADE"))

    vn = db.relationship("VN", back_populates="images")
    vn_image_metadata = db.relationship("VNImageMetadata", back_populates="parent", uselist=False, cascade="all, delete-orphan")

class CharacterImage(Image):
    character_id = db.Column(db.String(255), db.ForeignKey('character.id', ondelete="CASCADE"))

    character = db.relationship("Character", back_populates="images")
    character_image_metadata = db.relationship("CharacterImageMetadata", back_populates="parent", uselist=False, cascade="all, delete-orphan")

class SaveData(db.Model):
    __tablename__ = 'savedata'

    id = db.Column(db.String, primary_key=True)
    vnid = db.Column(db.String(255), db.ForeignKey('vn.id', ondelete="CASCADE"), nullable=False)
    time = db.Column(db.DateTime, nullable=False, default=func.now())
    filename = db.Column(db.String(255), nullable=False)

    vn = db.relationship("VN", back_populates="savedatas")
    savedata_metadata = db.relationship("SaveDataMetadata", back_populates="parent", uselist=False, cascade="all, delete-orphan")


class Backup(db.Model):
    __tablename__ = 'backup'

    id = db.Column(db.String(36), primary_key=True)
    time = db.Column(db.DateTime, nullable=False, default=lambda: datetime.now(timezone.utc))

    backup_metadata = db.relationship("BackupMetadata", back_populates="parent", uselist=False, cascade="all, delete-orphan")

# ----------------------------------------
# Metadata Models
# ----------------------------------------

class Metadata(db.Model):
    __abstract__ = True

    created_at = db.Column(db.DateTime, default=func.now())
    last_modified_at = db.Column(db.DateTime, default=func.now())
    last_accessed_at = db.Column(db.DateTime, default=func.now())
    view_count = db.Column(db.Integer, default=0)
    is_active = db.Column(db.Boolean, default=True)
    notes = db.Column(db.Text)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower().replace('metadata', '_metadata')

class VNMetadata(Metadata):
    id = db.Column(db.String(255), db.ForeignKey('vn.id', ondelete='CASCADE'), primary_key=True)
    parent = db.relationship("VN", back_populates="vn_metadata")

class TagMetadata(Metadata):
    id = db.Column(db.String(255), db.ForeignKey('tag.id', ondelete='CASCADE'), primary_key=True)
    parent = db.relationship("Tag", back_populates="tag_metadata")

class ProducerMetadata(Metadata):
    id = db.Column(db.String(255), db.ForeignKey('producer.id', ondelete="CASCADE"), primary_key=True)
    parent = db.relationship("Producer", back_populates="producer_metadata")

class StaffMetadata(Metadata):
    id = db.Column(db.String(255), db.ForeignKey('staff.id', ondelete="CASCADE"), primary_key=True)
    parent = db.relationship("Staff", back_populates="staff_metadata")

class CharacterMetadata(Metadata):
    id = db.Column(db.String(255), db.ForeignKey('character.id', ondelete="CASCADE"), primary_key=True)
    parent = db.relationship("Character", back_populates="character_metadata")

class TraitMetadata(Metadata):
    id = db.Column(db.String(255), db.ForeignKey('trait.id', ondelete="CASCADE"), primary_key=True)
    parent = db.relationship("Trait", back_populates="trait_metadata")

class SaveDataMetadata(Metadata):
    id = db.Column(db.String(255), db.ForeignKey('savedata.id', ondelete="CASCADE"), primary_key=True)
    parent = db.relationship("SaveData", back_populates="savedata_metadata")

class BackupMetadata(Metadata):
    id = db.Column(db.String(255), db.ForeignKey('backup.id', ondelete="CASCADE"), primary_key=True)
    parent = db.relationship("Backup", back_populates="backup_metadata")

class VNImageMetadata(Metadata):
    id = db.Column(db.String(255), db.ForeignKey('vn_image.id', ondelete="CASCADE"), primary_key=True)
    parent = db.relationship("VNImage", back_populates="vn_image_metadata")

class CharacterImageMetadata(Metadata):
    id = db.Column(db.String(255), db.ForeignKey('character_image.id', ondelete="CASCADE"), primary_key=True)
    parent = db.relationship("CharacterImage", back_populates="character_image_metadata")

# ----------------------------------------
# Event Listeners 
# ----------------------------------------
@event.listens_for(VNImage, 'after_delete')
def delete_vn_image_file(mapper, connection, target):
    ...

@event.listens_for(CharacterImage, 'after_delete')
def delete_character_image_file(mapper, connection, target):
    ...

@event.listens_for(SaveData, 'after_delete')
def delete_savedata_file(mapper, connection, target):
    ...

@event.listens_for(Backup, 'after_delete')
def delete_backup_file(mapper, connection, target):
    ...


ModelType = Union[
    VN, Tag, Producer, Staff, Character, Trait, 
    VNImage, CharacterImage,  SaveData, Backup
]

MetaModelType = Union[
    VNMetadata, TagMetadata, ProducerMetadata, StaffMetadata,
    CharacterMetadata, TraitMetadata, VNImageMetadata, CharacterImageMetadata,
    SaveDataMetadata, SaveDataMetadata
]

ImageModelType = Union[VNImage, CharacterImage]

MODEL_MAP = {
    # resource models
    'vn': VN,
    'tag': Tag,
    'producer': Producer,
    'staff': Staff,
    'character': Character,
    'trait': Trait,
    # image models
    'vn_image': VNImage,
    'character_image': CharacterImage,
    # others
    'savedata': SaveData,
    'backup': Backup
}

META_MODEL_MAP = {
    # resource metadata models
    'vn': VNMetadata,
    'tag': TagMetadata,
    'producer': ProducerMetadata,
    'staff': StaffMetadata,
    'character': CharacterMetadata,
    'trait': TraitMetadata,
    # image metadata models
    'vn_image': VNImageMetadata,
    'character_image': CharacterImageMetadata,
    # others
    'savedata': SaveDataMetadata,
    'backup': BackupMetadata
}

IMAGE_MODEL_MAP = {
    'vn': VNImage,
    'character': Character
}

def convert_model_to_dict(model):
    result = {}
    for column in inspect(model).mapper.column_attrs:
        value = getattr(model, column.key)
        if isinstance(value, (str, int, float, bool, type(None))):
            result[column.key] = value
        elif isinstance(value, (datetime, date)):
            result[column.key] = value.isoformat()
        elif isinstance(column.columns[0].type, ARRAY):
            if value is not None:
                result[column.key] = [
                    item if isinstance(item, (str, int, float, bool, type(None)))
                    else str(item)
                    for item in value
                ]
            else:
                result[column.key] = None
        elif isinstance(column.columns[0].type, (JSON, JSONB)):
            result[column.key] = value  # JSON and JSONB types are already serializable
        else:
            # For any other types, convert to string
            result[column.key] = str(value)
    return result