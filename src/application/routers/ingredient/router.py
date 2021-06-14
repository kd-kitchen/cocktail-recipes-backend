from fastapi import Depends, HTTPException
from fastapi.responses import Response

from src.dependencies.authentication import AuthHandler, UserAuthenticator
from src.ext import APIRouter
from src.infrastructure.repository.ingredients import Ingredient, IngredientsRepo
from . import models

router = APIRouter(prefix="/ingredient", tags=["Ingredient Management"])

requires_admin = UserAuthenticator(requires_admin=True)
requires_user = UserAuthenticator()


@router.get("/", response_model=models.IngredientOut)
async def get_ingredient(ingredients: Ingredient = Depends(requires_user)):
    return ingredients


@router.post("/", response_model=models.IngredientCreateIn)
async def create_ingredient(payload: models.IngredientCreateIn,
                            repo: IngredientsRepo = Depends()):
    ingredient = await repo.add_ingredient(**payload.dict())
    return ingredient.to_dict()
