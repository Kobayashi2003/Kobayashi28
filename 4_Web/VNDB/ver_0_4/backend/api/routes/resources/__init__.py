from .vn import VNResourceBlueprint
from .character import CharacterResourceBlueprint
from .producer import ProducerResourceBlueprint
from .staff import StaffResourceBlueprint
from .tag import TagResourceBlueprint
from .trait import TraitResourceBlueprint

vn_bp = VNResourceBlueprint().blueprint
character_bp = CharacterResourceBlueprint().blueprint
producer_bp = ProducerResourceBlueprint().blueprint
staff_bp = StaffResourceBlueprint().blueprint
tag_bp = TagResourceBlueprint().blueprint
trait_bp = TraitResourceBlueprint().blueprint