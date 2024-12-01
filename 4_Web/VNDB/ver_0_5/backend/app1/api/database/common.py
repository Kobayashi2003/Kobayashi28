from datetime import date, datetime

from sqlalchemy import inspect
from sqlalchemy.dialects.postgresql import JSON, JSONB, ARRAY

def convert_model_to_dict(model):
    result = {}
    for column in inspect(model).mapper.column_attrs:
        value = getattr(model, column.key)
        if isinstance(value, (str, int, float, bool, type(None))):
            result[column.key] = value
        elif isinstance(value, (datetime, date)):
            result[column.key] = value.isoformat()
        elif isinstance(column.columns[0].type, ARRAY):
            if value is not None:
                result[column.key] = [
                    item if isinstance(item, (str, int, float, bool, type(None)))
                    else str(item)
                    for item in value
                ]
            else:
                result[column.key] = None
        elif isinstance(column.columns[0].type, (JSON, JSONB)):
            result[column.key] = value  # JSON and JSONB types are already serializable
        else:
            # For any other types, convert to string
            result[column.key] = str(value)
    return result