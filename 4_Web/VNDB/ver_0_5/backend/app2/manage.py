from flask.cli import FlaskGroup
from imgserve import create_app

app = create_app()
cli = FlaskGroup(create_app=lambda: app)

if __name__ == "__main__":
    cli()
