from typing import Optional, Literal, Union, List

import re

def is_valid_id(id: str, valid_letters: Optional[Union[str, List[str]]] = None) -> bool:
    """
    Check if the given id is valid.
    
    A valid id must start with a letter followed by numbers.
    
    Args:
        id (str): The id to check.
        valid_letters (Optional[Union[str, List[str]]]): A string or list of strings containing all valid starting letters.
                                                         If None, all letters are considered valid.
    
    Returns:
        bool: True if the id is valid, False otherwise.
    
    Example:
        >>> is_valid_id('a123')
        True
        >>> is_valid_id('123a')
        False
        >>> is_valid_id('a')
        False
        >>> is_valid_id('1')
        False
        >>> is_valid_id('b123', valid_letters='abc')
        True
        >>> is_valid_id('d123', valid_letters='abc')
        False
        >>> is_valid_id('a123', valid_letters=['a', 'b', 'c'])
        True
        >>> is_valid_id('d123', valid_letters=['a', 'b', 'c'])
        False
    """
    if valid_letters is None:
        pattern = r'^[a-zA-Z]\d+$'
    else:
        if isinstance(valid_letters, str):
            letters = re.escape(valid_letters)
        else:
            letters = ''.join(re.escape(letter) for letter in valid_letters)
        pattern = f'^[{letters}]\d+$'
    
    return bool(re.match(pattern, id))

def infer_type_from_id(id: str) -> Literal['vn', 'character', 'tag', 'producer', 'staff', 'trait'] | None:
    """
    Infer the type of entity based on the first letter of the ID.

    This function should be used after validating the ID with is_valid_id().

    Args:
        id (str): The ID to infer the type from.

    Returns:
        Literal['vn', 'character', 'tag', 'producer', 'staff', 'trait'] | None: 
        The inferred type, or None if the type cannot be inferred.

    Example:
        >>> infer_type_from_id('v123')
        'vn'
        >>> infer_type_from_id('c456')
        'character'
        >>> infer_type_from_id('t789')
        'tag'
        >>> infer_type_from_id('p101')
        'producer'
        >>> infer_type_from_id('s202')
        'staff'
        >>> infer_type_from_id('r303')
        'trait'
        >>> infer_type_from_id('x404')
        None
    """
    if not is_valid_id(id):
        return None

    type_map = {
        'v': 'vn',
        'c': 'character',
        't': 'tag',
        'p': 'producer',
        's': 'staff',
        'r': 'trait'
    }
    
    first_letter = id[0].lower()
    return type_map.get(first_letter)

def is_valid_image_id(image_id: str, image_type: Literal['vn', 'character']) -> bool:
    """
    Check if the given image id is valid for the specified type.

    For 'vn' type, valid prefixes are 'cv', 'cv_t', 'sf', 'sf_t', 'u' followed by numbers.
    For 'character' type, valid prefixes are 'ch', 'u' followed by numbers.

    Args:
        image_id (str): The image id to check.
        image_type (Literal['vn', 'character']): The type of the image ('vn' or 'character').

    Returns:
        bool: True if the image id is valid for the specified type, False otherwise.

    Example:
        >>> is_valid_image_id('cv123', 'vn')
        True
        >>> is_valid_image_id('sf_t456', 'vn')
        True
        >>> is_valid_image_id('ch789', 'character')
        True
        >>> is_valid_image_id('x101', 'vn')
        False
        >>> is_valid_image_id('ch202', 'vn')
        False
        >>> is_valid_image_id('cv303', 'character')
        False
    """
    if image_type == 'vn':
        pattern = r'^(cv|cv_t|sf|sf_t|u)\d+$'
    elif image_type == 'character':
        pattern = r'^(ch|u)\d+$'
    else:
        return False

    return bool(re.match(pattern, image_id))