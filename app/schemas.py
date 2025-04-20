from pydantic import BaseModel


class CreateProduct(BaseModel):
    name: str
    description: str
    price: str
    image_url: str
    stock: int
    category: int


class Category(BaseModel):
    name: str
    parent_id: int | None = None
