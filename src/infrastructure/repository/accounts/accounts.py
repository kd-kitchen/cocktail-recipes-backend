import random
import string
from typing import Optional

from src.infrastructure.database import db
from .dataclasses import Account
from .utils import hash_password, validate

__all__ = ['AccountsRepo']


class AccountsRepo:
    @staticmethod
    async def set_account_admin_status(id: int, is_admin):
        await db.execute("""
        UPDATE account.account
        SET is_admin = :is_admin
        WHERE id = :id
        """, {'id': id, 'is_admin': is_admin})

    @staticmethod
    async def fetch_account(username: str) -> Optional[Account]:
        """Returns the account if and only if the username and password are valid"""
        res = await db.fetch_one("""
        SELECT id, username, password, email, is_admin
        FROM account.account
        WHERE LOWER(username) = :username
        """, {'username': username.lower()})

        return Account(**res) if res is not None else None

    @staticmethod
    async def fetch_account_by_id(id: int) -> Optional[Account]:
        res = await db.fetch_one("""
        SELECT id, username, password , email, is_admin
        FROM account.account
        WHERE id = :id
        """, {'id': id})

        return Account(**res) if res is not None else None

    async def add_account(self, username: str, password: str, email: str) -> Account:
        username, password = self._format_inputs(username, password)
        id: int = await db.execute("""
        INSERT INTO account.account (username, password, email, is_admin) 
        VALUES (:username, :password, :email, FALSE) 
        RETURNING id
        """, {"username": username, "password": password, "email": email})

        return Account(id, username, password, email, False)

    async def update_account(self, id: int, username: str, password: str, email: str) -> Optional[Account]:
        if await self.fetch_account_by_id(id) is None:
            return None

        username, password = self._format_inputs(username, password)
        payload = {"id": id, "username": username, "password": password, "email": email}

        is_admin = await db.execute("""
        UPDATE account.account
        SET username = :username, 
            password = :password,
            email    = :email
        WHERE id = :id
        RETURNING is_admin
        """, payload)

        return Account(**payload, is_admin=is_admin)

    async def remove_account(self, id: int):
        if await self.fetch_account_by_id(id) is None:
            return False

        await db.execute("DELETE FROM account.account WHERE id = :id", {'id': id})
        return True

    @staticmethod
    def _format_inputs(username: str, password: str):
        username = username.lower()

        choices = string.ascii_letters + string.digits
        salt = ''.join(random.choice(choices) for _ in range(6))
        password = hash_password(password, salt)

        return username, password

    validate = staticmethod(validate)
