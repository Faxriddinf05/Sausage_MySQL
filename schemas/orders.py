from pydantic import BaseModel
from typing import List

class SchemaOrderItem(BaseModel):
    product_id: int
    amount: int

class SchemaOrder(BaseModel):
    user_id: int
    address: str
    items: List[SchemaOrderItem]
