import uuid
from datetime import datetime
from typing import List, Optional
from zoneinfo import ZoneInfo

import motor.motor_asyncio
from beanie import Document, Indexed
from pydantic import BaseModel, validator

from api.consumable.schemas import Category


class Consumable(Document):
    user_id: Optional[uuid.UUID] = None
    name: str
    description: Optional[str] = None
    category: Optional[Category] = None
    favorite: bool = False
    consumed_at: datetime
    ingredients: Optional[List[str]] = None

    @validator("name", "description", "category", pre=True)
    def convert_to_lowercase(cls, value):
        """
        A validator function that converts the specified fields to lowercase.
        """

        if value is not None and isinstance(value, str):
            return value.lower()
        return value

    @validator("ingredients", pre=True)
    def convert_ingredients_to_lowercase(cls, ingredients):
        """
        A validator function that converts the specified fields to lowercase.
        """

        if ingredients is not None:
            return [ingredient.lower() for ingredient in ingredients]
        return ingredients

    @validator("consumed_at")
    def validate_consumed_at(cls, value):
        """
        A validator function that converts the consumed_at field to UTC.
        """

        if value.tzinfo is None:
            value = value.replace(tzinfo=ZoneInfo("UTC"))
        else:
            value = value.astimezone(ZoneInfo("UTC"))
        return value

    class Config:
        schema_extra = {
            "example": {
                "name": "Keto Breakfast",
                "description": "3 eggs with 6 slices of bacon and side of tomatoes",
                "category": "breakfast",
                "favorite": False,
                "consumed_at": datetime.now().replace(microsecond=0),
                "ingredients": ["Eggs", "Bacon", "Tomatoes"],
            }
        }

    class Settings:
        name = "consumable"
