from flask import Flask, render_template, send_file, abort, request

import io
import os
from datetime import datetime
from PIL import Image, ImageOps
from dotenv import load_dotenv

app = Flask(__name__)
load_dotenv()

BOOKS_DIR = os.getenv('BOOKS_DIR')
THUMBNAIL_SIZE = (200, 200)

def get_sorted_items(path, sort_by='modified_time', order='asc'):
    items = os.listdir(path)
    if sort_by == 'modified_time':
        items.sort(key=lambda x: os.path.getmtime(os.path.join(path, x)), reverse=(order == 'desc'))
    else:  # sort by name
        items.sort(key=lambda x: x.lower(), reverse=(order == 'desc'))
    return items

def get_all_works(sort_by='modified_time', order='desc'):
    all_works = []
    for author in os.listdir(BOOKS_DIR):
        author_path = os.path.join(BOOKS_DIR, author)
        if os.path.isdir(author_path):
            for work in os.listdir(author_path):
                work_path = os.path.join(author_path, work)
                images = get_sorted_items(work_path, sort_by='name')
                cover_image = images[0] if images else None
                all_works.append({
                    'author': author,
                    'name': work,
                    'cover': cover_image,
                    'modified_time': os.path.getmtime(work_path)
                })
    if sort_by == 'name':
        all_works.sort(key=lambda x: x['name'].lower(), reverse=(order == 'desc'))
    else:  # sort by modified time
        all_works.sort(key=lambda x: x['modified_time'], reverse=(order == 'desc'))
    return all_works

def get_all_authors(sort_by='modified_time', order='desc'):
    authors = []
    for author in os.listdir(BOOKS_DIR):
        author_path = os.path.join(BOOKS_DIR, author)
        if os.path.isdir(author_path):
            works = get_sorted_items(author_path)
            works_count = len(works)
            first_work = works[0] if works else None
            cover_image = None
            if first_work:
                work_path = os.path.join(author_path, first_work)
                images = get_sorted_items(work_path, sort_by='name')
                cover_image = images[0] if images else None
            authors.append({
                'name': author,
                'cover': cover_image,
                'first_work': first_work,
                'works_count': works_count,
                'modified_time': os.path.getmtime(author_path)
            })
    if sort_by == 'name':
        authors.sort(key=lambda x: x['name'].lower(), reverse=(order == 'desc'))
    else:  # sort by modified time
        authors.sort(key=lambda x: x['modified_time'], reverse=(order == 'desc'))
    return authors

def search_works(query, sort_by='modified_time', order='desc'):
    results = []
    for author in os.listdir(BOOKS_DIR):
        author_path = os.path.join(BOOKS_DIR, author)
        if os.path.isdir(author_path):
            if query.lower() in author.lower():
                works = get_sorted_items(author_path)
                for work in works:
                    work_path = os.path.join(author_path, work)
                    images = get_sorted_items(work_path, sort_by='name')
                    cover_image = images[0] if images else None
                    results.append((author, work, cover_image, os.path.getmtime(work_path)))
            else:
                for work in os.listdir(author_path):
                    if query.lower() in work.lower():
                        work_path = os.path.join(author_path, work)
                        images = get_sorted_items(work_path, sort_by='name')
                        cover_image = images[0] if images else None
                        results.append((author, work, cover_image, os.path.getmtime(work_path)))
    
    # Sort the results
    if sort_by == 'name':
        results.sort(key=lambda x: x[1].lower(), reverse=(order == 'desc'))
    else:  # sort by modified time
        results.sort(key=lambda x: x[3], reverse=(order == 'desc'))
    
    return results

@app.route('/')
def index():
    view_type = request.args.get('view', 'works')
    sort_by = request.args.get('sort_by', 'modified_time')
    order = request.args.get('order', 'desc')
    
    if view_type == 'authors':
        items = get_all_authors(sort_by, order)
    else:
        items = get_all_works(sort_by, order)
    
    return render_template('index.html', items=items, view_type=view_type, sort_by=sort_by, order=order)

@app.route('/author/<author_name>')
def author_works(author_name):
    author_path = os.path.join(BOOKS_DIR, author_name)
    sort_by = request.args.get('sort_by', 'modified_time')
    order = request.args.get('order', 'desc')
    works = get_sorted_items(author_path, sort_by, order)
    works_with_covers = []
    for work in works:
        work_path = os.path.join(author_path, work)
        images = get_sorted_items(work_path, sort_by='name')
        cover_image = images[0] if images else None
        works_with_covers.append({
            'name': work,
            'cover': cover_image,
            'modified_time': os.path.getmtime(work_path)
        })
    return render_template('author.html', author=author_name, works=works_with_covers, sort_by=sort_by, order=order)

@app.route('/work/<author_name>/<work_name>')
def work_images(author_name, work_name):
    work_path = os.path.join(BOOKS_DIR, author_name, work_name)
    images = get_sorted_items(work_path, sort_by='name')
    
    # Get additional work information
    last_modified = datetime.fromtimestamp(os.path.getmtime(work_path)).strftime('%Y-%m-%d %H:%M:%S')
    page_count = len(images)
    
    return render_template('work.html', 
                           author=author_name, 
                           work=work_name, 
                           images=images, 
                           last_modified=last_modified, 
                           page_count=page_count)

@app.route('/read/<author_name>/<work_name>')
def read_work(author_name, work_name):
    work_path = os.path.join(BOOKS_DIR, author_name, work_name)
    images = get_sorted_items(work_path, sort_by='name')
    images_per_row = int(request.args.get('images_per_row', 1))
    return render_template('read.html', author=author_name, work=work_name, images=images, images_per_row=images_per_row)

@app.route('/image/<path:image_path>')
def serve_image(image_path):
    full_path = os.path.join(BOOKS_DIR, image_path)
    if os.path.exists(full_path):
        return send_file(full_path)
    else:
        abort(404)

@app.route('/thumbnail/<path:image_path>')
def serve_thumbnail(image_path):
    full_path = os.path.join(BOOKS_DIR, image_path)
    if os.path.exists(full_path):
        img = Image.open(full_path)
        img.thumbnail(THUMBNAIL_SIZE)
        thumb = ImageOps.fit(img, THUMBNAIL_SIZE, Image.LANCZOS)
        img_io = io.BytesIO()
        thumb.save(img_io, 'JPEG', quality=85)
        img_io.seek(0)
        return send_file(img_io, mimetype='image/jpeg')
    else:
        abort(404)

@app.route('/search')
def search():
    query = request.args.get('query', '')
    sort_by = request.args.get('sort_by', 'modified_time')
    order = request.args.get('order', 'desc')
    results = search_works(query, sort_by, order)
    return render_template('search.html', query=query, results=results, sort_by=sort_by, order=order)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=80)