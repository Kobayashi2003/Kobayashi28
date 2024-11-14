from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.sql import func

from api import db

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

    local_vn = db.relationship("LocalVN", back_populates="vn", uselist=False)
    local_images = db.relationship("VNImage", back_populates="vn", cascade="all, delete-orphan")

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

    local_tag = db.relationship("LocalTag", back_populates="tag", uselist=False)

class Producer(db.Model):
    __tablename__ = 'producer'

    id = db.Column(db.String(255), primary_key=True)
    name = db.Column(db.String(255))
    original = db.Column(db.String(255))
    aliases = db.Column(ARRAY(db.String))
    lang = db.Column(db.String(10))
    type = db.Column(db.Enum('co', 'in', 'ng', name='producer_type_enum'))
    description = db.Column(db.Text)

    local_producer = db.relationship("LocalProducer", back_populates="producer", uselist=False)

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

    local_staff = db.relationship("LocalStaff", back_populates="staff", uselist=False)

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

    local_character = db.relationship("LocalCharacter", back_populates="character", uselist=False)
    local_images = db.relationship("CharacterImage", back_populates="character", cascade="all, delete-orphan")

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

    local_trait = db.relationship("LocalTrait", back_populates="trait", uselist=False)

class LocalVN(db.Model):
    __tablename__ = 'local_vn'

    id = db.Column(db.String(255), db.ForeignKey('vn.id'), primary_key=True)
    downloaded = db.Column(db.Boolean, default=False)
    last_updated = db.Column(db.DateTime, default=func.now())

    vn = db.relationship("VN", back_populates="local_vn")

class LocalTag(db.Model):
    __tablename__ = 'local_tag'

    id = db.Column(db.String(255), db.ForeignKey('tag.id'), primary_key=True)
    downloaded = db.Column(db.Boolean, default=False)
    last_updated = db.Column(db.DateTime, default=func.now())

    tag = db.relationship("Tag", back_populates="local_tag")

class LocalProducer(db.Model):
    __tablename__ = 'local_producer'

    id = db.Column(db.String(255), db.ForeignKey('producer.id'), primary_key=True)
    downloaded = db.Column(db.Boolean, default=False)
    last_updated = db.Column(db.DateTime, default=func.now())

    producer = db.relationship("Producer", back_populates="local_producer")

class LocalStaff(db.Model):
    __tablename__ = 'local_staff'

    id = db.Column(db.String(255), db.ForeignKey('staff.id'), primary_key=True)
    downloaded = db.Column(db.Boolean, default=False)
    last_updated = db.Column(db.DateTime, default=func.now())

    staff = db.relationship("Staff", back_populates="local_staff")

class LocalCharacter(db.Model):
    __tablename__ = 'local_character'

    id = db.Column(db.String(255), db.ForeignKey('character.id'), primary_key=True)
    downloaded = db.Column(db.Boolean, default=False)
    last_updated = db.Column(db.DateTime, default=func.now())

    character = db.relationship("Character", back_populates="local_character")

class LocalTrait(db.Model):
    __tablename__ = 'local_trait'

    id = db.Column(db.String(255), db.ForeignKey('trait.id'), primary_key=True)
    downloaded = db.Column(db.Boolean, default=False)
    last_updated = db.Column(db.DateTime, default=func.now())

    trait = db.relationship("Trait", back_populates="local_trait")

class Image(db.Model):
    __abstract__ = True

    id = db.Column(db.String(255), primary_key=True)
    image_type = db.Column(db.String(50))

    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

class VNImage(Image):
    vn_id = db.Column(db.String(255), db.ForeignKey('vn.id'))
    vn = db.relationship("VN", back_populates="local_images")

class CharacterImage(Image):
    character_id = db.Column(db.String(255), db.ForeignKey('character.id'))
    character = db.relationship("Character", back_populates="local_images")