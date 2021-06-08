from base64 import b64decode
from pathlib import Path
from typing import Optional, TypedDict

import jwt
from fastapi import Depends, HTTPException, Header

from src.infrastructure.repository.accounts import AccountsRepo

__all__ = ['AuthHandler', 'UserAuthenticator']


class AccountDict(TypedDict):
    username: str
    email: str
    is_admin: str


class AuthHandler:
    def __init__(self):
        self._algorithm = 'HS256'
        path_to_secret = Path(__file__).parents[3] / 'tmp' / 'secret.txt'

        with open(path_to_secret) as f:
            self._secret = f.read()

    def encode_payload(self, payload: dict):
        token = jwt.encode(payload, self._secret, algorithm=self._algorithm)
        return {**payload, "token": token}

    def decode_payload(self, token: str) -> AccountDict:
        return jwt.decode(token, self._secret, algorithms=self._algorithm)


class UserAuthenticator:
    def __init__(self, *, requires_admin=False):
        self._requires_admin = requires_admin

    async def __call__(self,
                       authorization: Optional[str] = Header(None),
                       repo: AccountsRepo = Depends(),
                       handler: AuthHandler = Depends()):
        if authorization is None:
            raise HTTPException(status_code=403, detail="User details missing")

        if authorization.startswith('Bearer'):
            acc = await self.decode_jwt_token(authorization, repo, handler)
        else:
            acc = await self.decode_basic_auth(authorization, repo)

        if self._requires_admin and not acc.is_admin:
            raise HTTPException(status_code=403, detail="User is not an admin")

        return acc

    @staticmethod
    async def decode_basic_auth(authorization: str, repo: AccountsRepo):
        uid, pwd = b64decode(authorization.split(' ')[1]).decode('utf-8').split(':')
        acc = await repo.fetch_account(uid)
        if acc is None or not repo.validate(acc, pwd):
            raise HTTPException(status_code=403, detail="Invalid credentials")

        return acc

    @staticmethod
    async def decode_jwt_token(authorization: str, repo: AccountsRepo, handler: AuthHandler):
        *_, token = authorization.split(' ')

        try:
            payload = handler.decode_payload(token)
            return await repo.fetch_account(payload['username'])

        except jwt.DecodeError:
            raise HTTPException(status_code=403, detail="Invalid credentials")
