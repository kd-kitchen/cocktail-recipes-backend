import datetime

from pydantic import EmailStr, validator

from src.ext import CamelModel


class IngredientCreateIn(CamelModel):
    iname: str
    creator_id: int
    description: str

    @validator('iname')
    def name_not_empty(cls, v: str):
        v = v.strip().lower()
        if len(v) == 0:
            raise ValueError("What is the name of your ingredient?")
        return v

    @validator('description')
    def description_not_empty(cls, v: str):
        if len(v) == 0:
            raise ValueError("Describe what the ingredient is!")
        return v


class IngredientOut(CamelModel):
    iid: int
    iname: str
    creator_id: int
    creation_date: datetime.datetime
    last_updated: datetime.datetime
    description: str


# class AdminUpdateIn(CamelModel):
#     id: int
#     is_admin: bool
