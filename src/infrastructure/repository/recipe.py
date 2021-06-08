from typing import Optional, TypedDict

from ..database import db

__all__ = ['RecipeRepo']


class RecipeRepo:
    def fetch_recipes(self):
        pass

    def add_recipe(self):
        pass

    def update_recipe(self):
        pass

    def remove_recipe(self):
        pass


class RecipeIngredientDict(TypedDict, total=False):
    id: int
    name: str


class RecipeIngredientRepo:
    @staticmethod
    async def _fetch_ingredient(id: int) -> Optional[RecipeIngredientDict]:
        res = await db.fetch_one("SELECT id, name FROM recipe.ingredient WHERE id = :id", {'id': id})
        return dict(res) if res is not None else res

    @staticmethod
    async def add_ingredient(name: str):
        payload = {'name': name}
        await db.execute("INSERT INTO recipe.ingredient (name) VALUES (:name)", payload)
        return payload

    async def update_ingredient(self, id: int, name: str) -> Optional[RecipeIngredientDict]:
        tag = self._fetch_ingredient(id)
        if tag is None:
            return None

        payload = {"name": name, "id": id}
        await db.execute("UPDATE recipe.ingredient SET name = :name WHERE id = :id", payload)
        return payload

    async def remove_ingredient(self, id: int):
        if await self._fetch_ingredient(id) is None:
            return False

        await db.execute("DELETE FROM recipe.tag WHERE id = :id", {'id': id})
        return True


class RecipeTagDict(TypedDict, total=False):
    id: int
    name: str


class RecipeTagRepo:
    @staticmethod
    async def _fetch_tag(id: int) -> Optional[RecipeTagDict]:
        res = db.fetch_one("SELECT id, name FROM recipe.tag WHERE id = :id", {'id': id})
        return dict(res) if res is not None else res

    @staticmethod
    async def add_tag(name: str) -> RecipeTagDict:
        payload = {'name': name}
        await db.execute("INSERT INTO recipe.tag (name) VALUES (:name)", payload)
        return payload

    async def update_tag(self, id: int, name: str) -> Optional[RecipeTagDict]:
        tag = self._fetch_tag(id)
        if tag is None:
            return None

        payload = {"name": name, "id": id}
        await db.execute("UPDATE recipe.tag SET name = :name WHERE id = :id", payload)
        return payload

    async def remove_tag(self, id: int):
        if await self._fetch_tag(id) is None:
            return False

        await db.execute("DELETE FROM recipe.tag WHERE id = :id", {'id': id})
        return True
