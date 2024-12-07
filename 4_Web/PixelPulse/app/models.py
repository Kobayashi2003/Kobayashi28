from app import db
from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from datetime import timezone
from werkzeug.security import generate_password_hash, check_password_hash

class UserFollow(db.Model):
    __tablename__ = 'user_follow'
    follower_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    followed_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

class ImageTagAssociation(db.Model):
    __tablename__ = 'image_tag_association'
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True)
    image_id = Column(Integer, ForeignKey('images.id'), primary_key=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    tag = relationship('Tag', back_populates='tagged_images')
    image = relationship('Image', back_populates='image_tags')

class UserTagIgnore(db.Model):
    __tablename__ = 'user_tag_ignore'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    tag_id = Column(Integer, ForeignKey('tags.id'), primary_key=True)
    ignored_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))

    user = relationship('User', back_populates='ignored_tags')
    tag = relationship('Tag', back_populates='ignored_by_users')

class UserImagePublish(db.Model):
    __tablename__ = 'user_image_publish'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    image_id = Column(Integer, ForeignKey('images.id'), primary_key=True)
    publish_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    user = relationship('User', back_populates='published_images')
    image = relationship('Image', back_populates='published_by')

class UserImageLike(db.Model):
    __tablename__ = 'user_image_like'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    image_id = Column(Integer, ForeignKey('images.id'), primary_key=True)
    like_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    user = relationship('User', back_populates='liked_images')
    image = relationship('Image', back_populates='liked_by')

class UserImageCollection(db.Model):
    __tablename__ = 'user_image_collection'
    user_id = Column(Integer, ForeignKey('users.id'), primary_key=True)
    image_id = Column(Integer, ForeignKey('images.id'), primary_key=True)
    collection_id = Column(Integer, ForeignKey('collections.id'), primary_key=True)
    collect_date = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    user = relationship('User', back_populates='collected_images')
    image = relationship('Image', back_populates='collected_by')
    collection = relationship('Collection', back_populates='images_in_collection')

class User(db.Model):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    username = Column(String(80), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=False)
    password_hash = Column(String(128))
    bio = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    
    published_images = relationship('UserImagePublish', back_populates='user')
    liked_images = relationship('UserImageLike', back_populates='user')
    collected_images = relationship('UserImageCollection', back_populates='user')
    owned_collections = relationship('Collection', back_populates='owner', lazy='dynamic')
    created_tags = relationship('Tag', back_populates='creator', lazy='dynamic')
    
    ignored_tags = relationship('UserTagIgnore', back_populates='user')
    comments = relationship('Comment', back_populates='author', lazy='dynamic')

    followers = relationship('UserFollow',
                             foreign_keys=[UserFollow.followed_id],
                             backref=db.backref('followed', lazy='joined'),
                             lazy='dynamic',
                             cascade='all, delete-orphan')
    following = relationship('UserFollow',
                             foreign_keys=[UserFollow.follower_id],
                             backref=db.backref('follower', lazy='joined'),
                             lazy='dynamic',
                             cascade='all, delete-orphan')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Image(db.Model):
    __tablename__ = 'images'
    id = Column(Integer, primary_key=True)
    title = Column(String(100))
    description = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    like_count = Column(Integer, default=0)
    collection_count = Column(Integer, default=0)
    
    published_by = relationship('UserImagePublish', back_populates='image')
    liked_by = relationship('UserImageLike', back_populates='image')
    collected_by = relationship('UserImageCollection', back_populates='image')
    
    image_tags = relationship('ImageTagAssociation', back_populates='image')
    comments = relationship('Comment', back_populates='image', lazy='dynamic')
    comment_count = Column(Integer, default=0)

class Tag(db.Model):
    __tablename__ = 'tags'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True, nullable=False)
    creator_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    image_count = Column(Integer, default=0)

    creator = relationship('User', back_populates='created_tags')
    tagged_images = relationship('ImageTagAssociation', back_populates='tag')
    ignored_by_users = relationship('UserTagIgnore', back_populates='tag')

    @property
    def update_image_count(self):
        self.image_count = len(self.tagged_images)
        db.session.commit()
        return self.image_count

class Collection(db.Model):
    __tablename__ = 'collections'
    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    description = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    is_default = Column(Boolean, default=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    
    owner = relationship('User', back_populates='owned_collections')
    images_in_collection = relationship('UserImageCollection', back_populates='collection')

    @classmethod
    def create_default_collection(cls, user):
        default_collection = cls(
            name="Default Collection",
            description="Your default collection",
            is_default=True,
            owner=user
        )
        db.session.add(default_collection)
        db.session.commit()
        return default_collection

class Comment(db.Model):
    __tablename__ = 'comments'
    id = Column(Integer, primary_key=True)
    content = Column(Text, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), onupdate=lambda: datetime.now(timezone.utc))
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    image_id = Column(Integer, ForeignKey('images.id'), nullable=False)

    author = relationship('User', back_populates='comments')
    image = relationship('Image', back_populates='comments')