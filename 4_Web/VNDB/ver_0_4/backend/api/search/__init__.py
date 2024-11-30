from .local.search import (
    search as search_local,
    search_resources_by_vnid as search_resources_by_vnid_local,
    search_resources_by_charid as search_resources_by_charid_local,
    search_vns_by_resource_id as search_vns_by_resource_id_local,
    search_characters_by_resource_id as search_characters_by_resource_id_local,
)

from .remote.search import (
    search_cache as search_remote,
    search_resources_by_vnid_paginated as search_resources_by_vnid_remote,
    search_resources_by_charid_paginated as search_resources_by_charid_remote,
    search_vns_by_resource_id_cache as search_vns_by_resource_id_remote,
    search_characters_by_resource_id_cache as search_characters_by_resource_id_remote, 
)