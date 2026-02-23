from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.workout.router import router as workout_router
from app.api.diet.router import router as diet_router
from app.api.coach.router import router as coach_router

from app.api.auth.router import router as auth_router
app = FastAPI(
    title=settings.APP_NAME
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://athelean-x-frontend-4qllwsmun-tabish-riyazs-projects.vercel.app",
],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["Authorization", "Content-Type"],
)


app.include_router(coach_router)
app.include_router(auth_router)
app.include_router(workout_router)
app.include_router(diet_router)

