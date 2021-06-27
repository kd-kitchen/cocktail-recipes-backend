from pydantic import validator

from src.ext import CamelModel


class IngredientCreateIn(CamelModel):
    name: str
    description: str

    @validator('name')
    def name_not_empty(cls, v: str):
        v = v.strip().lower()
        if len(v) == 0:
            raise ValueError("What is the name of your ingredient?")
        return v

    @validator('description')
    def description_not_empty(cls, v: str):
        if len(v) == 0:
            raise ValueError("Describe the shape size or color of your ingredient!")
        return v


class IngredientOut(CamelModel):
    id: int
    name: str
    description: str
