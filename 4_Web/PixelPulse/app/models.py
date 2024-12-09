from app import db
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship, declared_attr
from sqlalchemy.ext.hybrid import hybrid_property
from datetime import datetime, timezone


user_follow = db.Table('user_follow',
    Column('follower_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    Column('followed_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    Column('created_at', DateTime, default=lambda: datetime.now(timezone.utc))
)

user_ignored_tag = db.Table('user_ignored_tag',
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True),
    Column('ignored_at', DateTime, default=lambda: datetime.now(timezone.utc))
)

user_liked_image = db.Table('user_liked_image',
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    Column('image_id', Integer, ForeignKey('images.id', ondelete='CASCADE'), primary_key=True),
    Column('liked_at', DateTime, default=lambda: datetime.now(timezone.utc))
)

user_favorited_image = db.Table('user_favorited_image',
    Column('user_id', Integer, ForeignKey('users.id', ondelete='CASCADE'), primary_key=True),
    Column('image_id', Integer, ForeignKey('images.id', ondelete='CASCADE'), primary_key=True),
    Column('favorited_at', DateTime, default=lambda: datetime.now(timezone.utc))
)

image_tag_association = db.Table('image_tag_association',
    Column('image_id', Integer, ForeignKey('images.id', ondelete='CASCADE'), primary_key=True),
    Column('tag_id', Integer, ForeignKey('tags.id', ondelete='CASCADE'), primary_key=True)
)

image_collection_association = db.Table('image_collection_association',
    Column('image_id', Integer, ForeignKey('images.id', ondelete='CASCADE'), primary_key=True),
    Column('collection_id', Integer, ForeignKey('collections.id', ondelete='CASCADE'), primary_key=True)
)


class SoftDeleteMixin:
    @declared_attr
    def is_active(cls):
        return Column(Boolean, default=True, nullable=False)

    @declared_attr
    def deleted_at(cls):
        return Column(DateTime, nullable=True)

    @hybrid_property
    def is_deleted(self):
        return not self.is_active

    @is_deleted.expression
    def is_deleted(cls):
        return cls.is_active == False

    def delete(self, hard=False):
        if hard:
            db.session.delete(self)
        else:
            self.is_active = False
            self.deleted_at = datetime.now(timezone.utc)

    def restore(self):
        self.is_active = True
        self.deleted_at = None

    @classmethod
    def not_deleted(cls):
        return cls.query.filter(cls.is_active == True)


class User(db.Model, SoftDeleteMixin):
    __tablename__ = 'users'
    __table_args__ = (
        UniqueConstraint('username', 'is_active', name='uq_username_deleted_at'),
        UniqueConstraint('email', 'is_active', name='uq_email_deleted_at'),
    )

    id = Column(Integer, primary_key=True)
    username = Column(String(64), nullable=False, index=True)
    email = Column(String(128), nullable=False, index=True)
    password_hash = Column(String(256), nullable=False)
    bio = Column(Text, nullable=True)
    last_login = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)
    deleted_at = Column(DateTime, nullable=True, index=True)
    is_active = Column(Boolean, default=True, nullable=False)

    images = relationship('Image', back_populates='user', cascade='all, delete-orphan', lazy='dynamic')
    comments = relationship('Comment', back_populates='user', cascade='all, delete-orphan', lazy='dynamic')
    collections = relationship('Collection', back_populates='user', cascade='all, delete-orphan', lazy='dynamic')
    tags = relationship('Tag', back_populates='user', cascade='all, delete-orphan', lazy='dynamic')

    followers = relationship(
        'User', secondary=user_follow,
        primaryjoin=(user_follow.c.followed_id == id),
        secondaryjoin=(user_follow.c.follower_id == id),
        backref=db.backref('following', lazy='dynamic', cascade='all, delete'),
        lazy='dynamic',
        cascade='all, delete'
    )
    liked_images = relationship('Image', secondary=user_liked_image, back_populates='liked_by', cascade='all, delete', lazy='dynamic')
    favorited_images = relationship('Image', secondary=user_favorited_image, back_populates='favorited_by', cascade='all, delete', lazy='dynamic')
    ignored_tags = relationship('Tag', secondary=user_ignored_tag, back_populates='ignored_by', cascade='all, delete', lazy='dynamic')

    @property
    def follower_count(self):
        return self.followers.count()

    @property
    def following_count(self):
        return self.following.count()

    @property
    def image_count(self):
        return self.images.count()
    
    @property
    def comment_count(self):
        return self.comments.count()

    @property
    def collection_count(self):
        return self.collections.count()
    
    @property
    def tag_count(self):
        return self.tags.count()

    @property
    def liked_image_count(self):
        return self.liked_images.count()

    @property
    def favorited_image_count(self):
        return self.favorited_images.count()

    @property
    def ignored_tag_count(self):
        return self.ignored_tags.count()

class Image(db.Model, SoftDeleteMixin):
    __tablename__ = 'images'

    id = Column(Integer, primary_key=True)
    title = Column(String(128), nullable=False, index=True)
    description = Column(Text, nullable=True)

    uid = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)
    deleted_at = Column(DateTime, nullable=True ,index=True)
    is_active = Column(Boolean, default=True, nullable=False)

    user = relationship('User', back_populates='images')
    comments = relationship('Comment', back_populates='image', cascade='all, delete-orphan', lazy='dynamic')
    tags = relationship('Tag', secondary=image_tag_association, back_populates='images', cascade='all, delete', lazy='dynamic')
    collections = relationship('Collection', secondary=image_collection_association, back_populates='images', cascade='all, delete', lazy='dynamic')
    liked_by = relationship('User', secondary=user_liked_image, back_populates='liked_images', cascade='all, delete', lazy='dynamic')
    favorited_by = relationship('User', secondary=user_favorited_image, back_populates='favorited_images', cascade='all, delete', lazy='dynamic')

    @property
    def comment_count(self):
        return self.comments.count()

    @property
    def tag_count(self):
        return self.tags.count()

    @property
    def collection_count(self):
        return self.collections.count()

    @property
    def liked_by_count(self):
        return self.liked_by.count()

    @property
    def favorited_by_count(self):
        return self.favorited_by.count()

class Tag(db.Model, SoftDeleteMixin):
    __tablename__ = 'tags'
    __table_args__ = (
        UniqueConstraint('name', 'is_active', name='uq_name_deleted_at'),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False, index=True)

    uid = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)
    deleted_at = Column(DateTime, nullable=True, index=True)
    is_active = Column(Boolean, default=True, nullable=False)

    user = relationship('User', back_populates='tags')
    images = relationship('Image', secondary=image_tag_association, back_populates='tags', cascade='all, delete', lazy='dynamic')
    ignored_by = relationship('User', secondary=user_ignored_tag, back_populates='ignored_tags', cascade='all, delete', lazy='dynamic')

    @property
    def image_count(self):
        return self.images.count()

    @property
    def ignored_by_count(self):
        return self.ignored_by.count()

class Comment(db.Model, SoftDeleteMixin):
    __tablename__ = 'comments'

    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)

    uid = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    imgid = Column(Integer, ForeignKey('images.id', ondelete='CASCADE'), nullable=False, index=True)
    parent_id = Column(Integer, ForeignKey('comments.id', ondelete='CASCADE'), nullable=True, index=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)
    deleted_at = Column(DateTime, nullable=True, index=True)
    is_active = Column(Boolean, default=True, nullable=False)

    user = relationship('User', back_populates='comments')
    image = relationship('Image', back_populates='comments')
    replies = relationship('Comment', backref=db.backref('parent', remote_side=[id]), cascade='all, delete-orphan', lazy='dynamic')

    @property
    def reply_count(self):
        return len(self.replies)

class Collection(db.Model, SoftDeleteMixin):
    __tablename__ = 'collections'
    __table_args__ = (
        UniqueConstraint('name', 'uid', 'is_active', name='uq_name_uid_deleted_at'),
    )

    id = Column(Integer, primary_key=True)
    name = Column(String(64), nullable=False, index=True)
    description = Column(Text, nullable=True)

    uid = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.now(timezone.utc), nullable=False)
    updated_at = Column(DateTime, default=datetime.now(timezone.utc), onupdate=datetime.now(timezone.utc), nullable=False)
    deleted_at = Column(DateTime, nullable=True, index=True)
    is_active = Column(Boolean, default=True, nullable=False)
    is_default = Column(Boolean, default=False, nullable=False)

    user = relationship('User', back_populates='collections')
    images = relationship('Image', secondary=image_collection_association, back_populates='collections', cascade='all, delete', lazy='dynamic')

    @property
    def image_count(self):
        return self.images.count()
