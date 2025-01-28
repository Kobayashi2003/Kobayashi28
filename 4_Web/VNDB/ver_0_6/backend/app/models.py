from sqlalchemy import Column, String, Integer, Numeric, Boolean, Text, ForeignKey, Table
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy.orm import relationship

from app import db

vn_vn = Table('vn_vn', db.Model.metadata,
    Column('vn_id', String, ForeignKey('visual_novels.id'), primary_key=True),
    Column('related_vn_id', String, ForeignKey('visual_novels.id'), primary_key=True),
    Column('relation', String),
    Column('relation_official', Boolean)
)

vn_tag = Table('vn_tag', db.Model.metadata,
    Column('vn_id', String, ForeignKey('visual_novels.id'), primary_key=True),
    Column('tag_id', String, ForeignKey('tags.id'), primary_key=True),
    Column('rating', Numeric),
    Column('spoiler', Integer),
    Column('lie', Boolean)
)

vn_producer = Table('vn_producer', db.Model.metadata,
    Column('vn_id', String, ForeignKey('visual_novels.id')),
    Column('producer_id', String, ForeignKey('producers.id'))
)

class VisualNovel(db.Model):
    __tablename__ = 'vns'
    id = Column(String, primary_key=True)
    title = Column(String)
    alttitle = Column(String)
    titles = Column(ARRAY(JSONB))
    aliases = Column(ARRAY(String))
    olang = Column(String)
    devstatus = Column(Integer)
    released = Column(String)
    languages = Column(ARRAY(String))
    platforms = Column(ARRAY(String))
    length = Column(Integer)
    length_minutes = Column(Integer)
    description = Column(Text)
    average = Column(Numeric)
    rating = Column(Numeric)
    votecount = Column(Integer)
    editions = Column(ARRAY(JSONB))

    # One-to-one relationship with Cover
    image = relationship('Cover', back_populates='vn', uselist=False)

    # Self-referential many-to-many relationship
    relations = relationship(
        'VisualNovel',
        secondary=vn_vn,
        primaryjoin=(id == vn_vn.c.vn_id),
        secondaryjoin=(id == vn_vn.c.related_vn_id),
        backref='related_to'
    ) # TODO

    # One-to-many relationship with Screenshot
    screenshots = relationship('Screenshot', back_populates='vn')

    # Many-to-many relationship with Tag
    tags = relationship('Tag', secondary=vn_tag, back_populates='vns')

    # Many-to-many relationship with Producer
    developers = relationship('Producer', secondary=vn_producer, back_populates='vns')

class Release(db.Model):
    __tablename__ = 'releases'
    id = Column(String, primary_key=True)
    title = Column(String)
    alttitle = Column(String)
    languages = Column(ARRAY(JSONB))
    platforms = Column(ARRAY(String))
    media = Column(ARRAY(JSONB))
    released = Column(String)
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

class Producer(db.Model):
    __tablename__  = 'producers'
    id = Column(String, primary_key=True)
    name = Column(String)
    original = Column(String)
    aliases = Column(ARRAY(String))
    lang = Column(String)
    type = Column(String)
    description = Column(Text)

    vns = relationship('VisualNovel', secondary=vn_producer, back_populates='developers')

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

class Staff(db.Model):
    __tablename__ = 'staff'
    id = Column(String, primary_key=True)
    aid = Column(Integer)
    ismain = Column(Boolean)
    name = Column(String)
    original = Column(String)
    lang = Column(String)
    gender = Column(String)
    description = Column(Text)
    aliases = Column(ARRAY(JSONB))

class Tag(db.Model):
    __tablename__ = 'tags'
    id = Column(String, primary_key=True)
    name = Column(String)
    aliases = Column(ARRAY(String))
    description = Column(Text)
    category = Column(String)
    searchable = Column(Boolean)
    applicable = Column(Boolean)
    vn_count = Column(Integer)

    vns = relationship('VisualNovel', secondary=vn_tag, back_populates='tags')

class Trait(db.Model):
    __tablename__ = 'traits'
    id = Column(String, primary_key=True)
    name = Column(String)
    aliases = Column(ARRAY(String))
    description = Column(Text)
    searchable = Column(Boolean)
    applicable = Column(Boolean)
    char_count = Column(Integer)

class Image(db.Model):
    __abstract__ = True
    id = Column(String(255), primary_key=True)
    url = Column(String)
    dims = Column(ARRAY(Integer))
    sexual = Column(Numeric)
    violence = Column(Numeric)
    votecount = Column(Integer)

class Cover(Image):
    __tablename__ = 'cv'
    thumbnail = Column(String)
    thumbnail_dims = Column(ARRAY(Integer))

    vn_id = Column(String, ForeignKey('visual_novels.id'))
    vn = relationship('VisualNovel', back_populates='image', uselist=False)

class Screenshot(Image):
    __tablename__ = 'sf'
    thumbnail = Column(String)
    thumbnail_dims = Column(ARRAY(Integer))

    vn_id = Column(String, ForeignKey('visual_novels.id'))
    vn = relationship('VisualNovel', back_populates='screenshots', uselist=False)

class CharacterImage(Image):
    __tablename__ = 'ch'

class Extlink(db.Model):
    __tablename__ = 'extlinks'
    id = Column(String, primary_key=True)
    url = Column(String)
    label = Column(String)
    name = Column(String)