from flask_caching import Cache

cache = Cache(config={'CACHE_TYPE': 'simple'})

def init_cache(app):
    cache.init_app(app)