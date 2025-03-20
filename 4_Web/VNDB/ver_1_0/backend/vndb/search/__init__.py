from .local.search import (
    search as search_local,
    search_resources_by_vnid as search_resources_by_vnid_local,
    search_resources_by_charid as search_resources_by_charid_local,
    search_resources_by_release_id as search_resources_by_release_id_local,
    search_vns_by_resource_id as search_vns_by_resource_id_local,
    search_characters_by_resource_id as search_characters_by_resource_id_local,
    search_releases_by_resource_id as search_releases_by_resource_id_local
)

from .remote.search import (
    search_cache as search_remote,
    search_resources_by_vnid_paginated as search_resources_by_vnid_remote,
    search_resources_by_charid_paginated as search_resources_by_charid_remote,
    search_resources_by_release_id_paginated as search_resources_by_release_id_remote,
    search_vns_by_resource_id_cache as search_vns_by_resource_id_remote,
    search_characters_by_resource_id_cache as search_characters_by_resource_id_remote, 
    search_releases_by_resource_id_cache as search_releases_by_resource_id_remote,
)

from .common import (
    convert_remote_to_local
)