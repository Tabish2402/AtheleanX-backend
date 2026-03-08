import os

from sqlalchemy.orm import Session

from app.api.coach.schemas import CoachChatResponse
from app.models.workout import WorkoutPlan
from app.models.diet import DietPlan

AI_MODE = os.getenv("AI_MODE", "mock")



def _load_latest_context(db: Session, user_id: int) -> dict:
    """
    Load latest workout and diet plans for context.
    """
    workout = (
        db.query(WorkoutPlan)
        .filter(WorkoutPlan.user_id == user_id)
        .order_by(WorkoutPlan.created_at.desc())
        .first()
    )

    diet = (
        db.query(DietPlan)
        .filter(DietPlan.user_id == user_id)
        .order_by(DietPlan.created_at.desc())
        .first()
    )

    return {
    "has_workout": workout is not None,
    "has_diet": diet is not None,
    "injuries": workout.injuries if workout else None,
    
}


#just sample testing data here

def _mock_coach_reply(
    message: str,
    context: dict,
) -> CoachChatResponse:
    msg = message.lower()

    if "hard" in msg or "difficult" in msg:
        reply = (
            "That’s normal. You can reduce each exercise by 1 set "
            "and increase rest by 30–60 seconds. Focus on form first.It will get easier as you adapt!.ALWAYS WARM UP PROPERLY AND LISTEN TO YOUR BODY."
        )

    elif "easy" in msg:
        reply = (
            "If it feels easy, you can add 1 extra set or slow down "
            "the reps to increase time under tension.You may try to do more reps per set or reduce rest time to increase intensity."
        )

    elif "why" in msg:
        reply = (
            "Each plan is designed around your goal and experience level "
            "to ensure progress while minimizing injury risk.It balances volume and intensity to challenge you without overwhelming you."
        )

    elif "change" in msg or "modify" in msg:
        reply = (
            "You can swap similar exercises or adjust volume slightly. "
            "Let me know what you want to change specifically.But remember, consistency is key. Small adjustments are fine, but try to stick with the plan for at least a few weeks to see results."
        )

    elif not context["has_workout"] and not context["has_diet"]:
        reply = (
            "I don’t see any generated plans yet. "
            "Please generate a workout or diet plan first."
        )

    else:
        reply = (
            "I’m here to help. You can ask about difficulty, progress, "
            "or how to adjust your current plan.Kindly stick to questions related to your workout and diet plans for the best advice."
        )

    return CoachChatResponse(reply=reply)


#real ai coach

def _real_coach_reply(
    message: str,
    context: dict,
) -> CoachChatResponse:
    import os
    from dotenv import load_dotenv
    from openai import OpenAI

    # Load env safely (Windows-safe)
    load_dotenv(dotenv_path=".env", override=True)

    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL")

    if not OPENROUTER_API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY not set")

    client = OpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1",
    )

    system_prompt = """
You are an AI fitness coach for the AtheLeanX app.

Your role:
- Help users understand and follow their workout and diet plans
- Give motivation, recovery advice, and adjustment guidance
- Be concise, supportive, and practical

STRICT RULES:
- Do NOT generate new workout or diet plans
- Do NOT output JSON
- Do NOT discuss topics unrelated to fitness or nutrition
- If the user has no plans, tell them to generate one first
- Base advice only on whether plans exist, not on assumptions
-Dont use ** sign for showing bold in the reply, do use ** anywhere.
-Dont use ** in the reply, make sure you DO NOT use ** sign as used for showing bold font.
"""

    user_prompt = f"""
User message:
{message}

Context:
Has workout plan: {context["has_workout"]}
Has diet plan: {context["has_diet"]}
"""

    response = client.chat.completions.create(
        model=OPENROUTER_MODEL,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=0.6,
        max_tokens=300,
    )

    return CoachChatResponse(
        reply=response.choices[0].message.content.strip()
    )

#dispatcher func

def generate_coach_reply(
    message: str,
    db: Session,
    user_id: int,
) -> CoachChatResponse:
    context = _load_latest_context(db, user_id)

    if AI_MODE == "mock":
        return _mock_coach_reply(message, context)

    if AI_MODE in {"openai", "openrouter"}:
        return _real_coach_reply(message, context)

    raise RuntimeError(f"Invalid AI_MODE: {AI_MODE}")
