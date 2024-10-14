import os

from flask import Flask  

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY  = 'dev',
        STATIC_FOLDER = 'vndb/static',
        PG_USER     = 'postgres',
        PG_PASSWORD = 'root',
        PG_DB       = 'vndb',
        PG_HOST     = 'localhost',
        PG_PORT     = '5432'
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/test', methods=('GET', 'POST'))
    def test():
        from flask import request, render_template
        if request.method == 'POST':
            return render_template('test.html', test='success')
        return render_template('test.html', test='test')

    from . import db
    db.init_app(app)

    from . import vn
    app.register_blueprint(vn.vn_bp)

    from . import index
    app.register_blueprint(index.index_bp)

    from . import search
    app.register_blueprint(search.search_bp)
    app.add_url_rule('/search', endpoint='search', view_func=search.search, methods=['GET'])

    from . import download
    app.register_blueprint(download.download_bp)
    app.add_url_rule('/download', endpoint='download', view_func=download.download, methods=['GET'])

    return app