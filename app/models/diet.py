from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship
from datetime import datetime

from app.db.base import Base


class DietPlan(Base):
    __tablename__ = "diet_plans"

    id = Column(Integer, primary_key=True, index=True)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    goal = Column(String, nullable=False)
    diet_type = Column(String, nullable=False)
    meals_per_day = Column(Integer, nullable=False)
    calorie_target = Column(Integer, nullable=False)
    allergies = Column(JSONB, nullable=False)

    plan_json = Column(JSONB, nullable=False)

    created_at = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", backref="diet_plans")
