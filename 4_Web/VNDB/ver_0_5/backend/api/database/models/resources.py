from typing import Union

from api import db
from sqlalchemy.dialects.postgresql import JSONB, ARRAY

# ----------------------------------------
# Resources Models
# ----------------------------------------

class VN(db.Model):
    __tablename__ = 'vn'

    id = db.Column(db.String(255), primary_key=True)
    title = db.Column(db.String(255))
    titles = db.Column(ARRAY(JSONB))
    aliases = db.Column(ARRAY(db.String))
    olang = db.Column(db.String(10))
    devstatus = db.Column(db.Integer)
    released = db.Column(db.Date)
    languages = db.Column(ARRAY(db.String))
    platforms = db.Column(ARRAY(db.String))
    length = db.Column(db.Integer)
    length_minutes = db.Column(db.Integer)
    description = db.Column(db.Text)
    extlinks = db.Column(ARRAY(JSONB))

    image = db.Column(JSONB)
    screenshots = db.Column(ARRAY(JSONB))

    relations = db.Column(ARRAY(JSONB))
    tags = db.Column(ARRAY(JSONB))
    developers = db.Column(ARRAY(JSONB))
    staff = db.Column(ARRAY(JSONB))
    characters = db.Column(ARRAY(JSONB))
    va = db.Column(ARRAY(JSONB))

    vn_metadata = db.relationship("VNMetadata", back_populates="parent", uselist=False, cascade="all, delete-orphan")

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

    staff_metadata = db.relationship("StaffMetadata", back_populates="parent", uselist=False, cascade="all, delete-orphan")

class Character(db.Model):
    __tablename__ = 'character'

    id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255))
    original = db.Column(db.String(255))
    aliases = db.Column(ARRAY(db.String))
    description = db.Column(db.Text)
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

    image = db.Column(JSONB)

    vns = db.Column(ARRAY(JSONB))
    traits = db.Column(ARRAY(JSONB))

    character_metadata = db.relationship("CharacterMetadata", back_populates="parent", uselist=False, cascade="all, delete-orphan")

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

    trait_metadata = db.relationship("TraitMetadata", back_populates="parent", uselist=False, cascade="all, delete-orphan")

# ----------------------------------------
# Variables 
# ----------------------------------------

ModelType = Union[
    VN, Tag, Producer, Staff, 
    Character, Trait 
]

MODEL_MAP = {
    'vn': VN,
    'tag': Tag,
    'producer': Producer,
    'staff': Staff,
    'character': Character,
    'trait': Trait,
}