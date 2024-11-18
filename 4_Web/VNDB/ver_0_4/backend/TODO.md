- vns/<string:vnid>/vns - GET POST PUT DELETE
- vns/<string:vnid>/vns/<string:vnid2> - GET POST PUT DELETE

- vns/<string:vnid>/characters - GET POST PUT DELETE
- vns/<string:vnid>/characters/<string:charid> - GET POST PUT DELETE

- vns/<string:vnid>/tags - GET POST PUT DELETE
- vns/<string:vnid>/tags/<string:tag_id> - GET POST PUT DELETE

- vns/<string:vnid>/developers - GET POST PUT DELETE
- vns/<string:vnid>/developers/<string:dev_id> - GET POST PUT DELETE

- vns/<string:vnid>/staff - GET POST PUT DELETE
- vns/<string:vnid>/staff/<string:staff_id> - GET POST PUT DELETE

--> vns/<string:vnid>/<resource_type>/<resource_id> - GET POST PUT DELETE

<!-- - vns/<string:vnid>/vas
- vns/<string:vnid>/vas/<string:staff_id> -->

- characters/<string:charid>/vns - GET POST PUT DELETE
- characters/<string:charid>/vns/<string:vnid> - GET POST PUT DELETE

- characters/<string:charid>/traits - GET POST PUT DELETE
- characters/<string:charid>/vns/<string:trait_id> - GET POST PUT DELETE

--> characters/<string:charid>/<string:resource_type>/<resource_id> - GET POST PUT DELETE

```py
from sqlalchemy import Table, Column, String, ForeignKey, DateTime, func
from api import db

# Association tables for many-to-many relationships

vn_vn = Table('vn_vn', db.Model.metadata,
    Column('vn_id', String(255), ForeignKey('vn.id'), primary_key=True),
    Column('related_vn_id', String(255), ForeignKey('vn.id'), primary_key=True),
    Column('relationship_type', String(50)),
    Column('created_at', DateTime, default=func.now()),
    Column('updated_at', DateTime, default=func.now(), onupdate=func.now())
)

vn_character = Table('vn_character', db.Model.metadata,
    Column('vn_id', String(255), ForeignKey('vn.id'), primary_key=True),
    Column('character_id', String(255), ForeignKey('character.id'), primary_key=True),
    Column('role', String(50)),
    Column('created_at', DateTime, default=func.now()),
    Column('updated_at', DateTime, default=func.now(), onupdate=func.now())
)

vn_tag = Table('vn_tag', db.Model.metadata,
    Column('vn_id', String(255), ForeignKey('vn.id'), primary_key=True),
    Column('tag_id', String(255), ForeignKey('tag.id'), primary_key=True),
    Column('created_at', DateTime, default=func.now()),
    Column('updated_at', DateTime, default=func.now(), onupdate=func.now())
)

vn_developer = Table('vn_developer', db.Model.metadata,
    Column('vn_id', String(255), ForeignKey('vn.id'), primary_key=True),
    Column('developer_id', String(255), ForeignKey('producer.id'), primary_key=True),
    Column('role', String(50)),
    Column('created_at', DateTime, default=func.now()),
    Column('updated_at', DateTime, default=func.now(), onupdate=func.now())
)

vn_staff = Table('vn_staff', db.Model.metadata,
    Column('vn_id', String(255), ForeignKey('vn.id'), primary_key=True),
    Column('staff_id', String(255), ForeignKey('staff.id'), primary_key=True),
    Column('role', String(50)),
    Column('created_at', DateTime, default=func.now()),
    Column('updated_at', DateTime, default=func.now(), onupdate=func.now())
)

character_trait = Table('character_trait', db.Model.metadata,
    Column('character_id', String(255), ForeignKey('character.id'), primary_key=True),
    Column('trait_id', String(255), ForeignKey('trait.id'), primary_key=True),
    Column('created_at', DateTime, default=func.now()),
    Column('updated_at', DateTime, default=func.now(), onupdate=func.now())
)

# Update existing models to include relationships

class VN(db.Model):
    # ... (existing fields)

    related_vns = db.relationship('VN', secondary=vn_vn,
                                  primaryjoin=(id == vn_vn.c.vn_id),
                                  secondaryjoin=(id == vn_vn.c.related_vn_id),
                                  backref=db.backref('related_to', lazy='dynamic'),
                                  lazy='dynamic')
    characters = db.relationship('Character', secondary=vn_character, back_populates='vns')
    tags = db.relationship('Tag', secondary=vn_tag, back_populates='vns')
    developers = db.relationship('Producer', secondary=vn_developer, back_populates='developed_vns')
    staff_members = db.relationship('Staff', secondary=vn_staff, back_populates='vns')

class Character(db.Model):
    # ... (existing fields)

    vns = db.relationship('VN', secondary=vn_character, back_populates='characters')
    traits = db.relationship('Trait', secondary=character_trait, back_populates='characters')

class Tag(db.Model):
    # ... (existing fields)

    vns = db.relationship('VN', secondary=vn_tag, back_populates='tags')

class Producer(db.Model):
    # ... (existing fields)

    developed_vns = db.relationship('VN', secondary=vn_developer, back_populates='developers')

class Staff(db.Model):
    # ... (existing fields)

    vns = db.relationship('VN', secondary=vn_staff, back_populates='staff_members')

class Trait(db.Model):
    # ... (existing fields)

    characters = db.relationship('Character', secondary=character_trait, back_populates='traits')
```