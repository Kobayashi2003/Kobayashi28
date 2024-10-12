try:
    from vndb.db import connect_db
    from vndb.search import search_vndb, generate_fields, generate_filters
    from vndb.search import VN_Operactor_And
    from vndb.search import VN_Filter_ID
except ImportError:
    from db import __connect_db as connect_db
    from db import __close_db as close_db
    from search import search_vndb, generate_fields, generate_filters
    from search import VN_Operactor_And
    from search import VN_Filter_ID

import os
import requests
import logging
from functools import partial
from concurrent.futures import ThreadPoolExecutor

logger = logging.getLogger(__name__)
logging.basicConfig(filename='download.log', level=logging.INFO)

def download_image(image_url, path):
    try:
        response = requests.get(image_url, headers={ 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36' }, timeout=10)
        if response.status_code == 200:
            content_image = response.content




def download(id: str, path: str) -> bool:

    logger.info(f"Downloading VN with id {id} to {path}")

    path = os.path.join(path, id)
    if not os.path.exists(path):
        logger.info(f"Creating directory {path}")
        os.makedirs(path)

    conn = connect_db()
    with conn.cursor() as curs:
        curs.execute("SELECT data FROM vn WHERE id = %s", (id,))
        result = curs.fetchone()
        if not result:
            logger.warning(f"VN with id {id} not found in local database")
            fields = generate_fields()
            filter = generate_filters(filters=(VN_Operactor_And() + VN_Filter_ID(id)).get_filters())
            result = search_vndb(fields=fields, filters=filter)
            result = result['results'] if result else []
            if not result:
                logger.error(f"VN with id {id} not found in local database and VNDB API")
                return False
            curs.execute("INSERT INTO vn (id, data) VALUES (%s, %s)", (id, result))
            curs.commit()
            logger.info(f"VN with id {id} added to local database")
        data = result[0]

    images = []

    if 'url' in data['image'] and data['image']['url']:
        images.append(data['image']['url'])
    if 'thunmbnail' in data['image'] and data['image']['thumbnail']:
        images.append(data['image']['thumbnail'])
    for screenshot in data['screenshots']:
        if 'url' in screenshot and screenshot['url']:
            images.append(screenshot['url'])
        if 'thumbnail' in screenshot and screenshot['thumbnail']:
            images.append(screenshot['thumbnail'])
    for va in data['va']:
        if 'character' in va and va['character'] and 'url' in va['character']['image'] and va['character']['image']['url']:
            images.append(va['character']['image']['url'])

    with ThreadPoolExecutor(max_workers=10) as executor:
        for image in images:
            executor.submit(partial(requests.get, image, headers={ 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36' }, timeout=10), path)

    logger.info(f"Images downloaded for VN with id {id}")
    return True


if __name__ == '__main__':
    download('v19073', './')