import os
import json
from typing import List
from dotenv import load_dotenv
from openai import OpenAI
from app.api.diet.schemas import (
    DietGenerateRequest,
    DietPlanResponse,
    Meal,
    MealItem,
)


AI_MODE = os.getenv("AI_MODE", "mock")  # mock | openrouter | openai





def _real_generate_diet_plan(
    data: DietGenerateRequest,
) -> DietPlanResponse:
    import os
    import json
    from dotenv import load_dotenv
    from openai import OpenAI

   
    load_dotenv(dotenv_path=".env", override=True)

    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
    OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")

    if not OPENROUTER_API_KEY:
        raise RuntimeError("OPENROUTER_API_KEY not set")

    client = OpenAI(
        api_key=OPENROUTER_API_KEY,
        base_url="https://openrouter.ai/api/v1",
    )

    SYSTEM_PROMPT = """
You are a certified nutritionist.

You MUST return JSON that EXACTLY matches this schema:

{
  "meals": [
    {
      "meal": "Breakfast",
      "items": [
        {
          "name": "Food item name",
          "calories": 300,
          "protein": "20g"
        }
      ]
    }
  ]
}

STRICT RULES:
- Output ONLY JSON
- Do NOT wrap the response in another object
- Top-level key MUST be "meals"
- Generate EXACTLY the number of meals requested
- Do NOT generate extra meals
- Each meal MUST contain at least one item
- Each item MUST include: name, calories (int), protein (string)
- Respect calorie target across all meals combined
- Respect diet type and allergies
- Do NOT include explanations, totals, or metadata
- The diet should strictly be Indian, this app is sprecific for indian users only. So the meals and items should be strictly from Indian cuisine.
"""

    user_prompt = f"""
Generate a daily diet plan using ONLY these inputs:

Goal: {data.goal}
Diet type: {data.diet_type}
Meals per day: {data.meals_per_day}
Total calorie target: {data.calorie_target}
Allergies: {", ".join(data.allergies) if data.allergies else "None"}

IMPORTANT:
- Generate EXACTLY {data.meals_per_day} meals
- Use common meal names like Breakfast, Lunch, Dinner, Snack
- Distribute calories reasonably so total ≈ {data.calorie_target}

Return ONLY valid JSON.
"""

    last_error = None

    for attempt in range(1):  # retry once on invalid JSON
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

        try:
            parsed = json.loads(raw)
            return DietPlanResponse(**parsed)

        except Exception as e:
            last_error = e
            user_prompt += "\nREMINDER: Output MUST strictly match the JSON schema."

    raise ValueError(f"Invalid diet plan from OpenRouter: {last_error}")

# --------------------------------------------------
# MOCK IMPLEMENTATION (FREE / LOCAL)
# --------------------------------------------------

def _mock_generate_diet_plan(
    data: DietGenerateRequest,
) -> DietPlanResponse:
    """
    Deterministic mock diet generator.
    Minimal but realistic.
    """

    # Simple calorie split
    calories_per_meal = data.calorie_target // data.meals_per_day

    def meal_items(base_name: str) -> List[MealItem]:
        return [
            MealItem(
                name=f"{base_name}",
                calories=calories_per_meal,
                protein="20g",
            )
        ]

    meals = []

    meal_names = ["Breakfast", "Lunch", "Dinner", "Snack", "Snack 2", "Snack 3"]

    for i in range(data.meals_per_day):
        if data.diet_type == "vegan":
            base = "Tofu & Veggie Bowl"
        elif data.diet_type == "vegetarian":
            base = "Paneer & Rice Bowl"
        else:
            base = "Grilled Chicken & Rice"

        meals.append(
            Meal(
                meal=meal_names[i],
                items=meal_items(base),
            )
        )

    return DietPlanResponse(meals=meals)

# --------------------------------------------------
# DISPATCHER (THE SWITCH)
# --------------------------------------------------

def generate_diet_plan(
    data: DietGenerateRequest,
) -> DietPlanResponse:
    """
    Central AI entrypoint for diet generation.
    Switches between mock and real AI using AI_MODE.
    """

    if AI_MODE == "mock":
        return _mock_generate_diet_plan(data)

    if AI_MODE in {"openai", "openrouter"}:
        return _real_generate_diet_plan(data)

    raise RuntimeError(f"Invalid AI_MODE: {AI_MODE}")
