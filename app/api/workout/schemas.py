from pydantic import BaseModel, Field
from typing import List, Literal




class WorkoutGenerateRequest(BaseModel):
    goal: Literal["fat_loss", "muscle_gain", "strength"]
    experience: Literal["beginner", "intermediate", "advanced"]
    days_per_week: int = Field(ge=3, le=6)
    equipment: Literal["bodyweight", "dumbbells", "gym"]
    injuries: List[str] = []



class Exercise(BaseModel):
    name: str
    sets: int
    reps: str
    rest: str


class WorkoutDay(BaseModel):
    day: int
    focus: str
    exercises: List[Exercise]


class WorkoutPlanResponse(BaseModel):
    days: List[WorkoutDay]
