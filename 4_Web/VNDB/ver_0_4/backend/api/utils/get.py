from flask import current_app

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