import os

def get_image_path(image_id):
    """
    Generate the file path for an image based on its ID.
    Images are stored in subdirectories, each containing 100 images.
    """
    base_dir = 'images'
    sub_dir = str(image_id // 100)
    filename = f"{image_id}.jpg"  # Assuming all images are saved as JPG
    
    # Create the directory if it doesn't exist
    full_dir = os.path.join(base_dir, sub_dir)
    os.makedirs(full_dir, exist_ok=True)
    
    return os.path.join(full_dir, filename)
