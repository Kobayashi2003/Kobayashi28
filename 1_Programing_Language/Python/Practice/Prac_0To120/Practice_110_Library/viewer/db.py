import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_db():
    db = get_db()

    with current_app.open_resource('./schema.sql') as f:
        db.executescript(f.read().decode('utf8'))


def update_db():
    from viewer.common import LIBRARY_FOLDER, find_all_files
    import os

    db = get_db()
    books_db = db.execute(
        'SELECT * FROM book_info'
    ).fetchall()

    titles_db = [book['title'] for book in books_db]
    titles_lib = os.listdir(LIBRARY_FOLDER)

    books_del = list(set(titles_db) - set(titles_lib))
    for title in books_del:
        db.execute(
            'DELETE FROM book_info WHERE title = ?', (title,)
        )
        db.execute(
            'DELETE FROM page_info WHERE book_title = ?', (title,)
        )

    books_add = list(set(titles_lib) - set(titles_db))
    for title in titles_lib:
        book_pth = os.path.join(LIBRARY_FOLDER, title)
        pages_pth = [(os.path.relpath(page, LIBRARY_FOLDER)).replace('\\', '/') 
                           for page in find_all_files(book_pth)]
        pages_pth.reverse()
        if title in books_add:
            db.execute(
                'INSERT INTO book_info (title, page_count, ctime) VALUES (?, ?, ?)',
                (title, len(pages_pth), os.path.getctime(book_pth))
            )
            db.executemany(
                'INSERT INTO page_info (relpath, book_title) VALUES (?, ?)',
                [(path, title) for path in pages_pth]
            )
        else:
            db.execute(
                'UPDATE book_info SET page_count = ?, ctime = ? WHERE title = ?',
                (len(pages_pth), os.path.getctime(book_pth), title)
            )
            pages_info_db = db.execute(
                'SELECT * FROM page_info WHERE book_title = ?', (title,)
            ).fetchall()
            pages_relpath_db = [page['relpath'] for page in pages_info_db]
            pages_add = list(set(pages_pth) - set(pages_relpath_db))    
            pages_del = list(set(pages_relpath_db) - set(pages_pth))
            db.executemany(
                'INSERT INTO page_info (relpath, book_title) VALUES (?, ?)',
                [(path, title) for path in pages_add]
            )
            db.executemany(
                'DELETE FROM page_info WHERE relpath = ?',
                [(path,) for path in pages_del]
            )
    db.commit()


@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')


@click.command('update-db')
@with_appcontext
def update_db_command():
    """Update the database."""
    update_db()
    click.echo('Updated the database.')


def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(update_db_command)
