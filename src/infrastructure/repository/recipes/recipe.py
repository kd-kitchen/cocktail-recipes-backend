from collections import defaultdict

from src.application.routers.recipe.models import IngredientOut, RecipeOut
from src.infrastructure.database import db

__all__ = ['RecipeRepo']


class RecipeRepo:
    @staticmethod
    async def fetch_all_recipes():
        recipes = await db.fetch_all("""
        SELECT r.id, r.name, r.description, r.instruction, img.image_url
        FROM recipe.recipe AS r
        LEFT JOIN recipe.recipe_image AS img 
            ON r.id = img.recipe_id
        """)

        ingredients = await db.fetch_all(f"""
        SELECT x.recipe_id, 
               x.ingredient_id AS id,
               x.quantity,
               x.unit,
               ing.name,
               ing.description, 
               img.image_url
        FROM recipe.recipe_ingredient_assc_table AS x
        LEFT JOIN recipe.ingredient AS ing
            ON x.ingredient_id = ing.id
        LEFT JOIN recipe.ingredient_image img
            ON ing.id = img.ingredient_id
        WHERE x.recipe_id in ({', '.join(str(r['id']) for r in recipes)})
        """)

        ingredients_map = defaultdict(list)
        for x in ingredients:
            ingredients_map[x['recipe_id']].append(IngredientOut(id=x['id'],
                                                                 name=x['name'],
                                                                 unit=x['unit'],
                                                                 quantity=x['quantity'],
                                                                 description=x['description'],
                                                                 image_url=x['image_url']))

        return [RecipeOut(id=r['id'],
                          name=r['name'],
                          description=r['description'],
                          instruction=r['instruction'],
                          image_url=r['image_url'],
                          ingredients=ingredients_map[r['id']]) for r in recipes]
