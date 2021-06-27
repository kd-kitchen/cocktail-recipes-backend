from fastapi import Depends

from src.dependencies.authentication import UserAuthenticator
from src.ext import APIRouter
from src.infrastructure.repository.recipes.recipe import RecipeRepo

router = APIRouter(prefix="/recipe", tags=["Recipe Management"])

requires_user = UserAuthenticator()


@router.get("/")
async def fetch_all_recipe(repo: RecipeRepo = Depends()):
    return await repo.fetch_all_recipes()
