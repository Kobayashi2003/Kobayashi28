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
    title = Column(String(255))
    alttitle = Column(String(255))
    titles = Column(ARRAY(JSONB))
    aliases = Column(ARRAY(String))
    olang = Column(String(10))
    devstatus = Column(Integer)
    released = Column(Date)
    languages = Column(ARRAY(String))
    platforms = Column(ARRAY(String))
    image = Column(JSONB)
    length = Column(Integer)
    length_minutes = Column(Integer)
    length_votes = Column(Integer)
    description = Column(Text)
    screenshots = Column(ARRAY(JSONB))
    relations = Column(ARRAY(JSONB))
    tags = Column(ARRAY(JSONB))
    developers = Column(ARRAY(JSONB))
    editions = Column(ARRAY(JSONB))
    staff = Column(ARRAY(JSONB))
    va = Column(ARRAY(JSONB))
    extlinks = Column(ARRAY(JSONB))
    characters = Column(ARRAY(JSONB))
    releases = Column(ARRAY(JSONB))

    vn_metadata = db.relationship("VNMetadata", back_populates="parent", uselist=False, cascade="all, delete-orphan")

class Release(db.Model):
    __tablename__ ='release'

    id = Column(String(255), primary_key=True)
    title = Column(String(255))
    alttitle = Column(String(255))
    languages = Column(ARRAY(JSONB))
    platforms = Column(ARRAY(String))
    media = Column(ARRAY(JSONB))
    vns = Column(ARRAY(JSONB))
    producers = Column(ARRAY(JSONB))
    images = Column(ARRAY(JSONB))
    released = Column(Date)
    minage = Column(Integer)
    patch = Column(Boolean)
    freeware = Column(Boolean)
    uncensored = Column(Boolean)
    official = Column(Boolean)
    has_ero = Column(Boolean)
    resolution = Column(String)
    engine = Column(String)
    voiced = Column(Boolean)
    notes = Column(Text)
    gtin = Column(String(255))
    catalog = Column(String(255))
    extlinks = Column(ARRAY(JSONB))

class Tag(db.Model):
    __tablename__ = 'tag'

    id = Column(String(255), primary_key=True)
    aid = Column(String(255))
    name = Column(String(255))
    aliases = Column(ARRAY(String))
    description = Column(Text)
    category = Column(Enum('cont', 'ero', 'tech', name='tag_category_enum'))
    searchable = Column(Boolean)
    applicable = Column(Boolean)
    vn_count = Column(Integer)

    tag_metadata = db.relationship("TagMetadata", back_populates="parent", uselist=False, cascade="all, delete-orphan")

class Producer(db.Model):
    __tablename__ = 'producer'

    id = Column(String(255), primary_key=True)
    name = Column(String(255))
    original = Column(String(255))
    aliases = Column(ARRAY(String))
    lang = Column(String(10))
    type = Column(Enum('co', 'in', 'ng', name='producer_type_enum'))
    description = Column(Text)

    producer_metadata = db.relationship("ProducerMetadata", back_populates="parent", uselist=False, cascade="all, delete-orphan")

class Staff(db.Model):
    __tablename__ = 'staff'

    id = Column(String(255), primary_key=True)
    ismain = Column(Boolean)
    name = Column(String(255))
    original = Column(String(255))
    lang = Column(String(10))
    gender = Column(Enum('m', 'f', name='gender_enum'))
    description = Column(Text)
    extlinks = Column(ARRAY(JSONB))
    aliases = Column(ARRAY(JSONB))

    staff_metadata = db.relationship("StaffMetadata", back_populates="parent", uselist=False, cascade="all, delete-orphan")

class Character(db.Model):
    __tablename__ = 'character'

    id = Column(String(255), primary_key=True)
    name = Column(String(255))
    original = Column(String(255))
    aliases = Column(ARRAY(String))
    description = Column(Text)
    blood_type = Column(Enum('a', 'b', 'ab', 'o', name='blood_type_enum'))
    height = Column(Integer)
    weight = Column(Integer)
    bust = Column(Integer)
    waist = Column(Integer)
    hips = Column(Integer)
    cup = Column(Enum('AAA', 'AA', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', name='cup_size_enum'))
    age = Column(Integer)
    birthday = Column(ARRAY(Integer))
    sex = Column(ARRAY(Enum('m', 'f', 'b', 'n', name='sex_enum')))

    image = Column(JSONB)

    vns = Column(ARRAY(JSONB))
    traits = Column(ARRAY(JSONB))

    character_metadata = db.relationship("CharacterMetadata", back_populates="parent", uselist=False, cascade="all, delete-orphan")

class Trait(db.Model):
    __tablename__ = 'trait'

    id = Column(String(255), primary_key=True)
    name = Column(String(255))
    aliases = Column(ARRAY(String))
    description = Column(Text)
    searchable = Column(Boolean)
    applicable = Column(Boolean)
    group_id = Column(String(255))
    group_name = Column(String(255))
    char_count = Column(Integer)

    trait_metadata = db.relationship("TraitMetadata", back_populates="parent", uselist=False, cascade="all, delete-orphan")
# ----------------------------------------
# Variables 
# ----------------------------------------

ModelType = Union[VN, Tag, Producer, Staff, Character, Trait]

MODEL_MAP = {
    'vn': VN,
    'tag': Tag,
    'producer': Producer,
    'staff': Staff,
    'character': Character,
    'trait': Trait,
}