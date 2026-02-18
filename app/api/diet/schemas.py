from pydantic import BaseModel, Field
from typing import List, Literal


# -------- INPUT SCHEMA (Frontend → Backend) --------

class DietGenerateRequest(BaseModel):
    goal: Literal["fat_loss", "muscle_gain", "maintenance"]
    diet_type: Literal["vegetarian", "non_vegetarian", "vegan"]
    meals_per_day: int = Field(ge=3, le=6)
    calorie_target: int = Field(ge=1200, le=4000)
    allergies: List[str] = []


# -------- OUTPUT SCHEMA (AI → Backend → Frontend) --------

class MealItem(BaseModel):
    name: str
    calories: int
    protein: str


class Meal(BaseModel):
    meal: str  # Breakfast, Lunch, Dinner, Snack
    items: List[MealItem]


class DietPlanResponse(BaseModel):
    meals: List[Meal]
