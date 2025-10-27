import os
import time

import django
from typing import List

from django.db.models import Case, When, Value, F, TextField, CharField

from main_app.choices import LaptopOSChoices, LaptopBrandChoices, MealTypeChoice, DungeonDifficultyChoice,     WorkoutDifficultyChoice, WorkoutTypeChoice

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from populate_db import populate_model_with_data
from main_app.models import ArtworkGallery, Laptop, ChessPlayer, Meal, Dungeon, Workout

"""
SELECT * FROM artwork_gallery
ORDER BY rating DESC, id ASC
LIMIT 1;
"""
def show_highest_rated_art() -> str:
    highest_rated_art = ArtworkGallery.objects.order_by('-rating', 'id').first()
    # If no result returns None
    return f"{highest_rated_art.art_name} is the highest-rated art with a {highest_rated_art.rating} rating!"


"""
INSERT INTO
    artwork_gallery(...)
VALUES 
    (...),
    (...);
"""
def bulk_create_arts(first_art: ArtworkGallery, second_art: ArtworkGallery) -> None:
    ArtworkGallery.objects.bulk_create([
        first_art,
        second_art,
    ])


"""
DELETE FROM artwork_gallery
WHERE rating < 0;
"""
def delete_negative_rated_arts() -> None:
    ArtworkGallery.objects.filter(rating__lt=0).delete()


def show_the_most_expensive_laptop() -> str:
    laptop = Laptop.objects.order_by('-price', '-id').first()
    return f"{laptop.brand} is the most expensive laptop available for {laptop.price}$!"

def bulk_create_laptops(args: List[Laptop]):
    Laptop.objects.bulk_create(args)


"""
UPDATE laptop
SET storage = 512
WHERE brand IN ('Asus', 'Lenovo');
"""
def update_to_512_GB_storage() -> None:
    Laptop.objects.filter(brand__in=['Asus', 'Lenovo']).update(storage=512)

def update_to_16_GB_memory() -> None:
    Laptop.objects.filter(brand__in=['Acer', 'Dell', 'Apple']).update(memory=16)



# Option 1:
"""
UPDATE laptop
SET operation_system = value
WHERE brand = 'Some value'; -- x 4
"""

# Option 2:
"""
UPDATE laptop
SET operation_system = CASE
    WHEN brand = 'Asus' THEN 'Windows'
    ...
END;
"""
def update_operation_systems() -> None:
    # Option 2:
    Laptop.objects.update(
        operation_system=Case(
            When(brand=LaptopBrandChoices.ASUS, then=Value(LaptopOSChoices.WINDOWS)),
            When(brand=LaptopBrandChoices.APPLE, then=Value(LaptopOSChoices.MAC_OS)),
            When(brand=LaptopBrandChoices.LENOVO, then=Value(LaptopOSChoices.CHROME_OS)),
            When(brand__in=[
                    LaptopBrandChoices.DELL, LaptopBrandChoices.ACER
                ], then=Value(LaptopOSChoices.LINUX)
            ),
        )
    )

    # Option 3:  worst
    # for laptop in Laptop.objects.all():
    #     if laptop.brand == LaptopBrandChoices.ASUS:
    #         laptop.operation_system = LaptopOSChoices.WINDOWS
    #     elif laptop.brand == LaptopBrandChoices.APPLE:
    #         laptop.operation_system = LaptopOSChoices.MAC_OS
    #     elif laptop.brand == LaptopBrandChoices.LENOVO:
    #         laptop.operation_system = LaptopOSChoices.CHROME_OS
    #     elif laptop.brand in [LaptopBrandChoices.ACER, LaptopBrandChoices.DELL]:
    #         laptop.operation_system = LaptopOSChoices.LINUX
    # 
    #     laptop.save() 


    # Option 1:
    # Laptop.objects.filter(brand='Asus').update(operation_system=LaptopOSChoices.WINDOWS)
    # Laptop.objects.filter(brand='Apple').update(operation_system=LaptopOSChoices.MAC_OS)
    # Laptop.objects.filter(brand='Lenovo').update(operation_system=LaptopOSChoices.CHROME_OS)
    # Laptop.objects.filter(brand__in=['Dell', 'Acer']).update(operation_system=LaptopOSChoices.LINUX)


def delete_inexpensive_laptops() -> None:
    Laptop.objects.filter(price__lt=1200).delete()


def bulk_create_chess_players(args: List[ChessPlayer]) -> None:
    ChessPlayer.objects.bulk_create(args)


def delete_chess_players() -> None:
    ChessPlayer.objects.filter(title="no title").delete()


def change_chess_games_won() -> None:
    ChessPlayer.objects.filter(title="GM").update(games_won=30)

def change_chess_games_drawn() -> None:
    ChessPlayer.objects.update(games_drawn=10)

def change_chess_games_lost() -> None:
    ChessPlayer.objects.filter(title="no title").update(games_lost=25)


"""
UPDATE chess_player
SET title = 'GM'
WHERE rating >= 2400;
"""
def grand_chess_title_GM() -> None:
    ChessPlayer.objects.filter(rating__gte=2400).update(title='GM')


"""
UPDATE chess_player
SET title = 'IM'
WHERE rating BETWEEN 2300 AND 2399;
"""
def grand_chess_title_IM() -> None:
    ChessPlayer.objects.filter(rating__range=[2300, 2399]).update(title='IM')

def grand_chess_title_FM() -> None:
    ChessPlayer.objects.filter(rating__range=[2200, 2299]).update(title='FM')

def grand_chess_title_regular_player() -> None:
    ChessPlayer.objects.filter(rating__range=[0, 2199]).update(title='regular player')

def set_new_chefs() -> None:
    # Option 2: best
    Meal.objects.update(
        chef=Case(
            When(meal_type=MealTypeChoice.BREAKFAST, then=Value("Gordon Ramsay")),
            When(meal_type=MealTypeChoice.LUNCH, then=Value("Julia Child")),
            When(meal_type=MealTypeChoice.DINNER, then=Value("Jamie Oliver")),
            When(meal_type=MealTypeChoice.SNACK, then=Value("Thomas Keller")),
        )
    )

    # Option 1: not so bad
    # Meal.objects.filter(meal_type=MealTypeChoice.BREAKFAST).update(chef="Gordon Ramsay")
    # Meal.objects.filter(meal_type=MealTypeChoice.LUNCH).update(chef="Julia Child")
    # Meal.objects.filter(meal_type=MealTypeChoice.DINNER).update(chef="Jamie Oliver")
    # Meal.objects.filter(meal_type=MealTypeChoice.SNACK).update(chef="Thomas Keller")


def set_new_preparation_times() -> None:
    Meal.objects.update(
        preparation_time=Case(
            When(meal_type=MealTypeChoice.BREAKFAST, then=Value("10 minutes")),
            When(meal_type=MealTypeChoice.LUNCH, then=Value("12 minutes")),
            When(meal_type=MealTypeChoice.DINNER, then=Value("15 minutes")),
            When(meal_type=MealTypeChoice.SNACK, then=Value("5 minutes")),
        )
    )

"""
UPDATE meals
SET calories = 400
WHERE meal_type IN ['Breakfast', 'Dinner'];
"""
def update_low_calorie_meals() -> None:
    Meal.objects.filter(
        meal_type__in=[MealTypeChoice.BREAKFAST, MealTypeChoice.DINNER],
    ).update(
        calories=400,
    )


def update_high_calorie_meals() -> None:
    Meal.objects.filter(
        meal_type__in=[MealTypeChoice.LUNCH, MealTypeChoice.SNACK],
    ).update(
        calories=700,
    )


def delete_lunch_and_snack_meals() -> None:
    Meal.objects.filter(
        meal_type__in=[MealTypeChoice.LUNCH, MealTypeChoice.SNACK]
    ).delete()


"""
SELECT * FROM dungeons
WHERE difficulty = 'Hard'
ORDER BY location DESC;
"""
def show_hard_dungeons() -> str:
    hard_dungeons = Dungeon.objects.filter(
        difficulty=DungeonDifficultyChoice.HARD
    ).order_by('-location')

    return '\n'.join(
        f"{d.name} is guarded by {d.boss_name} who has {d.boss_health} health points!"
        for d in hard_dungeons
    )


def bulk_create_dungeons(args: List[Dungeon]) -> None:
    Dungeon.objects.bulk_create(args)


"""
UPDATE dungeon
SET boss_health = 500
WHERE difficulty != 'Easy';
"""
def update_dungeon_bosses_health() -> None:
    Dungeon.objects.exclude(
        difficulty=DungeonDifficultyChoice.EASY
    ).update(boss_health=500)

def update_dungeon_recommended_levels() -> None:
    Dungeon.objects.update(
        recommended_level=Case(
            When(difficulty=DungeonDifficultyChoice.EASY, then=Value(25)),
            When(difficulty=DungeonDifficultyChoice.MEDIUM, then=Value(50)),
            When(difficulty=DungeonDifficultyChoice.HARD, then=Value(75)),
            default=F('recommended_level'),
            output_field=CharField()
        )
    )


"""
UPDATE "main_app_dungeon" 
SET "reward" = CASE 
    WHEN ("main_app_dungeon"."boss_health" = 500) THEN '1000 Gold' 
    WHEN ("main_app_dungeon"."location" LIKE 'E%') THEN 'New dungeon unlocked' 
    WHEN ("main_app_dungeon"."location" LIKE '%s') THEN 'Dragonheart Amulet' 
    ELSE "main_app_dungeon"."reward" 
END;
"""
def update_dungeon_rewards() -> None:
    Dungeon.objects.update(
        reward=Case(
            When(boss_health=500, then=Value("1000 Gold")),
            When(location__startswith="E", then=Value("New dungeon unlocked")),
            When(location__endswith="s", then=Value("Dragonheart Amulet")),
            default=F('reward'),
            output_field=TextField()
        )
    )


def set_new_locations() -> None:
    Dungeon.objects.update(
        location=Case(
            When(recommended_level=25, then=Value("Enchanted Maze")),
            When(recommended_level=50, then=Value("Grimstone Mines")),
            When(recommended_level=75, then=Value("Shadowed Abyss")),
            default=F('location'),
            output_field=CharField()
        )
    )


"""
SELECT * FROM workout
WHERE
    difficulty = 'Hard' AND workout_type = 'Cardio'
"""
def get_high_difficulty_cardio_workouts() -> None:
    Workout.objects.filter(
        difficulty=WorkoutDifficultyChoice.HARD,
        workout_type=WorkoutTypeChoice.CARDIO,
    ).order_by('instructor')

def show_workouts() -> str:
    workouts = Workout.objects.filter(
        workout_type__in=[
            WorkoutTypeChoice.CALISTHENICS, 
            WorkoutTypeChoice.CROSSFIT
        ]
    ).order_by('id')

    return "\n".join(
        f"{w.name} from {w.workout_type} type has {w.difficulty} difficulty!"
        for w in workouts
    )

def delete_workouts() -> None:
    Workout.objects.exclude(workout_type__in=[
        WorkoutTypeChoice.CALISTHENICS,
        WorkoutTypeChoice.STRENGTH,
    ]).delete()

def set_new_instructors() -> None:
    Workout.objects.update(
        instructor=Case(
            When(workout_type=WorkoutTypeChoice.CARDIO, then=Value("John Smith")),
            When(workout_type=WorkoutTypeChoice.STRENGTH, then=Value("Michael Williams")),
            When(workout_type=WorkoutTypeChoice.YOGA, then=Value("Emily Johnson")),
            When(workout_type=WorkoutTypeChoice.CROSSFIT, then=Value("Sarah Davis")),
            When(workout_type=WorkoutTypeChoice.CALISTHENICS, then=Value("Chris Heria")),
        )
    )

def set_new_duration_times() -> None:
    Workout.objects.update(
        duration=Case(
            When(instructor="John Smith", then=Value("15 minutes")),
            When(instructor="Sarah Davis", then=Value("30 minutes")),
            When(instructor="Chris Heria", then=Value("45 minutes")),
            When(instructor="Michael Williams", then=Value("1 hour")),
            When(instructor="Emily Johnson", then=Value("1 hour and 30 minutes")),
        )
    )
