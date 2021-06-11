import datetime

from pydantic import EmailStr, validator

from src.ext import CamelModel


class AccountCreateIn(CamelModel):
    username: str
    password: str
    email: EmailStr

    @validator('username')
    def username_not_empty(cls, v: str):
        v = v.strip().lower()
        if len(v) == 0:
            raise ValueError("username must not be empty")
        return v

    @validator('password')
    def password_not_empty(cls, v: str):
        if len(v) == 0:
            raise ValueError("password must not be empty")
        return v


class AccountOut(CamelModel):
    username: str
    email: str
    token: str
    is_admin: bool
    exp: datetime.datetime


class AdminUpdateIn(CamelModel):
    id: int
    is_admin: bool
