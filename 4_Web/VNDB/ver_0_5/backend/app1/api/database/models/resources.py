from typing import Union

from sqlalchemy import Column, String, Integer, Boolean, Date, Text, Enum, ForeignKey
from sqlalchemy.dialects.postgresql import JSONB, ARRAY

from api import db

# ----------------------------------------
# Resources Models
# ----------------------------------------

class VN(db.Model):
    __tablename__ = 'vn'

    id = Column(String(255), primary_key=True)
    title = Column(String(255), nullable=True)
    alttitle = Column(String(255), nullable=True)
    titles = Column(ARRAY(JSONB), nullable=True)
    aliases = Column(ARRAY(String), nullable=True)
    olang = Column(String(10), nullable=True)
    devstatus = Column(Integer, nullable=True)
    released = Column(ARRAY(Integer), nullable=True)
    languages = Column(ARRAY(String), nullable=True)
    platforms = Column(ARRAY(String), nullable=True)
    image = Column(JSONB, nullable=True)
    length = Column(Integer, nullable=True)
    length_minutes = Column(Integer, nullable=True)
    length_votes = Column(Integer, nullable=True)
    description = Column(Text, nullable=True)
    screenshots = Column(ARRAY(JSONB), nullable=True)
    relations = Column(ARRAY(JSONB), nullable=True)
    tags = Column(ARRAY(JSONB), nullable=True)
    developers = Column(ARRAY(JSONB), nullable=True)
    editions = Column(ARRAY(JSONB), nullable=True)
    staff = Column(ARRAY(JSONB), nullable=True)
    va = Column(ARRAY(JSONB), nullable=True)
    extlinks = Column(ARRAY(JSONB), nullable=True)
    characters = Column(ARRAY(JSONB), nullable=True)
    releases = Column(ARRAY(JSONB), nullable=True)

    vn_metadata = db.relationship("VNMetadata", back_populates="parent", uselist=False, cascade="all, delete-orphan")

class Release(db.Model):
    __tablename__ ='release'

    id = Column(String(255), primary_key=True)
    title = Column(String(255), nullable=True)
    alttitle = Column(String(255), nullable=True)
    languages = Column(ARRAY(JSONB), nullable=True)
    platforms = Column(ARRAY(String), nullable=True)
    media = Column(ARRAY(JSONB), nullable=True)
    vns = Column(ARRAY(JSONB), nullable=True)
    producers = Column(ARRAY(JSONB), nullable=True)
    images = Column(ARRAY(JSONB), nullable=True)
    released = Column(ARRAY(Integer), nullable=True)
    minage = Column(Integer, nullable=True)
    patch = Column(Boolean, nullable=True)
    freeware = Column(Boolean, nullable=True)
    uncensored = Column(Boolean, nullable=True)
    official = Column(Boolean, nullable=True)
    has_ero = Column(Boolean, nullable=True)
    resolution = Column(ARRAY(Integer), nullable=True)
    engine = Column(String, nullable=True)
    voiced = Column(Integer, nullable=True)
    notes = Column(Text, nullable=True)
    gtin = Column(String(255), nullable=True)
    catalog = Column(String(255), nullable=True)
    extlinks = Column(ARRAY(JSONB), nullable=True)

    release_metadata = db.relationship("ReleaseMetadata", back_populates="parent", uselist=False, cascade="all, delete-orphan")

class Tag(db.Model):
    __tablename__ = 'tag'

    id = Column(String(255), primary_key=True)
    aid = Column(String(255), nullable=True)
    name = Column(String(255), nullable=True)
    aliases = Column(ARRAY(String), nullable=True)
    description = Column(Text, nullable=True)
    category = Column(String(255), nullable=True)
    searchable = Column(Boolean, nullable=True)
    applicable = Column(Boolean, nullable=True)
    vn_count = Column(Integer, nullable=True)

    tag_metadata = db.relationship("TagMetadata", back_populates="parent", uselist=False, cascade="all, delete-orphan")

class Producer(db.Model):
    __tablename__ = 'producer'

    id = Column(String(255), primary_key=True)
    name = Column(String(255), nullable=True)
    original = Column(String(255), nullable=True)
    aliases = Column(ARRAY(String), nullable=True)
    lang = Column(String(10), nullable=True)
    type = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)

    producer_metadata = db.relationship("ProducerMetadata", back_populates="parent", uselist=False, cascade="all, delete-orphan")

class Staff(db.Model):
    __tablename__ = 'staff'

    id = Column(String(255), primary_key=True)
    aid = Column(String(255), nullable=True)
    ismain = Column(Boolean, nullable=True)
    name = Column(String(255), nullable=True)
    original = Column(String(255), nullable=True)
    lang = Column(String(10), nullable=True)
    gender = Column(String(255), nullable=True)
    description = Column(Text, nullable=True)
    extlinks = Column(ARRAY(JSONB), nullable=True)
    aliases = Column(ARRAY(JSONB), nullable=True)

    staff_metadata = db.relationship("StaffMetadata", back_populates="parent", uselist=False, cascade="all, delete-orphan")

class Character(db.Model):
    __tablename__ = 'character'

    id = Column(String(255), primary_key=True)
    name = Column(String(255), nullable=True)
    original = Column(String(255), nullable=True)
    aliases = Column(ARRAY(String), nullable=True)
    description = Column(Text, nullable=True)
    blood_type = Column(String(255), nullable=True)
    height = Column(Integer, nullable=True)
    weight = Column(Integer, nullable=True)
    bust = Column(Integer, nullable=True)
    waist = Column(Integer, nullable=True)
    hips = Column(Integer, nullable=True)
    cup = Column(String(255), nullable=True)
    age = Column(Integer, nullable=True)
    birthday = Column(ARRAY(Integer), nullable=True)
    sex = Column(ARRAY(String), nullable=True)
    image = Column(JSONB, nullable=True)
    vns = Column(ARRAY(JSONB), nullable=True)
    traits = Column(ARRAY(JSONB), nullable=True)

    character_metadata = db.relationship("CharacterMetadata", back_populates="parent", uselist=False, cascade="all, delete-orphan")

class Trait(db.Model):
    __tablename__ = 'trait'

    id = Column(String(255), primary_key=True)
    name = Column(String(255), nullable=True)
    aliases = Column(ARRAY(String), nullable=True)
    description = Column(Text, nullable=True)
    searchable = Column(Boolean, nullable=True)
    applicable = Column(Boolean, nullable=True)
    group_id = Column(String(255), nullable=True)
    group_name = Column(String(255), nullable=True)
    char_count = Column(Integer, nullable=True)

    trait_metadata = db.relationship("TraitMetadata", back_populates="parent", uselist=False, cascade="all, delete-orphan")

# ----------------------------------------
# Variables 
# ----------------------------------------

ModelType = Union[VN, Tag, Producer, Staff, Character, Trait, Release]

MODEL_MAP = {
    'vn': VN, 
    'tag': Tag, 
    'producer': Producer,
    'staff': Staff, 
    'character': Character,
    'trait': Trait, 
    'release': Release
}