from datetime import datetime 
from typing import Tuple

from pydantic import BaseModel

class Delivery(BaseModel):
    timestamp: datetime
    dimensions: Tuple[int, int]


m = Delivery(timestamp='2020-01-01 12:00', dimensions=['10', '20'])
print(repr(m.timestamp))
print(m.dimensions)