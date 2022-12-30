from typing import Union
from pydantic import BaseModel, Field


class Category(BaseModel):
    category_id: int
    name: str
    categories: Union["list[Category]", list[None]] = Field(alias='children')