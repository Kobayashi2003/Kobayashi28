import click
from flask.cli import with_appcontext
from sqlalchemy import inspect
from api import db
from ..models import MODEL_MAP

@click.command('inspect-db')
@with_appcontext
def inspect_db():
    inspector = inspect(db.engine)
    for model_name, model_class in MODEL_MAP.items():
        columns = inspector.get_columns(model_class.__tablename__)
        foreign_keys = inspector.get_foreign_keys(model_class.__tablename__)

        print(f"Table: {model_class.__tablename__}")
        print("Columns:")
        for column in columns:
            print(f"  - {column['name']} ({column['type']})")
        print("Foreign Keys:")
        for fk in foreign_keys:
            print(f"  - {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")
        print("\n")