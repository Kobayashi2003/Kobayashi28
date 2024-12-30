from .init import init_db
from .forge import forge_db
from .clean import clean_db
from .drop import drop_db
from .inspect import inspect_db
from .makemigration import makemigrations
from .migrate import migrate_db
from .downgrade import downgrade_db

def register_commands(app):
    app.cli.add_command(init_db)
    app.cli.add_command(forge_db)
    app.cli.add_command(clean_db)
    app.cli.add_command(drop_db)
    app.cli.add_command(inspect_db)
    app.cli.add_command(makemigrations)
    app.cli.add_command(migrate_db)
    app.cli.add_command(downgrade_db)
