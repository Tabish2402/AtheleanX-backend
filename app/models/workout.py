from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from datetime import datetime


from app.db.base import Base


class WorkoutPlan(Base):
    __tablename__ = "workout_plans"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    goal = Column(String, nullable=False)
    experience = Column(String, nullable=False)
    days_per_week = Column(Integer, nullable=False)
    equipment = Column(String, nullable=False)
    injuries = Column(JSONB, nullable=False)

    plan_json = Column(JSONB, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    # relationship back to user
    user = relationship("User", backref="workout_plans")
