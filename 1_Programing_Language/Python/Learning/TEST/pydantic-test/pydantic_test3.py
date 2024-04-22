from pydantic import BaseModel, Field, ValidationError

from typing import Optional

class Fruit(BaseModel):
    name: str
    color: str
    weight: float
    bazam: Optional[dict] = Field(None)

try:
    Fruit(
        name = 'Apple',
        color = 'red',
        weight = "forty-two", # pydantic.error_wrappers.ValidationError: 1 validation error for Fruit
        bazam = {'foobar': [(1, True, 0.1)]},
    )
except ValidationError as e:
    print(f"Throw Error 1: {e}")


print('='*50)


try:
    Fruit(
        name = 'Apple',
        # color = 'red',
        weight = 4.2,
        # bazam = None # In pydantic v2, if you haven't set the default value for bazam, 
                       # you may need to set it to None, even if it is an Optional field.
    )
except ValidationError as e:
    print(f'Throw Error 2: {e}')