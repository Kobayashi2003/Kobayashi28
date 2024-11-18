from typing import List, Optional

from celery import chain

from api import celery
from api.database import exists, delete, delete_all, delete_images, get_all

@celery.task(bind=True)
def delete_characters_task(self, character_id: Optional[str] = None):
    """
    Delete a character and its associated images.
    If character_id is None, deletes all characters.
    """
    self.update_state(state='PROGRESS', meta={'status': 'Initializing character deletion...'})
    
    if character_id:
        # Single character deletion
        if not exists('character', character_id):
            return {"status": "NOT_FOUND", "result": None}
        
        deletion_chain = chain(
            delete_character_images.s(character_id),
            delete_single_character.s(character_id)
        )
    else:
        # Bulk character deletion
        character_ids = [character.id for character in get_all('character')]
        deletion_chain = chain(
            delete_all_character_images.s(character_ids),
            delete_all_characters.s()
        )
    
    result = deletion_chain.apply_async()
    return {"status": "SUCCESS", "task_id": result.id}

@celery.task
def delete_character_images(character_id: str):
    """Task to delete all images for a single character."""
    try:
        deleted_count = delete_images('character', character_id)
        return {"status": "SUCCESS", "result": f"{deleted_count} images deleted for character {character_id}"}
    except Exception as e:
        return {"status": "ERROR", "result": str(e)}

@celery.task
def delete_single_character(character_id: str):
    """Task to delete a single character after its images have been deleted."""
    try:
        success = delete('character', character_id)
        if success:
            return {"status": "SUCCESS", "result": f"Character {character_id} deleted successfully"}
        else:
            return {"status": "NOT_FOUND", "result": f"Character {character_id} not found"}
    except Exception as e:
        return {"status": "ERROR", "result": str(e)}

@celery.task
def delete_all_character_images(character_ids: List[str]):
    """Task to delete all images for all characters."""
    try:
        total_deleted = 0
        for character_id in character_ids:
            total_deleted += delete_images('character', character_id)
        return {"status": "SUCCESS", "result": f"{total_deleted} images deleted for all characters"}
    except Exception as e:
        return {"status": "ERROR", "result": str(e)}

@celery.task
def delete_all_characters():
    """Task to delete all characters after their images have been deleted."""
    try:
        deleted_count = delete_all('character')
        return {"status": "SUCCESS", "result": f"{deleted_count} characters deleted successfully"}
    except Exception as e:
        return {"status": "ERROR", "result": str(e)}