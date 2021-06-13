import random
import string
from typing import Optional

from src.infrastructure.database import db
from .dataclasses import Ingredient

__all__ = ['IngredientsRepo']


class IngredientsRepo:

    @staticmethod
    async def fetch_ingredient_by_iid(iid: int) -> Optional[Ingredient]:
        """Always returns ingredient based on ingredient id (iid) upon request"""
        res = await db.fetch_one("""
        SELECT *
        FROM ingredient.ingredient
        WHERE iid = :iid
        """, {'iid': iid})

        return Ingredient(**res) if res is not None else None

    @staticmethod
    async def fetch_ingredient_by_name(name: str) -> Optional[Ingredient]:
        res = await db.fetch_all("""
        SELECT *
        FROM ingredient.ingredient
        WHERE (name OR description) SIMILAR TO name
        """, {'id': id})

        return Ingredient(**res) if res is not None else None

    # async def add_account(self, username: str, password: str, email: str) -> Account:
    #     username, password = self._format_inputs(username, password)
    #     id: int = await db.execute("""
    #     INSERT INTO account.account (username, password, email, is_admin)
    #     VALUES (:username, :password, :email, FALSE)
    #     RETURNING id
    #     """, {"username": username, "password": password, "email": email})
    #
    #     return Account(id, username, password, email, False)
    #
    # async def update_account(self, id: int, username: str, password: str, email: str) -> Optional[Account]:
    #     if await self.fetch_account_by_id(id) is None:
    #         return None
    #
    #     username, password = self._format_inputs(username, password)
    #     payload = {"id": id, "username": username, "password": password, "email": email}
    #
    #     is_admin = await db.execute("""
    #     UPDATE account.account
    #     SET username = :username,
    #         password = :password,
    #         email    = :email
    #     WHERE id = :id
    #     RETURNING is_admin
    #     """, payload)
    #
    #     return Account(**payload, is_admin=is_admin)
    #
    # async def remove_account(self, id: int):
    #     if await self.fetch_account_by_id(id) is None:
    #         return False
    #
    #     await db.execute("DELETE FROM account.account WHERE id = :id", {'id': id})
    #     return True
    #
    # @staticmethod
    # def _format_inputs(username: str, password: str):
    #     username = username.lower()
    #
    #     choices = string.ascii_letters + string.digits
    #     salt = ''.join(random.choice(choices) for _ in range(6))
    #     password = hash_password(password, salt)
    #
    #     return username, password
    #
    # validate = staticmethod(validate)
