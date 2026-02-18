from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api.diet.schemas import (
    DietGenerateRequest,
    DietPlanResponse,
)
from app.ai.diet import generate_diet_plan
from app.dependencies.auth import get_current_user
from app.db.database import get_db
from app.models.user import User
from app.models.diet import DietPlan

router = APIRouter(
    prefix="/generate",
    tags=["diet"],
)


@router.post(
    "/diet",
    response_model=DietPlanResponse,
    status_code=status.HTTP_201_CREATED,
)
def generate_diet(
    payload: DietGenerateRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Generate a diet plan using AI (mock or real),
    persist it, and return the structured result.
    """

    try:
        diet_plan = generate_diet_plan(payload)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e),
        )

    # Persist to DB
    db_plan = DietPlan(
        user_id=current_user.id,
        goal=payload.goal,
        diet_type=payload.diet_type,
        meals_per_day=payload.meals_per_day,
        calorie_target=payload.calorie_target,
        allergies=payload.allergies,
        plan_json=diet_plan.model_dump(),
    )

    db.add(db_plan)
    db.commit()
    db.refresh(db_plan)

    return diet_plan
@router.get(
    "/diet/latest",
    response_model=DietPlanResponse,
)
def get_latest_diet(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    diet = (
        db.query(DietPlan)
        .filter(DietPlan.user_id == current_user.id)
        .order_by(DietPlan.created_at.desc())
        .first()
    )

    if not diet:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No diet plan found",
        )

    return diet.plan_json

