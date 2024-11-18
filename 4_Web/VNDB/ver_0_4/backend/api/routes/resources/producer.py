from .base import BaseResourceBlueprint

class ProducerResourceBlueprint(BaseResourceBlueprint):
    def __init__(self):
        super().__init__('producer')