from datetime import datetime
from enum import Enum
from typing import List, Optional

from beanie import PydanticObjectId
from pydantic import BaseModel


class Category(Enum):
    BREAKFAST = "breakfast"
    LUNCH = "lunch"
    DINNER = "dinner"
    SNACK = "snack"
    DRINK = "drink"
