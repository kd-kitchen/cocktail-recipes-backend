from fastapi import APIRouter, Depends

from src.dependencies.authentication import UserAuthenticator

router = APIRouter(prefix="/recipe", tags=["Recipe Management"])

requires_user = UserAuthenticator()


@router.get("/")
def get_all_recipes():
    raise NotImplementedError


@router.get("/<id:int>")
def get_recipe_details():
    raise NotImplementedError


@router.post("/", dependencies=[Depends(requires_user)])
def add_recipe():
    raise NotImplementedError


@router.put("/<id:int>", dependencies=[Depends(requires_user)])
def update_recipe():
    raise NotImplementedError


@router.delete("/<id:int>", dependencies=[Depends(requires_user)])
def delete_recipe():
    raise NotImplementedError
