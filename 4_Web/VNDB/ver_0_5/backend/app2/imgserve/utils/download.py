from typing import Optional, List, Dict

import httpx
import re
import os
from io import BytesIO
from concurrent.futures import ThreadPoolExecutor, as_completed

def download_image(type: str, id: int) -> Optional[BytesIO]:

    if id < 1:
        raise ValueError("Invalid ID")

    dir = str(id).zfill(2)[-2:]
    url = f"https://t.vndb.org/{type}/{dir}/{id}.jpg"

    try:
        response = httpx.get(url, timeout=10.0, follow_redirects=True)
        response.raise_for_status()
        image_data = BytesIO(response.content)
        image_data.seek(0)
        return image_data
    except (httpx.RequestError, httpx.HTTPStatusError):
        return None

def download_and_save_image(url: str, folder: str) -> bool:
    url_pattern = r"https://t\.vndb\.org/(?P<type>(?:sf|sf\.t|ch|cv|cv\.t))/(?P<dir>\d{2})/(?P<id>\d*?(?P=dir)|\d)\.jpg"
    match = re.match(url_pattern, url)
    if not match:
        return False
    type = match.group('type')
    dir = match.group('dir')
    id = int(match.group('id'))

    try:
        image_path = os.path.join(folder, type, dir, f"{id}.jpg")
        if os.path.exists(image_path):
            return True
        os.makedirs(os.path.dirname(image_path), exist_ok=True)

        image_data = download_image(type, id)
        if image_data is None:
            return False

        with open(image_path, 'wb') as f:
            f.write(image_data.getvalue())
        return True
    except Exception as exc:
        print(f"Error downloading image {url}: {exc}")
        return False

def download_images(urls: List[str], folder: str) -> Dict[str, bool]:
    download_status = {}

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(download_and_save_image, url, folder): url for url in urls}
        
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                success = future.result()
                download_status[url] = success
            except Exception as exc:
                download_status[url] = False
    
    return download_status