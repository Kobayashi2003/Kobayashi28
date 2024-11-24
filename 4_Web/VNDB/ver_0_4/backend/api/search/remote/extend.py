from typing import Dict, List, Any
from .common import get_remote_fields

import requests

def search_by_vnid(vnid: str, fields: List[str]) -> Dict[str, Any]:
    url = "https://api.vndb.org/kana/vn"

    payload = {
        "filters": ["id", "=", vnid],
        "fields": ",".join(fields),
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()["results"][0]

def search_by_charid(charid: str, fields: List[str]) -> Dict[str, Any]:
    url = "https://api.vndb.org/kana/character"

    payload = {
        "filters": ["id", "=", charid],
        "fields": ",".join(fields),
    }
    response = requests.post(url, json=payload)
    response.raise_for_status()
    return response.json()["results"][0]

def search_relations_by_vnid(vnid: str, response_size: str = "small") -> Dict[str, Any]:
    vn_fields = get_remote_fields("vn", response_size)
    vn_fields = [f"relations.{field}" for field in vn_fields]
    vn_fields.extend(["relations.relation", "relations.relation_official"])
    results = search_by_vnid(vnid, vn_fields)
    relations = results["relations"]
    return { "results": relations, "count": len(relations) }
        
def search_tags_by_vnid(vnid: str, response_size: str = "small") -> Dict[str, Any]:
    tag_fields = get_remote_fields("tag", response_size)
    tag_fields = [f"tags.{field}" for field in tag_fields]
    tag_fields.extend(["tags.rating", "tags.spoiler", "tags.lie"])
    results = search_by_vnid(vnid, tag_fields)
    tags = results["tags"]
    return { "results": tags, "count": len(tags) }

def search_developers_by_vnid(vnid: str, response_size: str = "small") -> Dict[str, Any]:
    producer_fields = get_remote_fields("producer", response_size)
    producer_fields = [f"developers.{field}" for field in producer_fields]
    results = search_by_vnid(vnid, producer_fields)
    developers =  results["developers"]
    return { "results": developers, "count": len(developers) }

def search_staff_by_vnid(vnid: str, response_size: str = "small") -> Dict[str, Any]:
    staff_fields = get_remote_fields("staff", response_size)
    staff_fields = [f"staff.{field}" for field in staff_fields]
    staff_fields.extend(["staff.eid", "staff.role"])
    results = search_by_vnid(vnid, staff_fields)
    staff = results["staff"]
    return { "results": staff, "count": len(staff) }

def search_characters_by_vnid(vnid: str, response_size: str = "small") -> Dict[str, Any]:
    url = "https://api.vndb.org/kana/character"

    character_fields = get_remote_fields("character", response_size)
    if response_size == 'small':
        character_fields.extend(["vns.id", "vns.role", "vns.spoiler"])

    payload = {
        "filters": ["vn", "=", ["id", "=", vnid]],
        "fields": ",".join(character_fields),
        "results": 100,
        "page": 1,
        "count": True
    }

    more = True
    results = []
    while more:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        response = response.json()
        results.extend(response["results"])
        more = response["more"]
        payload["page"] += 1

    for char in results:
        matching_vn = next((vn for vn in char["vns"] if vn["id"] == vnid), None)
        if matching_vn:
            char["role"] = matching_vn["role"]
            char["spoiler"] = matching_vn["spoiler"]
        if response_size == "small":
            char.pop("vns")

    return {"results": results, "count": len(results)}

def search_vns_by_charid(charid: str, response_size: str = "small") -> Dict[str, Any]:
    vn_fields = get_remote_fields("vn", response_size)
    vn_fields = [f'vns.{field}' for field in vn_fields]
    vn_fields.extend(["vns.role", "vns.spoiler"])
    results = search_by_charid(charid, vn_fields)
    vns = results["vns"]
    return { "results": vns, "count": len(vns) }

def search_traits_by_charid(charid: str, response_size: str = "small") -> Dict[str, Any]:
    trait_fields = get_remote_fields("trait", response_size)
    trait_fields = [f"traits.{field}" for field in trait_fields]
    trait_fields.extend(["traits.spoiler", "traits.lie"])
    results = search_by_charid(charid, trait_fields)
    traits = results["traits"]
    return { "results": traits, "count": len(traits) }

def search_resources_by_vnid(vnid, related_resource_type, response_size = "small") -> Dict[str, Any]:
    if related_resource_type == "vn":
        return search_relations_by_vnid(vnid, response_size)
    if related_resource_type == "tag":
        return search_tags_by_vnid(vnid, response_size)
    if related_resource_type == "producer":
        return search_developers_by_vnid(vnid, response_size)
    if related_resource_type == "staff":
        return search_staff_by_vnid(vnid, response_size)
    if related_resource_type == "character":
        return search_characters_by_vnid(vnid, response_size)
    raise ValueError(f"Invalid resource type: {related_resource_type}")

def search_resources_by_charid(charid, related_resource_type, response_size = "small") -> Dict[str, Any]:
    if related_resource_type == "vn":
        return search_vns_by_charid(charid, response_size)
    if related_resource_type == "trait":
        return search_traits_by_charid(charid, response_size)
    raise ValueError(f"Invalid resource type: {related_resource_type}")