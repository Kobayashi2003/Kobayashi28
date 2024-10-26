import requests
import os
from flask import url_for
from api.utils.logger import download_logger

def download_image(url: str, save_path: str) -> bool:
    try:
        response = requests.get(url, stream=True)
        response.raise_for_status()
        
        with open(save_path, 'wb') as file:
            for chunk in response.iter_content(chunk_size=8192):
                file.write(chunk)
        
        download_logger.info(f"Image downloaded successfully: {url}")
        return True
    except requests.RequestException as e:
        download_logger.error(f"Error downloading image {url}: {str(e)}")
        return False
    except IOError as e:
        download_logger.error(f"Error saving image {save_path}: {str(e)}")
        return False

def extract_images(vn_data: dict, id: str) -> list:
    pass