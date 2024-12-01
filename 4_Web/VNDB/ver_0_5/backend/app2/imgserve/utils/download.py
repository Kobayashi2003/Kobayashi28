from typing import Optional

import httpx
from io import BytesIO

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