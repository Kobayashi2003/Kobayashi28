from typing import Annotated, Dict, List, Literal, Tuple

from annotated_types import Gt 

from pydantic import BaseModel 

class Fruit(BaseModel):
    name: str
    color: Literal['red', 'green'] 
    weight: Annotated[float, Gt(0)]
    bazam: Dict[str, List[Tuple[int, bool, float]]]


print(
    Fruit(
        name = 'Apple',
        color = 'red', 
        weight = 4.2, 
        bazam = {'foobar': [(1, True, 0.1)]},
    )
)