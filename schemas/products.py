from pydantic import BaseModel, Field


class SchemaProducts(BaseModel):
    name : str
    heading : str
    price : int
    amount : int
    image : str