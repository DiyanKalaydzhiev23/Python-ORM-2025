"""
#### STEPS TO SET UP SQLALCHEMY AND ALEMBIC:
1. pip install sqlalchemy
2. pip install alembic
3. pip install psycopg2-binary
4. Create DB
5. Create models file and Base class
6. alembic init alembic
7. Update target_metadata
8. Update in alembic.ini the db path
"""
from typing import List

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from helpers import handle_session
from models import Recipe, Chef

engine = create_engine(f"postgresql+psycopg2://postgres:admin@localhost/sql_alchemy")
Session = sessionmaker(bind=engine)
session = Session()


@handle_session(session)
def create_recipe(name: str, ingredients: str, instructions: str) -> None:
    new_recipe = Recipe(
        name=name,
        ingredients=ingredients,
        instructions=instructions
    )

    session.add(new_recipe)


@handle_session(session)
def update_recipe_by_name(name: str, new_name: str,  new_ingredients: str, new_instructions: str):
    session.query(Recipe).filter_by(name=name).update({
        Recipe.name: new_name,
        Recipe.ingredients: new_ingredients,
        Recipe.instructions: new_instructions,
    })

    # recipe_to_update = session.query(Recipe).filter_by(name=name).one()
    #
    # recipe_to_update.name = new_name
    # recipe_to_update.ingredients = new_ingredients
    # recipe_to_update.ingredients = new_instructions

@handle_session(session)
def delete_recipe_by_name(name: str) -> None:
    """DELETE FROM recipe WHERE name = name"""
    session.query(Recipe).filter_by(name=name).delete()


@handle_session(session, autoclose=False)
def get_recipes_by_ingredient(ingredient_name: str) -> List:
    """SELECT * FROM recipe WHERE ingredient_name IN ingredients"""
    return session.query(Recipe).filter(
        Recipe.ingredients.ilike(f"%{ingredient_name}%")
    ).all()


@handle_session(session)
def swap_recipe_ingredients_by_name(first_recipe_name: str, second_recipe_name: str) -> None:
    first_recipe = (
        session.query(Recipe)
        .filter_by(name=first_recipe_name)
        .with_for_update()
        .one()
    )
    second_recipe = (
        session.query(Recipe)
        .filter_by(name=second_recipe_name)
        .with_for_update()  # locks the records
        .one()
    )

    first_recipe.ingredients, second_recipe.ingredients = second_recipe.ingredients, first_recipe.ingredients


@handle_session(session)
def relate_recipe_with_chef_by_name(recipe_name: str, chef_name: str) -> str:
    recipe = session.query(Recipe).filter_by(name=recipe_name).one()

    if recipe.chef:
        raise Exception(f"Recipe: {recipe_name} already has a related chef")

    chef = session.query(Chef).filter_by(name=chef_name).one()
    recipe.chef = chef

    return f"Related recipe {recipe_name} with chef {chef_name}"


@handle_session(session)
def get_recipes_with_chef() -> str:
    """
    SELECT
        recipe.name,
        chef.name
    FROM
        recipe
    JOIN
        chef
    ON
        recipe.chef_id = chef.id;
    """

    recipes_with_chef = session.query(
        Recipe.name,
        Chef.name
    ).join(
        Chef, Recipe.chef
    ).all()

    return "\n".join(
        f"Recipe: {recipe_name} made by chef: {chef_name}"
        for recipe_name, chef_name in recipes_with_chef
    )
