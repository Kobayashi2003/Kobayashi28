from .base import BaseResourceBlueprint

class TagResourceBlueprint(BaseResourceBlueprint):
    def __init__(self):
        super().__init__('tag')

tag_bp = TagResourceBlueprint().blueprint