from sqlalchemy import Column, String, Integer, Float, Boolean, Text, ForeignKey, Table
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy.orm import relationship
from app import db

vn_cv = Table('vn_cv', db.Model.metadata,
    Column('vn_id', String, ForeignKey('vns.id'), primary_key=True),
    Column('cv_id', String, ForeignKey('cv.id'), primary_key=True)
)

vn_vn = Table('vn_vn', db.Model.metadata,
    Column('vn1_id', String, ForeignKey('vns.id'), primary_key=True),
    Column('vn2_id', String, ForeignKey('vns.id'), primary_key=True),
    Column('relation', String),
    Column('relation_official', Boolean)
)

vn_sf = Table('vn_sf', db.Model.metadata,
    Column('vn_id', String, ForeignKey('vns.id'), primary_key=True),
    Column('sf_id', String, ForeignKey('sf.id'), primary_key=True)
)

vn_tag = Table('vn_tag', db.Model.metadata,
    Column('vn_id', String, ForeignKey('vns.id'), primary_key=True),
    Column('tag_id', String, ForeignKey('tags.id'), primary_key=True),
    Column('rating', Float),
    Column('spoiler', Integer),
    Column('lie', Boolean)
)

vn_producer = Table('vn_producer', db.Model.metadata,
    Column('vn_id', String, ForeignKey('vns.id'), primary_key=True),
    Column('producer_id', String, ForeignKey('producers.id'), primary_key=True)
)

vn_staff = Table('vn_staff', db.Model.metadata,
    Column('vn_id', String, ForeignKey('vns.id'), primary_key=True),
    Column('staff_id', String, ForeignKey('staff.id'), primary_key=True),
    Column('eid', Integer),
    Column('role', String),
    Column('note', Text)
)

vn_extlink = Table('vn_extlink', db.Model.metadata,
    Column('vn_id', String, ForeignKey('vns.id'), primary_key=True),
    Column('extlink_id', String, ForeignKey('extlinks.id'), primary_key=True)
)

release_vn = Table('release_vn', db.Model.metadata,
    Column('release_id', String, ForeignKey('releases.id'), primary_key=True),
    Column('vn_id', String, ForeignKey('vns.id'), primary_key=True),
    Column('rtype', String)
)

release_producer = Table('release_producer', db.Model.metadata,
    Column('release_id', String, ForeignKey('releases.id'), primary_key=True),
    Column('producer_id', String, ForeignKey('producers.id'), primary_key=True),
    Column('developer', Boolean),
    Column('publisher', Boolean)
)

release_cv = Table('release_cv', db.Model.metadata,
    Column('release_id', String, ForeignKey('releases.id'), primary_key=True),
    Column('cv_id', String, ForeignKey('cv.id'), primary_key=True),
    Column('type', String),
    Column('vn', String, ForeignKey('vns.id')),
    Column('languages', ARRAY(String)),
    Column('photo', Boolean)
)

release_extlink = Table('release_extlink', db.Model.metadata,
    Column('release_id', String, ForeignKey('releases.id'), primary_key=True),
    Column('extlink_id', String, ForeignKey('extlinks.id'), primary_key=True)
)

character_ch = Table('character_ch', db.Model.metadata,
    Column('character_id', String, ForeignKey('characters.id'), primary_key=True),
    Column('ch_id', String, ForeignKey('ch.id'), primary_key=True)
)

character_vn = Table('character_vn', db.Model.metadata,
    Column('character_id', String, ForeignKey('characters.id'), primary_key=True),
    Column('vn_id', String, ForeignKey('vns.id'), primary_key=True),
    Column('spoiler', Integer),
    Column('role', String)
)

character_trait = Table('character_trait', db.Model.metadata,
    Column('character_id', String, ForeignKey('characters.id'), primary_key=True),
    Column('trait_id', String, ForeignKey('traits.id'), primary_key=True),
    Column('spoiler', Integer),
    Column('lie', Boolean)
)

producer_extlink = Table('producer_extlink', db.Model.metadata,
    Column('producer_id', String, ForeignKey('producers.id'), primary_key=True),
    Column('extlink_id', String, ForeignKey('extlinks.id'), primary_key=True)
)

staff_extlink = Table('staff_extlink', db.Model.metadata,
    Column('staff_id', String, ForeignKey('staff.id'), primary_key=True),
    Column('extlink_id', String, ForeignKey('extlinks.id'), primary_key=True)
)

class VoiceActor(db.Model):
    __tablename__ = 'va'
    vn_id = Column(String, ForeignKey('vns.id'), primary_key=True)
    character_id = Column(String, ForeignKey('characters.id'), primary_key=True)
    staff_id = Column(String, ForeignKey('staff.id'), primary_key=True)
    note = Column(Text)

    vn = relationship('VisualNovel', back_populates='va')
    character = relationship('Character', back_populates='va')
    staff = relationship('Staff', back_populates='va')

class Appearance(db.Model):
    __tablename__ = 'appearances'
    character_id = Column(String, ForeignKey('characters.id'), primary_key=True)
    vn_id = Column(String, ForeignKey('vns.id'), primary_key=True)
    release_id = Column(String, ForeignKey('releases.id'), primary_key=True)

    character = relationship('Character', back_populates='appearances')
    vn = relationship('VisualNovel', back_populates='appearances')
    release = relationship('Release', back_populates='appearances')

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
    average = Column(Float)
    rating = Column(Float)
    votecount = Column(Integer)
    editions = Column(ARRAY(JSONB))

    # One-to-one relationship with Cover
    image = relationship('Cover', secondary=vn_cv, uselist=False, back_populates='vn')

    # Self-referential many-to-many relationship
    relations = relationship(
        'VisualNovel',
        secondary=vn_vn,
        primaryjoin=(id == vn_vn.c.vn1_id),
        secondaryjoin=(id == vn_vn.c.vn2_id),
        backref='relations_reverse'
    )

    # One-to-many relationship with Screenshot
    screenshots = relationship('Screenshot', secondary=vn_sf, back_populates='vn')

    # Many-to-many relationship with Tag
    tags = relationship('Tag', secondary=vn_tag, back_populates='vns')

    # Many-to-many relationship with Producer
    developers = relationship('Producer', secondary=vn_producer, back_populates='vns')

    # Many-to-many relationship with Staff
    staff = relationship('Staff', secondary=vn_staff, back_populates='vns')

    # Many-to-many relationship with Extlink
    extlinks = relationship('Extlink', secondary=vn_extlink, back_populates='vns')

    # Many-to-many relationship with Release
    releases = relationship('Release', secondary=release_vn, back_populates='vns')

    # Many-to-many relationship with Character
    characters = relationship('Character', secondary=character_vn, back_populates='vns')

    # Ternary relationship
    va = relationship('VoiceActor', back_populates='vn')

    # Ternary relationship
    appearances = relationship('Appearance', back_populates='vn')

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

    # Many-to-many relationship with VisualNovel
    vns = relationship('VisualNovel', secondary=release_vn, back_populates='releases')

    # Many-to-many relationship with Producer
    producers = relationship('Producer', secondary=release_producer, back_populates='releases') 

    # One-to-many relationship with Cover
    images = relationship('Cover', secondary=release_cv, back_populates='release') 

    # Many-to-many relationship with Extlink
    extlinks = relationship('Extlink', secondary=release_extlink, back_populates='releases')

    # Ternary relationship
    appearances = relationship('Appearance', back_populates='release')

class Producer(db.Model):
    __tablename__  = 'producers'
    id = Column(String, primary_key=True)
    name = Column(String)
    original = Column(String)
    aliases = Column(ARRAY(String))
    lang = Column(String)
    type = Column(String)
    description = Column(Text)

    # Many-to-many relationship with VisualNovel
    vns = relationship('VisualNovel', secondary=vn_producer, back_populates='developers')

    # Many-to-many relationship with Release
    releases = relationship('Release', secondary=release_producer, back_populates='producers')

    # Many-to-many relationship with Extlink
    extlinks = relationship('Extlink', secondary=producer_extlink, back_populates='producers')

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

    # One-to-one relationship with CharacterImage
    image = relationship('CharacterImage', secondary=character_ch, uselist=False, back_populates='character')

    # Many-to-many relationship with VisualNovel
    vns = relationship('VisualNovel', secondary=character_vn, back_populates='characters')

    # Many-to-Many relationship with Trait
    traits = relationship('Trait', secondary=character_trait, back_populates='characters')

    # Ternary relationship
    va = relationship('VoiceActor', back_populates='character')

    # Ternary relationship
    appearances = relationship('Appearance', back_populates='character')

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

    # Many-to-many relationship with Extlink
    extlinks = relationship('Extlink', secondary=staff_extlink, back_populates='staff')

    # Many-to-many relationship with VisualNovels
    vns = relationship('VisualNovel', secondary=vn_staff, back_populates='staff')

    # Ternary relationship
    va = relationship('VoiceActor', back_populates='staff')

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

    # Many-to-many relationship with VisualNovel
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
    group_id = Column(String)
    group_name = Column(String)

    # Many-to-many relationship with Trait
    characters = relationship('Character', secondary=character_trait, back_populates='traits')

class Image(db.Model):
    __abstract__ = True
    url = Column(String)
    dims = Column(ARRAY(Integer))
    sexual = Column(Float)
    violence = Column(Float)
    votecount = Column(Integer)

class Cover(Image):
    __tablename__ = 'cv'
    id = Column(String(255), primary_key=True)
    thumbnail = Column(String)
    thumbnail_dims = Column(ARRAY(Integer))

    # One-to-one relationship with VisualNovel
    vn = relationship('VisualNovel', secondary=vn_cv, uselist=False, back_populates='image')

    # Many-to-one relationship with Release
    release = relationship('Release', secondary=release_cv, uselist=False, back_populates='images')

class Screenshot(Image):
    __tablename__ = 'sf'
    id = Column(String(255), primary_key=True)
    thumbnail = Column(String)
    thumbnail_dims = Column(ARRAY(Integer))

    # Many-to-one relationship with VisualNovel
    vn = relationship('VisualNovel', secondary=vn_sf, uselist=False, back_populates='screenshots')

class CharacterImage(Image):
    __tablename__ = 'ch'
    id = Column(String(255), primary_key=True)

    # One-to-one relationship with Character
    character = relationship('Character', secondary=character_ch, uselist=False, back_populates='image')

class Extlink(db.Model):
    __tablename__ = 'extlinks'
    id = Column(String, primary_key=True)
    url = Column(String)
    label = Column(String)
    name = Column(String)

    # Many-to-many relationship with VisualNovel
    vns = relationship('VisualNovel', secondary=vn_extlink, back_populates='extlinks')

    # Many-to-many relationship with Release
    releases = relationship('Release', secondary=release_extlink, back_populates='extlinks')

    # Many-to-many relationship with Producer
    producers = relationship('Producer', secondary=producer_extlink, back_populates='extlinks')

    # Many-to-many relationship with Staff
    staff = relationship('Staff', secondary=staff_extlink, back_populates='extlinks')