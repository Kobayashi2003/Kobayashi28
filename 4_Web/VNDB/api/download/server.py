import os
from flask import current_app
from api.download.utils import download_image, extract_images 
from api.utils.logger import download_logger
from api.db.operations import search 
from concurrent.futures import ThreadPoolExecutor


def download2server(filters):
    try:
        # Search for VNs matching the filters
        vns = search(filters)
        
        if not vns:
            download_logger.info("No VNs found matching the filters")
            return []
        
        downloaded_images = []
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = []
            for vn in vns:
                vn_id = vn['id']
                images = extract_images(vn['data'], vn_id)
                for image in images:
                    save_path = os.path.join(current_app.config['IMAGES_FOLDER'], vn_id, image['filename'])
                    futures.append(executor.submit(download_image, image['url'], save_path))
            
            for future in futures:
                if future.result():
                    downloaded_images.append(future.result())
        
        download_logger.info(f"Downloaded {len(downloaded_images)} images to server")
        return downloaded_images
    
    except Exception as e:
        download_logger.error(f"Error in download2server: {str(e)}")
        raise