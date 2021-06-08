from fastapi import Depends, HTTPException
from fastapi.responses import Response

from src.dependencies.authentication import AuthHandler, UserAuthenticator
from src.ext import APIRouter
from src.infrastructure.repository.accounts import Account, AccountsRepo
from . import models

router = APIRouter(prefix="/account", tags=["Account Management"])

requires_admin = UserAuthenticator(requires_admin=True)
requires_user = UserAuthenticator()


@router.get("/", response_model=models.AccountOut)
async def get_account(acc: Account = Depends(requires_user), handler: AuthHandler = Depends()):
    return handler.encode_payload(acc.to_dict())


@router.post("/", response_model=models.AccountOut)
async def create_account(payload: models.AccountCreateIn,
                         repo: AccountsRepo = Depends(),
                         handler: AuthHandler = Depends()):
    acc = await repo.add_account(**payload.dict())
    return handler.encode_payload(acc.to_dict())


@router.put("/", response_model=models.AccountOut)
async def update_account(payload: models.AccountCreateIn,
                         acc: Account = Depends(requires_user),
                         repo: AccountsRepo = Depends(),
                         handler: AuthHandler = Depends()):
    acc = await repo.update_account(acc.id, **payload.dict())
    return handler.encode_payload(acc.to_dict())


@router.delete("/", dependencies=[Depends(UserAuthenticator(requires_admin=True))])
async def delete_admin(repo: AccountsRepo = Depends(),
                       acc: Account = Depends(requires_admin)):
    success = await repo.remove_account(acc.id)
    if not success:
        raise HTTPException(status_code=404, detail=f"no admin with id {id}")
    return Response(status_code=200)


@router.put("/admin", dependencies=[Depends(requires_admin)])
async def update_admin_status(payload: models.AdminUpdateIn, repo: AccountsRepo = Depends()):
    await repo.set_account_admin_status(payload.id, payload.is_admin)
    return Response(status_code=200)
