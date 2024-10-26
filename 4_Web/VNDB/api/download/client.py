import os
import zipfile
from flask import current_app
from api.utils.logger import download_logger 
from api.db.operations import search
from api.download.utils import download_image, extract_images
from concurrent.futures import ThreadPoolExecutor


def download2client(filters):
    try:
        # Search for VNs matching the filters
        vns = search(filters)
        
        if not vns:
            download_logger.info("No VNs found matching the filters")
            return None
        
        # Create a temporary zip file
        temp_zip = os.path.join(current_app.config['TEMP_FOLDER'], 'vn_images.zip')
        with zipfile.ZipFile(temp_zip, 'w') as zipf:
            with ThreadPoolExecutor(max_workers=10) as executor:
                futures = []
                for vn in vns:
                    vn_id = vn['id']
                    images = extract_images(vn['data'], vn_id)
                    for image in images:
                        save_path = os.path.join(current_app.config['IMAGES_FOLDER'], vn_id, image['filename'])
                        futures.append(executor.submit(download_image, image['url'], save_path))
                
                for future in futures:
                    future.result()
                
                for vn in vns:
                    vn_id = vn['id']
                    images = extract_images(vn['data'], vn_id)
                    for image in images:
                        image_path = os.path.join(current_app.config['IMAGES_FOLDER'], vn_id, image['filename'])
                        if os.path.exists(image_path):
                            zipf.write(image_path, os.path.join(vn_id, image['filename']))
        
        download_logger.info(f"Created zip file with images from {len(vns)} VNs")
        return temp_zip
    
    except Exception as e:
        download_logger.error(f"Error in download2client: {str(e)}")
        raise