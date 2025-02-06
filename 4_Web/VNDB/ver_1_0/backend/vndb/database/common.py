import json
from datetime import date, datetime
from sqlalchemy import inspect
from sqlalchemy.dialects.postgresql import JSON, JSONB, ARRAY
from sqlalchemy.orm.attributes import InstrumentedAttribute

def convert_model_to_dict(model):
    result = {}
    for column in inspect(model).mapper.column_attrs:
        value = getattr(model, column.key)
        result[column.key] = convert_value(value, column)
    return result

def convert_value(value, column=None):
    if isinstance(value, (str, int, float, bool, type(None))):
        return value
    elif isinstance(value, (datetime, date)):
        return value.isoformat()
    elif isinstance(value, list):
        return [convert_value(item) for item in value]
    elif isinstance(value, dict):
        return {k: convert_value(v) for k, v in value.items()}
    elif column and isinstance(column.columns[0].type, ARRAY):
        if value is not None:
            return [convert_value(item) for item in value]
        return None
    elif column and isinstance(column.columns[0].type, JSONB):
        return value  # JSONB is already JSON-serializable
    elif isinstance(value, InstrumentedAttribute):
        # Handle relationships
        if value.property.uselist:
            return [convert_model_to_dict(item) for item in value]
        elif value.property.mapper:
            return convert_model_to_dict(value)
    else:
        try:
            # Try to convert to JSON
            return json.loads(json.dumps(value))
        except:
            # If JSON conversion fails, convert to string as a last resort
            return str(value)