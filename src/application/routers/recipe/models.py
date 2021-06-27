from typing import Optional

from pydantic import Field, validator

from src.ext import CamelModel


class RecipeIngredientInfoIn(CamelModel):
    id: int
    quantity: int = Field(..., gt=0)
    unit: str

    @validator('unit')
    def unit_not_empty(cls, v: str):
        v = v.strip().lower()
        if len(v) == 0:
            raise ValueError("unit cannot be empty or whitespace")
        return v


class RecipeCreateIn(CamelModel):
    name: str
    description: str
    instruction: str
    ingredients: list[RecipeIngredientInfoIn]

    @validator('name')
    def name_not_empty(cls, v: str):
        v = v.strip().lower()
        if len(v) == 0:
            raise ValueError("What is the name of your ingredient?")
        return v


class IngredientOut(CamelModel):
    id: int
    name: str
    quantity: float
    unit: str
    description: str
    image_url: Optional[str]


class RecipeOut(CamelModel):
    id: int
    name: str
    description: str
    instruction: str
    image_url: str
    ingredients: list[IngredientOut]
