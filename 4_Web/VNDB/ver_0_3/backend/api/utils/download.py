from typing import Dict, List, Union

import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed

from .convert import convert_imgurl_to_imgid
from api.database.models import VN, Character

def extract_images(type: str, data: Union[VN, Character]) -> List[Dict[str, str]]:
    """
    Extract image URLs and their types from VN or Character data.
    
    Args:
        type (str): The type of data ('vn' or 'character').
        data (Union[VN, Character]): The VN or Character object to extract images from.
    
    Returns:
        List[Dict[str, str]]: A list of dictionaries, each containing a URL and its image type.
    
    Raises:
        ValueError: If an invalid type is provided.
    """
    if type == 'vn':
        urls = extract_images_vn(data)
    elif type == 'character':
        urls = extract_images_character(data)
    else:
        raise ValueError(f"Invalid type: {type}. Expected 'vn' or 'character'.")
    
    return urls

def extract_images_vn(vn: VN) -> List[Dict[str, str]]:
    """
    Extract image URLs and their types from a VN object.
    
    Args:
        vn (VN): The VN object to extract images from.
    
    Returns:
        List[Dict[str, str]]: A list of dictionaries, each containing a URL and its image type.
    """
    urls = []

    if vn.image:
        if 'url' in vn.image:
            urls.append({vn.image['url']: 'cv'})
        if 'thumbnail' in vn.image:
            urls.append({vn.image['thumbnail']: 'cv.t'})

    if vn.screenshots:
        for screenshot in vn.screenshots:
            if 'url' in screenshot:
                urls.append({screenshot['url']: 'sf'})
            if 'thumbnail' in screenshot:
                urls.append({screenshot['thumbnail']: 'sf.t'})
    
    return urls

def extract_images_character(character: Character) -> List[Dict[str, str]]:
    """
    Extract image URL and its type from a Character object.
    
    Args:
        character (Character): The Character object to extract image from.
    
    Returns:
        List[Dict[str, str]]: A list containing a dictionary with the URL and its image type, or an empty list if no image is found.
    """
    if character.image and 'url' in character.image:
        return [{character.image['url']: 'ch'}]
    
    return []
    
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