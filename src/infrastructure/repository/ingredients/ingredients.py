import datetime
import random
import string
from typing import Optional

from src.infrastructure.database import db
from .dataclasses import Ingredient

__all__ = ['IngredientsRepo']


class IngredientsRepo:
    @staticmethod
    async def fetch_all_ingredients():
        results = await db.fetch_all("""
        select id, name, description
        FROM recipe.ingredient
        """)

        return [Ingredient(**r) for r in results]

    @staticmethod
    async def fetch_ingredient_by_iid(id: int) -> Optional[Ingredient]:
        """Always returns ingredient based on ingredient id (iid) upon request"""
        res = await db.fetch_one("""
        SELECT *
        FROM recipe.ingredient
        WHERE id = :id
        """, {'id': id})

        return Ingredient(**res) if res is not None else None

    @staticmethod
    async def fetch_ingredient_by_name(name: str) -> Optional[Ingredient]:
        res = await db.fetch_all("""
        SELECT *
        FROM recipe.ingredient
        WHERE (name OR description) SIMILAR TO name
        """, {'name': name})

        return Ingredient(**res) if res is not None else None

    async def add_ingredient(self, name: str, description: str) -> Ingredient:
        name = self._format_inputs(name)
        description = description
        id = await db.execute("""
        INSERT INTO recipe.ingredient (name, description)
        VALUES (:name, :description)
        RETURNING id
        """, {"name": name, "description": description})

        return Ingredient(id, name, description)

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

    @staticmethod
    def _format_inputs(nae: str):
        nae = nae.lower()

        return nae
