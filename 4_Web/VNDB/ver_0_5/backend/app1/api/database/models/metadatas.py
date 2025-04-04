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
    updated_at = db.Column(db.DateTime, default=func.now())
    is_active = db.Column(db.Boolean, default=True)

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower().replace('metadata', '_metadatas')

class VNMetadata(Metadata):
    id = db.Column(db.String(255), db.ForeignKey('vns.id', ondelete='CASCADE'), primary_key=True)
    parent = db.relationship("VN", back_populates="meta")

class TagMetadata(Metadata):
    id = db.Column(db.String(255), db.ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)
    parent = db.relationship("Tag", back_populates="meta")

class ProducerMetadata(Metadata):
    id = db.Column(db.String(255), db.ForeignKey('producers.id', ondelete="CASCADE"), primary_key=True)
    parent = db.relationship("Producer", back_populates="meta")

class StaffMetadata(Metadata):
    id = db.Column(db.String(255), db.ForeignKey('staff.id', ondelete="CASCADE"), primary_key=True)
    parent = db.relationship("Staff", back_populates="meta")

class CharacterMetadata(Metadata):
    id = db.Column(db.String(255), db.ForeignKey('characters.id', ondelete="CASCADE"), primary_key=True)
    parent = db.relationship("Character", back_populates="meta")

class TraitMetadata(Metadata):
    id = db.Column(db.String(255), db.ForeignKey('traits.id', ondelete="CASCADE"), primary_key=True)
    parent = db.relationship("Trait", back_populates="meta")

class ReleaseMetadata(Metadata):
    id = db.Column(db.String(255), db.ForeignKey('releases.id', ondelete="CASCADE"), primary_key=True)
    parent = db.relationship("Release", back_populates="meta")

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