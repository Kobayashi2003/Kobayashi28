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
    is_active = db.Column(db.Boolean, default=True)

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

class ReleaseMetadata(Metadata):
    id = db.Column(db.String(255), db.ForeignKey('release.id', ondelete="CASCADE"), primary_key=True)
    parent = db.relationship("Release", back_populates="release_metadata")

# ----------------------------------------
# Variables 
# ----------------------------------------

MetaModelType = Union[
    VNMetadata, TagMetadata, ProducerMetadata, 
    StaffMetadata, CharacterMetadata, TraitMetadata,
    ReleaseMetadata
]

META_MODEL_MAP = {
    'vn': VNMetadata,
    'tag': TagMetadata,
    'producer': ProducerMetadata,
    'staff': StaffMetadata,
    'character': CharacterMetadata,
    'trait': TraitMetadata,
    'release': ReleaseMetadata
}