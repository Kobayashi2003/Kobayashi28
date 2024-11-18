from .base import BaseResourceBlueprint

class TraitResourceBlueprint(BaseResourceBlueprint):
    def __init__(self):
        super().__init__('trait')

trait_bp = TraitResourceBlueprint().blueprint