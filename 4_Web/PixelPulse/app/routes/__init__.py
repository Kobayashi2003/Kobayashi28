from .user_routes import ns as user_ns
from .image_routes import ns as image_ns
from .tag_routes import ns as tag_ns

def register_namespaces(api):
    api.add_namespace(user_ns)
    api.add_namespace(image_ns)
    api.add_namespace(tag_ns)
