from typing import Union

from werkzeug.security import generate_password_hash, check_password_hash

from userserve import db
from sqlalchemy import Integer, String, Boolean, DateTime, Column, ForeignKey, event, UniqueConstraint
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import JSONB, ARRAY
from sqlalchemy.orm import relationship, declared_attr
from sqlalchemy.ext.mutable import MutableList


class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    is_admin = Column(Boolean, default=False, nullable=False)
    username = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255))
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    # Relationships
    vn_categories = relationship("VNCategory", back_populates="user", cascade="all, delete-orphan")
    release_categories = relationship("ReleaseCategory", back_populates="user", cascade="all, delete-orphan")
    character_categories = relationship("CharacterCategory", back_populates="user", cascade="all, delete-orphan")
    producer_categories = relationship("ProducerCategory", back_populates="user", cascade="all, delete-orphan")
    staff_categories = relationship("StaffCategory", back_populates="user", cascade="all, delete-orphan")
    tag_categories = relationship("TagCategory", back_populates="user", cascade="all, delete-orphan")
    trait_categories = relationship("TraitCategory", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __iter__(self):
        yield 'id', self.id
        yield 'username', self.username
        yield 'is_admin', self.is_admin
        yield 'created_at', self.created_at.isoformat() if self.created_at else None
        yield 'updated_at', self.updated_at.isoformat() if self.updated_at else None

    def __str__(self):
        return f"<User(id={self.id}, username={self.username}, is_admin={self.is_admin})>"

    def __repr__(self):
        return f"User(id={self.id!r}, username={self.username!r}, is_admin={self.is_admin!r})"

class Category(db.Model):
    __abstract__ = True

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    category_name = Column(String(255), nullable=False)
    marks = Column(MutableList.as_mutable(ARRAY(JSONB)), default=lambda: [])
    created_at = Column(DateTime(timezone=True), default=func.now())
    updated_at = Column(DateTime(timezone=True), default=func.now(), onupdate=func.now())

    @declared_attr
    def __table_args__(cls):
        return (
            UniqueConstraint('user_id', 'category_name', name=f'uq_{cls.__name__.lower()}_user_category'),
        )

    @property
    def type(self):
        raise NotImplementedError("Subclasses must implement this property")

    @declared_attr
    def __mapper_args__(cls):
        return {
            'polymorphic_identity': cls.type.fget(None),
        }

    def __iter__(self):
        yield 'id', self.id
        yield 'user_id', self.user_id
        yield 'category_name', self.category_name
        yield 'marks', self.marks
        yield 'type', self.type
        yield 'created_at', self.created_at.isoformat()
        yield 'updated_at', self.updated_at.isoformat()

    def __str__(self):
        return f"<{self.__class__.__name__}(id={self.id}, user_id={self.user_id}, category_name={self.category_name}, type={self.type})>"

    def __repr__(self):
        return f"{self.__class__.__name__}(id={self.id!r}, user_id={self.user_id!r}, category_name={self.category_name!r}, type={self.type!r})"

class VNCategory(Category):

    __tablename__ = 'vn_categories'

    @property
    def type(self):
        return 'vn'

    user = relationship("User", back_populates="vn_categories")

class ReleaseCategory(Category):

    __tablename__ = 'release_categories'

    @property
    def type(self):
        return 'release'

    user = relationship("User", back_populates="release_categories")

class CharacterCategory(Category):

    __tablename__ = 'character_categories'

    @property
    def type(self):
        return 'character'

    user = relationship("User", back_populates="character_categories")

class ProducerCategory(Category):

    __tablename__ = 'producer_categories'

    @property
    def type(self):
        return 'producer'

    user = relationship("User", back_populates="producer_categories")

class StaffCategory(Category):

    __tablename__ = 'staff_categories'

    @property
    def type(self):
        return 'staff'

    user = relationship("User", back_populates="staff_categories")

class TagCategory(Category):

    __tablename__ = 'tag_categories'

    @property
    def type(self):
        return 'tag'

    user = relationship("User", back_populates="tag_categories")

class TraitCategory(Category):

    __tablename__ = 'trait_categories'

    @property
    def type(self):
        return 'trait'

    user = relationship("User", back_populates="trait_categories")

CategoryType = Union[VNCategory, CharacterCategory, ProducerCategory, StaffCategory]

CATEGORY_MODEL = {
    'v': VNCategory,
    'r': ReleaseCategory,
    'c': CharacterCategory,
    'p': ProducerCategory,
    's': StaffCategory,
    'g': TagCategory,
    'i': TraitCategory
}

ModelType = Union[
    User, VNCategory, ReleaseCategory, CharacterCategory, 
    ProducerCategory, StaffCategory, TagCategory, TraitCategory
]

MODEL_MAP = {
    'user': User,
    'vn': VNCategory,
    'release': ReleaseCategory,
    'character': CharacterCategory,
    'producer': ProducerCategory,
    'staff': StaffCategory,
    'tag': TagCategory,
    'trait': TraitCategory
}

def create_default_categories(mapper, connection, target):
    session = db.Session(bind=connection)
    for category_class in CATEGORY_MODEL.values():
        default_category = category_class(user_id=target.id, category_name="Default")
        session.add(default_category)
    session.commit()

event.listen(User, 'after_insert', create_default_categories)