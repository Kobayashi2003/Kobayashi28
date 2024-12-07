from sqlalchemy import inspect
from app import create_app, db
from app.models import User, Image, Tag, Collection, Comment

app = create_app()

def describe_table(table):
    inspector = inspect(db.engine)
    columns = inspector.get_columns(table.__tablename__)
    foreign_keys = inspector.get_foreign_keys(table.__tablename__)
    
    print(f"Table: {table.__tablename__}")
    print("Columns:")
    for column in columns:
        print(f"  - {column['name']} ({column['type']})")
    print("Foreign Keys:")
    for fk in foreign_keys:
        print(f"  - {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")
    print("\n")

for table in [User, Image, Tag, Collection, Comment]:
    with app.app_context():
        describe_table(table)