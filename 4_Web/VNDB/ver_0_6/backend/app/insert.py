from app import db
from .models import Tag 
from .search import search_cache

def insert_tag(tag_id: str) -> Tag:
    tag_data = search_cache('tag', {'id': tag_id}, response_size='large')
    if not tag_data['results']:
        raise ValueError(f"No tag found with id: {tag_id}")
    tag_info = tag_data['results'][0]
    
    tag = Tag(
        id=tag_info['id'],
        name=tag_info['name'],
        aliases=tag_info.get('aliases', []),
        description=tag_info.get('description', ''),
        category=tag_info.get('category', ''),
        searchable=tag_info.get('searchable', False),
        applicable=tag_info.get('applicable', False),
        vn_count=tag_info.get('vn_count', 0)
    )
    db.session.add(tag)

    try:
        db.session.commit()
        print(f"Successfully inserted tag: {tag.name}")
    except Exception as e:
        db.session.rollback()
        print(f"Error inserting tag: {str(e)}")
        raise
    
    return tag
