
import os
import json
from dotenv import load_dotenv
from openai import OpenAI

from app.api.workout.schemas import (
    WorkoutGenerateRequest,
    WorkoutPlanResponse,
    WorkoutDay,
    Exercise,
)

#configuration

AI_MODE = os.getenv("AI_MODE", "mock")  # mock | openrouter 

load_dotenv(dotenv_path=".env", override=True)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")



SYSTEM_PROMPT = """
You are a fitness expert and personal trainer. Your task is to create personalized workout plans based strictly on user input.

RULES:
1. Output must be valid json that strictly adheres to the WorkoutPlanResponse schema.
2. Do not include any explanations or text outside of the json response.
3. The workout plan should be based strictly on the user input and should not make any assumptions beyond the provided information.
4. Ensure user safety by not recommending any exercises that could be harmful based on the user's injuries or experience level.
5. For the "reps" field, you can use a range (e.g. "8-12") or a specific number (e.g. "10"). For the "rest" field, you can specify time in seconds (e.g. "60s") or a general guideline (e.g. "1-2 minutes").
6. The workout plan should be balanced and target different muscle groups throughout the week.
7. Equipment rules:
   - bodyweight → bodyweight exercises
   - dumbbells → dumbbell exercises
   - gym → full gym exercises
8. Experience rules:
   - beginner → simple movements, lower volume
   - intermediate/advanced → higher volume, more complexity
9. Goal rules:
   - fat_loss → higher reps, shorter rest
   - muscle_gain → moderate reps/rest
   - strength → low reps, long rest,much heavier weights
"""

#genai implementation
import os
import json
from dotenv import load_dotenv
from openai import OpenAI

from app.api.workout.schemas import (
    WorkoutGenerateRequest,
    WorkoutPlanResponse,
)

# ensure env vars are loaded (windows-safe)
load_dotenv(dotenv_path=".env", override=True)

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")

SYSTEM_PROMPT = """
You are a fitness expert and personal trainer. Your task is to create personalized workout plans based strictly on user input.
You MUST return JSON that EXACTLY matches this schema, change the numerical value according to the plan:
{
  "days": [
    {
      "day": 1,
      "focus": "string",
      "exercises": [
        {
          "name": "string",
          "sets": 3,
          "reps": "string",
          "rest": "string"
        }
      ]
    }
  ]
}
RULES:
1. Output must be valid JSON that strictly adheres to the WorkoutPlanResponse schema.
2. Do not include any explanations or text outside of the JSON response.
3. The workout plan should be based strictly on the user input and should not make assumptions beyond the provided information.
4. Ensure user safety based on injuries and experience level.
5. Reps can be ranges (e.g. "8-12"), rest can be seconds or minutes.
6. Balance muscle groups across the week.A minimum of four exercies each day and maximum of 6 depending upon begginer,intermidiate or advanced level.

7. Equipment rules:
   - bodyweight → bodyweight exercises
   - dumbbells → dumbbell exercises
   - gym → full gym exercises
8. Experience rules:
   - beginner → simple movements, lower volume
   - intermediate/advanced → higher volume
9. Goal rules:
   - fat_loss → higher reps, shorter rest
   - muscle_gain → moderate reps/rest
   - strength → low reps, long rest
- Generate EXACTLY days per week asked workout days.
- Do NOT generate more days than requested.

"""

def _real_generate_workout_plan(
    data: WorkoutGenerateRequest,
) -> WorkoutPlanResponse:
    if not OPENROUTER_API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY not set")

    client = OpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1",
    )

    user_prompt = f"""
Generate a workout plan using ONLY the following inputs.

Goal: {data.goal}
Experience: {data.experience}
Days per week: {data.days_per_week}
Equipment: {data.equipment}
Injuries: {", ".join(data.injuries) if data.injuries else "None"}

Return ONLY valid JSON. No markdown. No explanation.
"""

    last_error = None

    for attempt in range(1):  # retry once if JSON invalid
        response = client.chat.completions.create(
            model=OPENROUTER_MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.2,
            max_tokens=1200,
        )

        raw = response.choices[0].message.content.strip()
        raw = response.choices[0].message.content

        print("========== RAW LLM OUTPUT ==========")   
        print(raw)
        print("====================================")
    
        
    
    
        try:
            parsed = json.loads(raw)
            return WorkoutPlanResponse(**parsed)

        except Exception as e:
            last_error = e
            user_prompt += "\nREMINDER: OUTPUT MUST BE VALID JSON ONLY."

    raise ValueError(f"Invalid workout plan from OpenRouter: {last_error}")


#the mock data i created to save free tokens during development. It generates a simple workout plan based on the input parameters without calling the AI API. This allows us to test the full flow of the application without incurring costs or hitting rate limits on the AI service.

def _mock_generate_workout_plan(
    data: WorkoutGenerateRequest,
) -> WorkoutPlanResponse:
    days = []

    for day in range(1, data.days_per_week + 1):
        if data.goal == "fat_loss":
            focus = "Full Body Fat Loss"
            exercises = [
                Exercise(name="Jump Squats", sets=3, reps="12-15", rest="45s"),
                Exercise(name="Push-ups", sets=3, reps="10-12", rest="45s"),
                Exercise(name="Mountain Climbers", sets=3, reps="30s", rest="30s"),
            ]
        elif data.goal == "muscle_gain":
            focus = "Hypertrophy"
            exercises = [
                Exercise(name="Goblet Squats", sets=4, reps="8-10", rest="90s"),
                Exercise(name="Dumbbell Bench Press", sets=4, reps="8-10", rest="90s"),
                Exercise(name="Dumbbell Rows", sets=3, reps="10-12", rest="75s"),
            ]
        else:  # strength
            focus = "Strength Training"
            exercises = [
                Exercise(name="Deadlift", sets=5, reps="5", rest="2-3 min"),
                Exercise(name="Squat", sets=5, reps="5", rest="2-3 min"),
                Exercise(name="Overhead Press", sets=3, reps="5", rest="2 min"),
            ]

        days.append(
            WorkoutDay(
                day=day,
                focus=focus,
                exercises=exercises,
            )
        )

    return WorkoutPlanResponse(days=days)

# very imp. the switch from mock to genai

def generate_workout_plan(
    data: WorkoutGenerateRequest,
) -> WorkoutPlanResponse:
    """
    Central AI entrypoint.
    Switches between mock and real AI using AI_MODE.
    """

    if AI_MODE == "mock":
        return _mock_generate_workout_plan(data)

    if AI_MODE in {"openai", "openrouter"}:
        return _real_generate_workout_plan(data)

    raise RuntimeError(f"Invalid AI_MODE: {AI_MODE}")


