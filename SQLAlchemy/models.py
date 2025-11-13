from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()  # the equivalent of models.Model


class Recipe(Base):
    __tablename__ = "recipe"

    id = Column(
        Integer,
        primary_key=True,
    )

    name = Column(
        String,
        nullable=False,
    )

    ingredients = Column(
        Text,
        nullable=False,
    )

    instructions = Column(
        Text,
        nullable=False,
    )

    chef_id = Column(
        Integer,
        ForeignKey('chef.id')
    )

    chef = relationship(
        "Chef",
        back_populates="recipies",
    )


class Chef(Base):
    __tablename__ = "chef"

    id = Column(
        Integer,
        primary_key=True,
    )

    name = Column(
        String,
        nullable=False,
    )

    recipies = relationship(
        "Recipe",
        back_populates="chef",  # the same thing as related_name in Django
    )
