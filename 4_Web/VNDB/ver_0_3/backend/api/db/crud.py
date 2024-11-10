from api.db import models
from api.db.database import db

from typing import List, Dict, Any, Union, Optional

ModelType = Union[models.VN, models.Tag, models.Producer, models.Staff, models.Character, models.Trait, models.LocalVN, models.LocalTag, models.LocalProducer, models.LocalStaff, models.LocalCharacter, models.LocalTrait]

MODEL_MAP = {
    'vn': models.VN,
    'tag': models.Tag,
    'producer': models.Producer,
    'staff': models.Staff,
    'character': models.Character,
    'trait': models.Trait,
    'local_vn': models.LocalVN,
    'local_tag': models.LocalTag,
    'local_producer': models.LocalProducer,
    'local_staff': models.LocalStaff,
    'local_character': models.LocalCharacter,
    'local_trait': models.LocalTrait,
}

def create(type: str, id: str, data: Dict[str, Any]) -> ModelType:
    model = MODEL_MAP.get(type)
    if not model:
        raise ValueError(f"Invalid model type: {type}")
    
    item = model(id=id, **data)
    db.session.add(item)
    db.session.commit()
    return item

def update(type: str, id: str, data: Dict[str, Any]) -> Optional[ModelType]:
    model = MODEL_MAP.get(type)
    if not model:
        raise ValueError(f"Invalid model type: {type}")
    
    item = model.query.get(id)
    if item:
        for key, value in data.items():
            setattr(item, key, value)
        db.session.commit()
    return item

def delete(type: str, id: str) -> bool:
    model = MODEL_MAP.get(type)
    if not model:
        raise ValueError(f"Invalid model type: {type}")
    
    item = model.query.get(id)
    if item:
        db.session.delete(item)
        db.session.commit()
        return True
    return False

def get(type: str, id: str) -> Optional[ModelType]:
    model = MODEL_MAP.get(type)
    if not model: 
        raise ValueError(f"Invalid model type: {type}")
    
    return model.query.get(id)

def get_all(type: str) -> List[ModelType]:
    model = MODEL_MAP.get(type)
    if not model:
        raise ValueError(f"Invalid model type: {type}")

    return model.query.all()

def exists(type: str, id: str) -> bool:
    model = MODEL_MAP.get(type)
    if not model:
        raise ValueError(f"Invalid model type: {type}")
    return model.query.filter_by(id=id).first() is not None