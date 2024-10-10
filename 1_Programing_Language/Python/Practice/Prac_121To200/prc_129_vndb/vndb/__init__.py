import os

from flask import Flask  

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY  = 'dev',
        PG_USER     = 'postgres',
        PG_PASSWORD = 'root',
        PG_DB       = 'flask_db',
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

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Yep, I am KOBAYASHI.'

    @app.route('/test', methods=('GET', 'POST'))
    def test():
        from flask import request, render_template
        if request.method == 'POST':
            return render_template('test.html', test='success')
        return render_template('test.html', test='test')

    from . import db
    db.init_app(app)

    from . import pages
    app.register_blueprint(pages.vn_bp)
    app.add_url_rule('/', endpoint='vn.index', methods=['GET', 'POST'])
    app.add_url_rule('/<id>', endpoint='vn.show', methods=['GET', 'POST'])

    return app