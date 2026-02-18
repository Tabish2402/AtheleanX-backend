from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.models.coach import CoachMessage
from app.api.coach.schemas import (
    CoachChatRequest,
    CoachChatResponse,
    CoachMessageItem,
)
from app.ai.coach import generate_coach_reply
from app.dependencies.auth import get_current_user
from app.db.database import get_db
from app.models.user import User

router = APIRouter(
    prefix="/coach",
    tags=["coach"],
)

@router.post(
    "/chat",
    response_model=CoachChatResponse,
    status_code=status.HTTP_200_OK,
)
def coach_chat(
    payload: CoachChatRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    AI Coach chat endpoint.
    Saves user + assistant messages.
    """

    # 1️⃣ Save USER message
    user_msg = CoachMessage(
        user_id=current_user.id,
        role="user",
        content=payload.message,
    )
    db.add(user_msg)
    db.commit()

    # 2️⃣ Generate AI reply
    reply = generate_coach_reply(
        message=payload.message,
        db=db,
        user_id=current_user.id,
    )

    # 3️⃣ Save ASSISTANT reply
    assistant_msg = CoachMessage(
        user_id=current_user.id,
        role="assistant",
        content=reply.reply,
    )
    db.add(assistant_msg)
    db.commit()

    # 4️⃣ Return reply
    return reply
@router.get(
    "/history",
    response_model=list[CoachMessageItem],
    status_code=status.HTTP_200_OK,
)
def get_coach_history(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Return full AI coach chat history for the current user.
    """

    messages = (
        db.query(CoachMessage)
        .filter(CoachMessage.user_id == current_user.id)
        .order_by(CoachMessage.created_at.asc())
        .all()
    )

    return [
    CoachMessageItem(role=msg.role, content=msg.content)
    for msg in messages
]
  
