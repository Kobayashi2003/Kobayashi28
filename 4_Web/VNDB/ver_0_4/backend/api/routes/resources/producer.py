from .base import BaseResourceBlueprint

class ProducerResourceBlueprint(BaseResourceBlueprint):
    def __init__(self):
        super().__init__('producer')

producer_bp = ProducerResourceBlueprint().blueprint