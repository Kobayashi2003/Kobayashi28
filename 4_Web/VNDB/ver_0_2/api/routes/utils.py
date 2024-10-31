from flask import request
from typing import Dict,Any, List, Optional

def get_filters(search_type: str) -> Dict[str, Any]:
    if search_type == 'local':
        return {
            'id':           request.args.get('localID'),
            'title':        request.args.get('localTitle'),
            'length':       request.args.get('localLength'),
            'tags':         split_arg('localTags'),
            'developers':   split_arg('localDevelopers'),
            'characters':   split_arg('localCharacters')
        }
    else:  # vndb
        return {
            'query':        request.args.get('vndbQuery'),
            'developers':   split_arg('vndbDevelopers'),
            'characters':   split_arg('vndbCharacters'),
            'staffs':       split_arg('vndbStaffs'),
            'released_date_expressions': split_arg('vndbReleasedDate'),
            'length':       parse_int('vndbLength'),
            'dev_status':   parse_int('vndbDevStatus'),
            'has_anime':    is_checked('vndbHasAnime'),
            'has_review':   is_checked('vndbHasReview'),
            'has_screenshot': is_checked('vndbHasScreenshot'),
            'has_description': is_checked('vndbHasDescription')
        }

def split_arg(key: str, delimiter: str = ',') -> List[str]:
    args = request.args.get(key, '').split(delimiter) if request.args.get(key) else []
    return [arg.strip() for arg in args]

def parse_int(key: str) -> Optional[int]:
    value = request.args.get(key)
    return int(value) if value else None

def is_checked(key: str) -> bool:
    return request.args.get(key) == 'on'