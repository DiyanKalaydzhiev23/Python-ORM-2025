from sqlalchemy import Column, Integer, String, Text, false, ForeignKey
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()  # same as models.Model


class Recipe(Base):
    __tablename__ = 'recipes'

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
        ForeignKey('chefs.id')
    )

    chef = relationship(
        "Chef",
        back_populates="recipes"
    )



class Chef(Base):
    __tablename__ = 'chefs'

    id = Column(
        Integer,
        primary_key=True,
    )

    name = Column(
        String,
        nullable=False,
    )

    recipes = relationship(
        "Recipe",
        back_populates="chef",
    )

