import os
import time

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from viewer.user import login_required
from viewer.db import get_db

from viewer.common import LIBRARY_FOLDER

bp = Blueprint('library', __name__, static_folder=LIBRARY_FOLDER)


@bp.route('/', methods=('GET', 'POST'))
@login_required
def index():

    db = get_db()
    
    if request.method == 'POST':
        title = request.form['title']
        if not title:
            books = db.execute(
                'SELECT * FROM book_info'
            ).fetchall()
        else:
            books = db.execute(
                'SELECT * FROM book_info WHERE title LIKE ?', ('%'+title+'%',)
            ).fetchall()
    else:
        books = db.execute(
            'SELECT * FROM book_info'
        ).fetchall()

    books = [dict(book) for book in books]
    for book in books:
        pages_info = db.execute(
            'SELECT * FROM page_info WHERE book_title = ?', (book['title'],)
        ).fetchall()
        book['ctime'] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(float(book['ctime'])))
        book['cover'] = pages_info[0]['relpath']
    return render_template('library/index.html', books=books)


def get_book(book_title):
    book_info = get_db().execute(
        'SELECT * FROM book_info WHERE title = ?', (book_title,)
    ).fetchone()

    if book_info is None:
        abort(404, "Book id {0} doesn't exist.".format(book_title))

    pages_info = get_db().execute(
        'SELECT * FROM page_info WHERE book_title = ?', (book_title,)
    ).fetchall()

    pages_relpath = [page['relpath'] for page in pages_info]

    book = {
        'title': book_info['title'],
        'page_count': book_info['page_count'],
        'ctime': book_info['ctime'],
        'pages_relpath': pages_relpath,
    }

    return book


@bp.route('/<book_title>')
@login_required
def book(book_title):
    book = get_book(book_title)
    return render_template('library/book.html', book=book)
