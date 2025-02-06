from typing import Union

from sqlalchemy import Column, String, Integer, Float, Boolean, Text, DateTime
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy.sql import func

from vndb import db

# ----------------------------------------
# Resources Models
# ----------------------------------------

class VN(db.Model):
    __tablename__ = 'vns'

    id = Column(String, primary_key=True)
    title = Column(String)
    alttitle = Column(String)
    titles = Column(ARRAY(JSONB))
    aliases = Column(ARRAY(String))
    olang = Column(String)
    devstatus = Column(Integer)
    released = Column(ARRAY(Integer))
    languages = Column(ARRAY(String))
    platforms = Column(ARRAY(String))
    image = Column(JSONB)
    length = Column(Integer)
    length_minutes = Column(Integer)
    length_votes = Column(Integer)
    description = Column(Text)
    average = Column(Float)
    rating = Column(Integer)
    votecount = Column(Integer)
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

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime)

class Release(db.Model):
    __tablename__ ='releases'

    id = Column(String, primary_key=True)
    title = Column(String)
    alttitle = Column(String)
    languages = Column(ARRAY(JSONB))
    platforms = Column(ARRAY(String))
    media = Column(ARRAY(JSONB))
    vns = Column(ARRAY(JSONB))
    producers = Column(ARRAY(JSONB))
    images = Column(ARRAY(JSONB))
    released = Column(ARRAY(Integer))
    minage = Column(Integer)
    patch = Column(Boolean)
    freeware = Column(Boolean)
    uncensored = Column(Boolean)
    official = Column(Boolean)
    has_ero = Column(Boolean)
    resolution = Column(JSONB)
    engine = Column(String)
    voiced = Column(Integer)
    notes = Column(Text)
    gtin = Column(String)
    catalog = Column(String)
    extlinks = Column(ARRAY(JSONB))

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime)

class Tag(db.Model):
    __tablename__ = 'tags'

    id = Column(String, primary_key=True)
    aid = Column(String)
    name = Column(String)
    aliases = Column(ARRAY(String))
    description = Column(Text)
    category = Column(String)
    searchable = Column(Boolean)
    applicable = Column(Boolean)
    vn_count = Column(Integer)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime)

class Producer(db.Model):
    __tablename__ = 'producers'

    id = Column(String, primary_key=True)
    name = Column(String)
    original = Column(String)
    aliases = Column(ARRAY(String))
    lang = Column(String)
    type = Column(String)
    description = Column(Text)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime)

class Staff(db.Model):
    __tablename__ = 'staff'

    id = Column(String, primary_key=True)
    aid = Column(String)
    ismain = Column(Boolean)
    name = Column(String)
    original = Column(String)
    lang = Column(String)
    gender = Column(String)
    description = Column(Text)
    extlinks = Column(ARRAY(JSONB))
    aliases = Column(ARRAY(JSONB))

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime)


    meta = db.relationship("StaffMetadata", back_populates="parent", uselist=False, cascade="all, delete-orphan")

class Character(db.Model):
    __tablename__ = 'characters'

    id = Column(String, primary_key=True)
    name = Column(String)
    original = Column(String)
    aliases = Column(ARRAY(String))
    description = Column(Text)
    blood_type = Column(String)
    height = Column(Integer)
    weight = Column(Integer)
    bust = Column(Integer)
    waist = Column(Integer)
    hips = Column(Integer)
    cup = Column(String)
    age = Column(Integer)
    birthday = Column(ARRAY(Integer))
    sex = Column(ARRAY(String))
    image = Column(JSONB)
    vns = Column(ARRAY(JSONB))
    traits = Column(ARRAY(JSONB))

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime)

class Trait(db.Model):
    __tablename__ = 'traits'

    id = Column(String, primary_key=True)
    name = Column(String)
    aliases = Column(ARRAY(String))
    description = Column(Text)
    searchable = Column(Boolean)
    applicable = Column(Boolean)
    group_id = Column(String)
    group_name = Column(String)
    char_count = Column(Integer)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
    deleted_at = Column(DateTime)

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