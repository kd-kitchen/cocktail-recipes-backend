from fastapi import Depends

from src.dependencies.authentication import UserAuthenticator
from src.ext import APIRouter
from src.infrastructure.repository.ingredients import IngredientsRepo
from . import models

router = APIRouter(prefix="/ingredient", tags=["Ingredient Management"])

requires_admin = UserAuthenticator(requires_admin=True)
requires_user = UserAuthenticator()


@router.get("/", response_model=list[models.IngredientOut])
async def fetch_all_ingredients(repo: IngredientsRepo = Depends()):
    results = await repo.fetch_all_ingredients()
    return [r.to_dict() for r in results]


@router.get("/{id}", response_model=models.IngredientOut)
async def get_ingredient(id: int, repo: IngredientsRepo = Depends()):
    return (await repo.fetch_ingredient_by_iid(id)).to_dict()


@router.post("/", response_model=models.IngredientCreateIn)
async def create_ingredient(payload: models.IngredientCreateIn,
                            repo: IngredientsRepo = Depends()):
    return (await repo.add_ingredient(**payload.dict())).to_dict()
