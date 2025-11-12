from pydantic import BaseModel

class SchemaOrderItem(BaseModel):
    product_id: int
    amount: int
    price: int
    order_id: int
