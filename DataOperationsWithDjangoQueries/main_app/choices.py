from django.db import models


class RoomTypeChoice(models.TextChoices):
    STANDARD = "Standard", "Standard"
    DELUXE = "Deluxe", "Deluxe"
    SUITE = "Suite", "Suite"


class CharacterTypeChoices(models.TextChoices):
    MAGE = "Mage", "Mage"
    WARRIOR = "Warrior", "Warrior"
    ASSASSIN = "Assassin", "Assassin"
    SCOUT = "Scout", "Scout"
    FUSION = "Fusion", "Fusion"
