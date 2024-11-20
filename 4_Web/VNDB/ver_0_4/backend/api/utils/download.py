from typing import Dict, List 

import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

from .convert import convert_imgurl_to_imgid

def download_images(urls: List[str], path: str) -> Dict[str, bool]:
    """
    Download multiple images concurrently.
    
    Args:
        urls (List[str]): List of image URLs to download.
        path (str): Directory path to save the downloaded images.
    
    Returns:
        Dict[str, bool]: A dictionary mapping each URL to a boolean indicating download success or failure.
    """
    os.makedirs(path, exist_ok=True)
    download_status = {}

    with ThreadPoolExecutor(max_workers=10) as executor:
        future_to_url = {executor.submit(download_image, url, path): url for url in urls}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                success = future.result()
                download_status[url] = success 
            except Exception as exc:
                download_status[url] = False
    
    return download_status

def download_image(url: str, path: str) -> bool:
    """
    Download a single image from a given URL.
    
    Args:
        url (str): The URL of the image to download.
        path (str): Directory path to save the downloaded image.
    
    Returns:
        bool: True if the download was successful, False otherwise.
    """
    try:
        response = requests.get(url, stream=True, timeout=30)
        response.raise_for_status()

        filename = f'{convert_imgurl_to_imgid(url)}.jpg'
        if not filename:
            filename = 'image.jpg'

        local_path = os.path.join(path, filename)

        with open(local_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        return True

    except requests.RequestException as e:
        return False