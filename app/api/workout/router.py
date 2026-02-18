from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.workout.schemas import (
    WorkoutGenerateRequest,
    WorkoutPlanResponse,
)
from app.ai.workout import generate_workout_plan
from app.dependencies.auth import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.models.workout import WorkoutPlan

router = APIRouter(
    prefix="/generate",
    tags=["workout"],
)


@router.post(
    "/workout",
    response_model=WorkoutPlanResponse,
    status_code=status.HTTP_201_CREATED,
)
def generate_workout(
    payload: WorkoutGenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Generate a workout plan using AI (mock or real),
    persist it, and return the structured result.
    """

    try:
        workout_plan = generate_workout_plan(payload)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

    # Persist to DB
    db_plan = WorkoutPlan(
        user_id=current_user.id,
        goal=payload.goal,
        experience=payload.experience,
        days_per_week=payload.days_per_week,
        equipment=payload.equipment,
        injuries=payload.injuries,
        plan_json=workout_plan.model_dump(),
    )

    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)

    return workout_plan
@router.get(
    "/workout/latest",
    response_model=WorkoutPlanResponse,
)
def get_latest_workout(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    workout = (
        db.query(WorkoutPlan)
        .filter(WorkoutPlan.user_id == current_user.id)
        .order_by(WorkoutPlan.created_at.desc())
        .first()
    )

    if not workout:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No workout plan found",
        )

    return workout.plan_json
