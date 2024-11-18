from .base import BaseResourceBlueprint

class StaffResourceBlueprint(BaseResourceBlueprint):
    def __init__(self):
        super().__init__('staff', plural_form='staff')

staff_bp = StaffResourceBlueprint().blueprint