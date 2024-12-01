from enum import Enum, auto
from typing import Optional

class FilterOperator(Enum):
    EQUAL = "="
    NOT_EQUAL = "!="
    GREATER_THAN = ">"
    GREATER_THAN_EQUAL = ">="
    LESS_THAN = "<"
    LESS_THAN_EQUAL = "<="

class FilterType(Enum):
    STRING = auto()
    INTEGER = auto()
    FLOAT = auto()
    BOOLEAN = auto()
    DATE = auto()
    VNDBID = auto()
    ARRAY = auto()
    NESTED = auto()

class VNDBFilter:
    def __init__(self, name: str, filter_type: FilterType, flags: str = "", associated_domain: Optional[str] = None):
        self.name = name
        self.filter_type = filter_type
        self.flags = flags
        self.associated_domain = associated_domain

class VNDBFilters:
    VN = {
        "id": VNDBFilter("id", FilterType.VNDBID, "o"),
        "search": VNDBFilter("search", FilterType.STRING, "m"),
        "lang": VNDBFilter("lang", FilterType.STRING, "m"),
        "olang": VNDBFilter("olang", FilterType.STRING),
        "platform": VNDBFilter("platform", FilterType.STRING, "m"),
        "length": VNDBFilter("length", FilterType.INTEGER, "o"),
        "released": VNDBFilter("released", FilterType.DATE, "o,n"),
        "rating": VNDBFilter("rating", FilterType.FLOAT, "o,i"),
        "votecount": VNDBFilter("votecount", FilterType.INTEGER, "o"),
        "has_description": VNDBFilter("has_description", FilterType.BOOLEAN),
        "has_anime": VNDBFilter("has_anime", FilterType.BOOLEAN),
        "has_screenshot": VNDBFilter("has_screenshot", FilterType.BOOLEAN),
        "has_review": VNDBFilter("has_review", FilterType.BOOLEAN),
        "devstatus": VNDBFilter("devstatus", FilterType.INTEGER),
        "tag": VNDBFilter("tag", FilterType.ARRAY, "m"),
        "dtag": VNDBFilter("dtag", FilterType.ARRAY, "m"),
        "anime_id": VNDBFilter("anime_id", FilterType.INTEGER),
        "label": VNDBFilter("label", FilterType.ARRAY, "m"),
        "release": VNDBFilter("release", FilterType.NESTED, "m"),
        "character": VNDBFilter("character", FilterType.NESTED, "m", associated_domain="CHARACTER"),
        "staff": VNDBFilter("staff", FilterType.NESTED, "m", associated_domain="STAFF"),
        "developer": VNDBFilter("developer", FilterType.NESTED, "m", associated_domain="PRODUCER"),
    }

    CHARACTER = {
        "id": VNDBFilter("id", FilterType.VNDBID, "o"),
        "search": VNDBFilter("search", FilterType.STRING, "m"),
        "role": VNDBFilter("role", FilterType.STRING, "m"),
        "blood_type": VNDBFilter("blood_type", FilterType.STRING),
        "sex": VNDBFilter("sex", FilterType.STRING),
        "height": VNDBFilter("height", FilterType.INTEGER, "o,n,i"),
        "weight": VNDBFilter("weight", FilterType.INTEGER, "o,n,i"),
        "bust": VNDBFilter("bust", FilterType.INTEGER, "o,n,i"),
        "waist": VNDBFilter("waist", FilterType.INTEGER, "o,n,i"),
        "hips": VNDBFilter("hips", FilterType.INTEGER, "o,n,i"),
        "cup": VNDBFilter("cup", FilterType.STRING, "o,n,i"),
        "age": VNDBFilter("age", FilterType.INTEGER, "o,n,i"),
        "trait": VNDBFilter("trait", FilterType.ARRAY, "m"),
        "dtrait": VNDBFilter("dtrait", FilterType.ARRAY, "m"),
        "birthday": VNDBFilter("birthday", FilterType.ARRAY, "n"),
        "seiyuu": VNDBFilter("seiyuu", FilterType.NESTED, "m", associated_domain="STAFF"),
        "vn": VNDBFilter("vn", FilterType.NESTED, "m", associated_domain="VN"),
    }

    PRODUCER = {
        "id": VNDBFilter("id", FilterType.VNDBID, "o"),
        "search": VNDBFilter("search", FilterType.STRING, "m"),
        "lang": VNDBFilter("lang", FilterType.STRING),
        "type": VNDBFilter("type", FilterType.STRING),
    }

    STAFF = {
        "id": VNDBFilter("id", FilterType.VNDBID, "o"),
        "aid": VNDBFilter("aid", FilterType.INTEGER),
        "search": VNDBFilter("search", FilterType.STRING, "m"),
        "lang": VNDBFilter("lang", FilterType.STRING),
        "gender": VNDBFilter("gender", FilterType.STRING),
        "role": VNDBFilter("role", FilterType.STRING, "m"),
        "extlink": VNDBFilter("extlink", FilterType.STRING, "m"),
        "ismain": VNDBFilter("ismain", FilterType.BOOLEAN),
    }

    TAG = {
        "id": VNDBFilter("id", FilterType.VNDBID, "o"),
        "search": VNDBFilter("search", FilterType.STRING, "m"),
        "category": VNDBFilter("category", FilterType.STRING),
    }

    TRAIT = {
        "id": VNDBFilter("id", FilterType.VNDBID, "o"),
        "search": VNDBFilter("search", FilterType.STRING, "m"),
    }

    RELEASE = {
        "id": VNDBFilter("id", FilterType.VNDBID, "o"),
        "search": VNDBFilter("search", FilterType.STRING, "m"),
        "lang": VNDBFilter("lang", FilterType.STRING, "m"),
        "platform": VNDBFilter("platform", FilterType.STRING, "m"),
        "released": VNDBFilter("released", FilterType.DATE, "o"),
        "resolution": VNDBFilter("resolution", FilterType.ARRAY, "o,i"),
        "resolution_aspect": VNDBFilter("resolution_aspect", FilterType.ARRAY, "o,i"),
        "minage": VNDBFilter("minage", FilterType.INTEGER, "o,n,i"),
        "medium": VNDBFilter("medium", FilterType.STRING, "m,n"),
        "voiced": VNDBFilter("voiced", FilterType.INTEGER, "n"),
        "engine": VNDBFilter("engine", FilterType.STRING, "n"),
        "rtype": VNDBFilter("rtype", FilterType.STRING, "m"),
        "extlink": VNDBFilter("extlink", FilterType.STRING, "m"),
        "patch": VNDBFilter("patch", FilterType.BOOLEAN),
        "freeware": VNDBFilter("freeware", FilterType.BOOLEAN),
        "uncensored": VNDBFilter("uncensored", FilterType.BOOLEAN, "i"),
        "official": VNDBFilter("official", FilterType.BOOLEAN),
        "has_ero": VNDBFilter("has_ero", FilterType.BOOLEAN),
        "vn": VNDBFilter("vn", FilterType.NESTED, "m", associated_domain="VN"),
        "producer": VNDBFilter("producer", FilterType.NESTED, "m", associated_domain="PRODUCER"),
    }