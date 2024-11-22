from typing import Union

from api import db
from sqlalchemy.sql import func
from sqlalchemy.ext.declarative import declared_attr

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
# Variables 
# ----------------------------------------

MetaModelType = Union[
    VNMetadata, TagMetadata, ProducerMetadata, StaffMetadata,
    CharacterMetadata, TraitMetadata, VNImageMetadata, CharacterImageMetadata,
    SaveDataMetadata, SaveDataMetadata
]

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