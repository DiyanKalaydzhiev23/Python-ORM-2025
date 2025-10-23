import os
from decimal import Decimal
from typing import Optional

import django

from main_app.choices import RoomTypeChoice, CharacterTypeChoices

# Set up Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "orm_skeleton.settings")
django.setup()

from django.db.models import QuerySet, Case, When, F, Value
from populate_db import populate_model_with_data
from main_app.models import Pet, Artifact, Location, Car, Task, HotelRoom, Character


def create_pet(name: str, species: str) -> str:
    """
    INSERT INTO
        pets("name", "species")
    VALUES
        (name, species)
    RETURNING *;
    """
    pet = Pet.objects.create(
        name=name,
        species=species
    )

    return f"{pet.name} is a very cute {pet.species}!"


def create_artifact(
    name: str,
    origin: str,
    age: int,
    description: str,
    is_magical: bool
) -> str:
    artifact = Artifact.objects.create(
        name=name,
        origin=origin,
        age=age,
        description=description,
        is_magical=is_magical,
    )

    return f"The artifact {artifact.name} is {artifact.age} years old!"


def rename_artifact(artifact: Artifact, new_name: str) -> None:
    """
    UPDATE artifacts
    SET name = new_name
    WHERE id = artifact.id;
    """

    if artifact.age > 250 and artifact.is_magical:
        artifact.name = new_name
        artifact.save()


def delete_all_artifacts() -> None:
    """
    DELETE FROM artifacts;
    """
    Artifact.objects.all().delete()


def show_all_locations() -> str:
    """
    SELECT * FROM locations
    ORDER BY id DESC;
    """

    locations = Location.objects.all().order_by('-id')

    return '\n'.join(f"{l.name} has a population of {l.population}!" for l in locations)


def new_capital() -> None:
    """
    Option: 1
    SELECT * FROM locations
    LIMIT 1;

    UPDATE locations
    SET is_capital = True
    WHERE id = some_id;

    ---
    """

    # Option: 1
    first_location = Location.objects.first()
    first_location.is_capital = True
    first_location.save()

    # Option: 2
    # Location.objects.filter(pk=Location.objects.first().id).update(is_capital=True)


def get_capitals() -> QuerySet:
    """
    SELECT * FROM locations WHERE is_capital = True;
    """
    return Location.objects.filter(is_capital=True)


def delete_first_location() -> None:
    Location.objects.first().delete()


def apply_discount() -> None:
    """
    Option 1:
    SELECT * FROM cars;

    FOR LOOP
        INSERT cars ...
    """

    for car in Car.objects.all():
        # 2008 -> "2008" -> '2' -> 2 + ... -> 10 / 100 -> 0.10
        percentage_off = Decimal(str(sum(int(d) for d in str(car.year)) / 100))
        discount = car.price * percentage_off  # 1000 * 0.10 -> 100
        car.price_with_discount = car.price - discount
        car.save()


    # Option 2: where cars is a list
    # Car.objects.bulk_update(cars, ['price_with_discount'])

    # Option 3: Get rid of the python for loop


def get_recent_cars() -> QuerySet:
    """
    SELECT model, price_with_discount FROM cars WHERE year > 2020;
    """
    return Car.objects.filter(year__gt=2020).values('model', 'price_with_discount')


def delete_last_car() -> None:
    """
    SELECT * FROM cars ORDER BY id DESC LIMIT 1;

    DELETE FROM cars
    WHERE id = last_car_id;
    """
    Car.objects.last().delete()


def show_unfinished_tasks() -> str:
    """
    SELECT * FROM tasks WHERE NOT is_finished;
    """
    tasks = Task.objects.filter(is_finished=False)

    return '\n'.join(
        f"Task - {t.title} needs to be done until {t.due_date}!"
        for t in tasks
    )


def complete_odd_tasks() -> None:
    # TODO: research how to do it in a better way with only 1 query
    tasks = Task.objects.all()
    completed_tasks = []

    for t in tasks:
        if t.id % 2 != 0:
            t.is_finished = True
            completed_tasks.append(t)

    Task.objects.bulk_update(completed_tasks, ['is_finished'])


def encode_and_replace(text: str, task_title: str) -> None:
    encoded_text = ''.join(chr(ord(l) - 3) for l in text)

    # Option 1: python loop -> worst
    for task in Task.objects.filter(title=task_title):
        task.description = encoded_text
        task.save()

    # Option 2: bulk update (look up previous func) -> slightly better
    # Option 3: direct update -> best ->
    # UPDATE tasks SET description = encoded_text WHERE title = task_title
    Task.objects.filter(title=task_title).update(description=encoded_text)


def get_deluxe_rooms() -> str:
    rooms = HotelRoom.objects.filter(room_type=RoomTypeChoice.DELUXE)
    even_id_rooms = [r for r in rooms if r.id % 2 == 0]  # TODO: do it in the filter

    return '\n'.join(
        f"Deluxe room with number {r.room_number} costs {r.price_per_night}$ per night!"
        for r in even_id_rooms
    )


def increase_room_capacity() -> None:
    reserved_rooms = HotelRoom.objects.filter(is_reserved=True).order_by('id')
    previous_room: Optional[HotelRoom] = None

    for r in reserved_rooms:
        if previous_room:
            r.capacity += previous_room.capacity
        else:
            r.capacity += r.id

        previous_room = r
        r.save()


def reserve_first_room() -> None:
    first_room = HotelRoom.objects.first()
    first_room.is_reserved = True
    first_room.save()


def delete_last_room() -> None:
    room = HotelRoom.objects.last()

    if not room.is_reserved:
        room.delete()


def update_characters() -> None:
    """
    UPDATE characters
    SET
        level = CASE
            WHEN class_name = 'Mage' THEN level + 3
            ELSE level
        END
        intelligence = CASE ... END
    """

    Character.objects.update(
        level=Case(
            When(class_name='Mage', then=F('level') + 3),
            default=F('level')
        ),
        intelligence=Case(
            When(class_name='Mage', then=F('intelligence') - 7),
            default=F('intelligence')
        ),
        hit_points=Case(
            When(class_name='Warrior', then=F('hit_points') / 2),
            default=F('hit_points')
        ),
        dexterity=Case(
            When(class_name='Warrior', then=F('dexterity') + 4),
            default=F('dexterity')
        ),
        inventory=Case(
            When(class_name__in=['Assassin', 'Scout'], then=Value('The inventory is empty')),
            default=F('inventory')
        )
    )


def fuse_characters(first_character: Character, second_character: Character) -> None:
    inventory = None

    if first_character.class_name in [CharacterTypeChoices.MAGE, CharacterTypeChoices.SCOUT]:
        inventory = "Bow of the Elven Lords, Amulet of Eternal Wisdom"
    elif first_character.class_name in [CharacterTypeChoices.WARRIOR, CharacterTypeChoices.ASSASSIN]:
        inventory = "Dragon Scale Armor, Excalibur"

    Character.objects.create(
        name=first_character.name + ' ' + second_character.name,
        class_name=CharacterTypeChoices.FUSION,
        level=(first_character.level + second_character.level) // 2,
        strength=(first_character.strength + second_character.strength) * 1.2,
        dexterity=(first_character.dexterity + second_character.dexterity) * 1.4,
        intelligence=(first_character.intelligence + second_character.intelligence) * 1.5,
        hit_points=(first_character.hit_points + second_character.hit_points),
        inventory=inventory
    )

    first_character.delete()
    second_character.delete()


def grand_dexterity() -> None:
    """
    UPDATE main_app_character
    SET dexterity = 30;
    """
    Character.objects.update(dexterity=30)


def grand_intelligence() -> None:
    Character.objects.update(intelligence=40)


def grand_strength() -> None:
    Character.objects.update(strength=50)


def delete_characters() -> None:
    """
    DELETE FROM main_app_character WHERE inventory = 'The inventory is empty';
    """
    Character.objects.filter(inventory='The inventory is empty').delete()
