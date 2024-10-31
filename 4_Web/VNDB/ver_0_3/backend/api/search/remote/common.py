from api.search.remote.search import VNDBAPIWrapper
from api.search.remote.fields import VNDBFields
from api.search.remote.filters import VNDBFilters

from typing import List

SMALL_FIELDS_VN: List[str] = [
    VNDBFields.VN.ID,
    VNDBFields.VN.TITLE,
    VNDBFields.VN.RELEASED,
    VNDBFields.VN.IMAGE.THUMBNAIL,
    VNDBFields.VN.IMAGE.SEXUAL,
    VNDBFields.VN.IMAGE.VIOLENCE
]

FIELDS_VN: List[str] = VNDBFields.VN.ALL
FIELDS_CHARACTER: List[str] = VNDBFields.Character.ALL
FIELDS_TAG: List[str] = VNDBFields.Tag.ALL
FIELDS_PRODUCER: List[str] = VNDBFields.Producer.ALL
FIELDS_STAFF: List[str] = VNDBFields.Staff.ALL
FIELDS_TRAIT: List[str] = VNDBFields.Trait.ALL

api = VNDBAPIWrapper()

