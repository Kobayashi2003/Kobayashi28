import os

from flask import current_app

def get_image_path(resource_type: str, image_id: str) -> str:
    """
    Get the path of an image file if it exists and is associated with the given resource.
    
    :param resource_type: The type of resource ('vn' or 'character')
    :param image_id: The ID of the image
    :return: The path to the image file if it exists and is associated with the resource, None otherwise
    """
    image_folder = get_image_folder(resource_type=resource_type)
    image_path = os.path.join(image_folder, f"{image_id}.jpg")

    return image_path if os.path.exists(image_path) else ''

def get_savedata_path(savedata_id: str) -> str:
    """
    Get the path of a savedata file if it exists and is associated with the given VN.
    
    :param savedata_id: The ID of the savedata
    :return: The path to the savedata file if it exists and is associated with the VN, None otherwise
    """
    savedata_folder = get_savedata_folder()
    savedata_path = os.path.join(savedata_folder, savedata_id)

    return savedata_path if os.path.exists(savedata_path) else ''

def get_backup_path(backup_id: str) -> str:
    """
    Get the full path for a backup file.

    :param back_id: The ID of the backup
    :return: The full path to the backup file
    """
    backup_folder = get_backup_folder()
    backup_path = os.path.join(backup_folder, f"{backup_id}.dump")
   
    return backup_path if os.path.exists(backup_path) else ''



def get_image_folder(resource_type: str) -> str:
    """
    Get the image folder path for a given resource type from the current app config.
    
    Args:
        resource_type (str): The type of resource (e.g., 'vn', 'character')
    
    Returns:
        str: The path to the image folder for the given resource type
    
    Raises:
        ValueError: If the resource type is not supported or the config key is not found
    """
    config_key = f'IMAGE_{resource_type.upper()}_FOLDER'
    
    if config_key not in current_app.config:
        raise ValueError(f"Unsupported resource type: {resource_type}")
    
    return current_app.config[config_key]

def get_savedata_folder() -> str:
    """
    Get the savedata folder path from the current app config.
    
    Returns:
        str: The path to the savedata folder
    
    Raises:
        ValueError: If the config key for the savedata folder is not found
    """
    config_key = 'SAVEDATA_FOLDER'
    
    if config_key not in current_app.config:
        raise ValueError(f"Config key not found: {config_key}")
    
    return current_app.config[config_key]

def get_backup_folder() -> str:
    """
    Get the backup folder path from the current app config.
    
    Returns:
        str: The path to the backup folder
    
    Raises:
        ValueError: If the config key for the backup folder is not found
    """
    config_key = 'BACKUP_FOLDER'
    
    if config_key not in current_app.config:
        raise ValueError(f"Config key not found: {config_key}")
    
    return current_app.config[config_key]

