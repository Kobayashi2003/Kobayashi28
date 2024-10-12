import psycopg2

import click
from flask import current_app, g


def connect_db():
    if 'conn' not in g:
        g.conn = psycopg2.connect(
            user     = current_app.config['PG_USER'],
            password = current_app.config['PG_PASSWORD'],
            database = current_app.config['PG_DB'],
            host     = current_app.config['PG_HOST'],
            port     = current_app.config['PG_PORT']
        )
    return g.conn


def close_db(e=None):
    conn = g.pop('conn', None)
    if conn:
        conn.close()


def init_db():
    conn = connect_db()
    with conn.cursor() as curs:
        with current_app.open_resource('schema.sql') as f:
            curs.execute(f.read().decode('utf8'))
    conn.commit()


@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Initialized the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
