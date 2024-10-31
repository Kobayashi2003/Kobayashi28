import requests
import os
from flask import current_app
from api.utils.logger import download_logger


def download_image(url: str, save_path: str) -> bool:
    try:
        if os.path.exists(save_path):
            download_logger.info(f"Image already exists: {save_path}")
            return True

        response = requests.get(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36'
        }, timeout=10)
        response.raise_for_status()
        
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
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

def extract_images(vn_data: dict, vn_id: str) -> list:
    images = []
    
    if vn_data.get('image') and vn_data['image'].get('url'):
        images.append({
            'url': vn_data['image']['url'],
            'filename': f"{vn_id}_main.{vn_data['image']['url'].split('.')[-1]}",
            'type': 'main'
        })
    
    if vn_data.get('screenshots') and isinstance(vn_data['screenshots'], list):
        for i, screenshot in enumerate(vn_data['screenshots']):
            if screenshot.get('url'):
                images.append({
                    'url': screenshot['url'],
                    'filename': f"{vn_id}_screenshot_{i}.{screenshot['url'].split('.')[-1]}",
                    'type': 'screenshot'
                })
    
    if vn_data.get('va') and isinstance(vn_data['va'], list):
        for i, va in enumerate(vn_data['va']):
            if va.get('character') and va['character'].get('image') and va['character']['image'].get('url'):
                images.append({
                    'url': va['character']['image']['url'],
                    'filename': f"{vn_id}_character_{i}.{va['character']['image']['url'].split('.')[-1]}",
                    'type': 'character'
                })
    
    return images

def get_image_url(vn_id: str, filename: str) -> str:
    return f"{current_app.config['IMAGES_URL_PREFIX']}/{vn_id}/{filename}"