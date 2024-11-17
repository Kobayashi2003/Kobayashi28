from typing import Optional, List

from celery import chain
from api import celery
from api.database import exists, delete, delete_all, delete_images, delete_savedatas, get_all

@celery.task(bind=True)
def delete_vns_task(self, vn_id: Optional[str] = None):
    """
    Delete a VN and its associated images and savedatas.
    If vn_id is None, deletes all VNs.
    """
    self.update_state(state='PROGRESS', meta={'status': 'Initializing VN deletion...'})
    
    if vn_id:
        # Single VN deletion
        if not exists('vn', vn_id):
            return {"status": "NOT_FOUND", "result": None}
        
        deletion_chain = chain(
            delete_vn_images.s(vn_id),
            delete_vn_savedatas.s(vn_id),
            delete_single_vn.s(vn_id)
        )
    else:
        # Bulk VN deletion
        vn_ids = [vn.id for vn in get_all('vn')]
        deletion_chain = chain(
            delete_all_vn_images.s(vn_ids),
            delete_all_vn_savedatas.s(vn_ids),
            delete_all_vns.s()
        )
    
    result = deletion_chain.apply_async()
    return {"status": "SUCCESS", "task_id": result.id}

@celery.task
def delete_vn_images(vn_id: str):
    """Task to delete all images for a single VN."""
    try:
        deleted_count = delete_images('vn', vn_id)
        return {"status": "SUCCESS", "result": f"{deleted_count} images deleted for VN {vn_id}"}
    except Exception as e:
        return {"status": "ERROR", "result": str(e)}

@celery.task
def delete_vn_savedatas(vn_id: str):
    """Task to delete all savedatas for a single VN."""
    try:
        deleted_count = delete_savedatas(vn_id)
        return {"status": "SUCCESS", "result": f"{deleted_count} savedatas deleted for VN {vn_id}"}
    except Exception as e:
        return {"status": "ERROR", "result": str(e)}

@celery.task
def delete_single_vn(vn_id: str):
    """Task to delete a single VN after its dependencies have been deleted."""
    try:
        success = delete('vn', vn_id)
        if success:
            return {"status": "SUCCESS", "result": f"VN {vn_id} deleted successfully"}
        else:
            return {"status": "NOT_FOUND", "result": f"VN {vn_id} not found"}
    except Exception as e:
        return {"status": "ERROR", "result": str(e)}

@celery.task
def delete_all_vn_images(vn_ids: List[str]):
    """Task to delete all images for all VNs."""
    try:
        total_deleted = 0
        for vn_id in vn_ids:
            total_deleted += delete_images('vn', vn_id)
        return {"status": "SUCCESS", "result": f"{total_deleted} images deleted for all VNs"}
    except Exception as e:
        return {"status": "ERROR", "result": str(e)}

@celery.task
def delete_all_vn_savedatas(vn_ids: List[str]):
    """Task to delete all savedatas for all VNs."""
    try:
        total_deleted = 0
        for vn_id in vn_ids:
            total_deleted += delete_savedatas(vn_id)
        return {"status": "SUCCESS", "result": f"{total_deleted} savedatas deleted for all VNs"}
    except Exception as e:
        return {"status": "ERROR", "result": str(e)}

@celery.task
def delete_all_vns():
    """Task to delete all VNs after their dependencies have been deleted."""
    try:
        deleted_count = delete_all('vn')
        return {"status": "SUCCESS", "result": f"{deleted_count} VNs deleted successfully"}
    except Exception as e:
        return {"status": "ERROR", "result": str(e)}