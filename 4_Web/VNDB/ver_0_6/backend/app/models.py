from sqlalchemy import Column, String, Integer, Numeric, Boolean, Text
from sqlalchemy.types import TypeDecorator
from sqlalchemy.dialects.postgresql import JSONB, ARRAY

from app import db

class Title(TypeDecorator):
    impl = JSONB

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        lang : str = value.get('lang')
        title : str = value.get('title')
        latin : str | None = value.get('latin')
        official : bool = value.get('official')
        main : bool = value.get('main')
        return {k: v for k, v in locals().items() if k not in {'self', 'value', 'dialect'}}

    def process_result_value(self, value, dialect):
        return value

class Edition(TypeDecorator):
    impl = JSONB

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        eid : int = value.get('eid')
        lang : str | None = value.get('lang')
        name : str = value.get('name')
        official: bool = value.get('official')
        return {k: v for k, v in locals().items() if k not in {'self', 'value', 'dialect'}}

    def process_result_value(self, value, dialect):
        return value

class Language(TypeDecorator):
    impl = JSONB

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        lang : str = value.get('lang')
        title : str | None = value.get('title')
        latin : str | None = value.get('latin')
        mtl : bool = value.get('mtl')
        main : bool = value.get('main')
        return {k: v for k, v in locals().items() if k not in {'self', 'value', 'dialect'}}

    def process_result_value(self, value, dialect):
        return value

class Alias(TypeDecorator):
    impl = JSONB

    def process_bind_param(self, value, dialect):
        if value is None:
            return None
        aid : int = value.get('aid')
        name : str = value.get('name')
        latin : str = value.get('latin')
        ismain : bool = value.get('ismain')
        return {k: v for k, v in locals().items() if k not in {'self', 'value', 'dialect'}}

    def process_result_value(self, value, dialect):
        return value

class Media(TypeDecorator):
    impl = JSONB 

    def process_bind_param(self, value, dialect):
        if value is not None:
            return None
        medium : str = value.get('medium')
        qty: int = value.get('qty')
        return {k: v for k, v in locals().items() if k not in {'self', 'value', 'dialect'}}

    def process_result_value(self, value, dialect):
        return value

class Resolution(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        if value is None or isinstance(value, str):
            return value
        return f"{value[0]}x{value[1]}"

    def process_result_value(self, value, dialect):
        if value is None or value == "non-standard":
            return value
        width, height = map(int, value.split('x'))
        return [width, height]

class Birthday(TypeDecorator):
    impl = String

    def process_bind_param(self, value, dialect):
        if value is None:
            return value
        return f"{value[0]}-{value[1]}"

    def process_result_value(self, value, dialect):
        if value is None:
            return value
        month, day = map(int, value.split('-'))
        return [month, day]

class VisualNovel(db.Model):
    __tablename__ = 'visual_novels'
    id = Column(String(255), primary_key=True)
    title = Column(String(255))
    alttitle = Column(String(255))
    titles = Column(ARRAY(Title))
    aliases = Column(ARRAY(String))
    olang = Column(String(255))
    devstatus = Column(Integer)
    released = Column(String(255))
    languages = Column(ARRAY(String))
    platforms = Column(ARRAY(String))
    length = Column(Integer)
    length_minutes = Column(Integer)
    length_votes = Column(Integer)
    description = Column(Text)
    average = Column(Numeric)
    rating = Column(Numeric)
    votecount = Column(Integer)
    editions = Column(ARRAY(Edition))

class Release(db.Model):
    __tablename__ = 'releases'
    id = Column(String(255), primary_key=True)
    title = Column(String(255))
    alttitle = Column(String(255))
    languages = Column(Language)
    platforms = Column(ARRAY(String))
    media = Column(ARRAY(Media))
    released = Column(String(255))
    minage = Column(Integer)
    patch = Column(Boolean)
    freeware = Column(Boolean)
    uncensored = Column(Boolean)
    official = Column(Boolean)
    has_ero = Column(Boolean)
    resolution = Column(Resolution)
    engine = Column(String(255))
    voiced = Column(Integer)
    ntoes = Column(Text)
    gtin = Column(String(255))
    catalog = Column(String)

class Producer(db.Model):
    __tablename__ = 'producers'
    id = Column(String(255), primary_key=True)
    name = Column(String(255))
    original = Column(String(255))
    aliases = Column(ARRAY(String))
    lang = Column(String(255))
    type = Column(String(255))
    description = Column(Text)

class Character(db.Model):
    __tablename__ = 'characters'
    id = Column(String(255), primary_key=True)
    name = Column(String(255))
    original = Column(String(255))
    aliases = Column(ARRAY(String))
    description = Column(Text)
    blood_type = Column(String(255))
    height = Column(Integer)
    weight = Column(Integer)
    bust = Column(Integer)
    waist = Column(Integer)
    hips = Column(Integer)
    cup = Column(String(255))
    age = Column(Integer)
    birthday = Column(Birthday)
    sex = Column(ARRAY(String)) # TODO

class Staff(db.Model):
    __tablename__ = 'staff'
    id = Column(String(255), primary_key=True)
    aid = Column(Integer)
    ismain = Column(Boolean)
    name = Column(String(255))
    original = Column(String(255))
    lang = Column(String(255))
    gender = Column(String(255))
    description = Column(Text)
    aliases = Column(ARRAY(Alias))

class Tag(db.Model):
    __tablename__ = 'tags'
    id = Column(String(255), primary_key=True)
    name = Column(String(255))
    aliases = Column(ARRAY(String))
    description = Column(Text)
    category = Column(String(255))
    searchable = Column(Boolean)
    applicable = Column(Boolean)
    vn_count = Column(Integer)

class Trait(db.Model):
    __tablename__ = 'traits'
    id = Column(String(255), primary_key=True)
    name = Column(String(255))
    aliases = Column(ARRAY(String))
    description = Column(Text)
    searchable = Column(Boolean)
    applicable = Column(Boolean)
    group_id = Column(String(255)) #TODO
    group_name = Column(String(255)) #TODO
    char_count = Column(Integer)


class Image(db.Model):
    __abstract__ = True
    id = Column(String(255), primary_key=True)
    url = Column(String)
    dims = Column(ARRAY(Integer))
    sexual = Column(Numeric)
    violence = Column(Numeric)
    votecount = Column(Integer)

class CoverImage(Image):
    __tablename__ = 'cover_images'
    thumbnail = Column(String)
    thumbnail_dims = Column(ARRAY(Integer))

class ScreenShot(Image):
    __tablename__ = 'screenshots'
    thumbnail = Column(String)
    thumbnail_dims = Column(ARRAY(Integer))

class CharacterImage(Image):
    __tablename__ = 'character_images'

class Extlink(db.Model):
    __tablename__ = 'extlinks'
    id = Column(String(255), primary_key=True)
    url = Column(String(255))
    label = Column(String(255))
    name = Column(String(255))