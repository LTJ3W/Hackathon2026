import json
import os
from typing import Any, Dict, List

from django.conf import settings


def _build_chat_prompt(user_message: str) -> str:
    exercises = _load_exercises()[:20]
    ingredients = _load_ingredients()[:20]

    return f"""
You are FitGuide AI, a beginner-friendly fitness and nutrition assistant.
Answer briefly, clearly, and safely.

The user asked:
{user_message}

You may use this app data for grounding.

Exercises:
{json.dumps(exercises, indent=2)}

Ingredients:
{json.dumps(ingredients, indent=2)}

Rules:
- Keep answers short and practical.
- Be encouraging and beginner-friendly.
- Only answer fitness, workout, exercise, recovery, and nutrition questions.
- Do not give medical advice.
- If asked something medical, tell the user to consult a professional.
- If the question is outside fitness/nutrition, say you can only help with fitness and nutrition topics.
""".strip()

def fitness_chat_reply(user_message: str) -> str:
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        return (
            "AI chat is not configured yet. Please add an OpenAI API key. "
            "I can help with beginner fitness and nutrition questions once enabled."
        )

    try:
        from openai import OpenAI

        client = OpenAI(api_key=api_key)
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=_build_chat_prompt(user_message),
        )
        return response.output_text.strip()
    except Exception as e:
        print("OPENAI ERROR:", e)
        return f"Sorry, the AI assistant is unavailable right now. Error: {e}"

def _load_exercises() -> List[Dict[str, Any]]:
    with open(settings.EXERCISES_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def _load_ingredients() -> List[Dict[str, Any]]:
    with open(settings.INGREDIENTS_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def _goal_to_data_goal(goal: str) -> str:
    mapping = {
        "lose_weight": "weight_loss",
        "build_muscle": "muscle_gain",
        "maintain_health": "maintain_health",
    }
    return mapping.get(goal, goal)


def _plan_days(exercise_days: str) -> int:
    mapping = {"0": 2, "1-2": 2, "3-4": 4, "5+": 5}
    return mapping.get(exercise_days, 3)


def _difficulty(active: str, exercise_days: str) -> str:
    if active == "no" or exercise_days in {"0", "1-2", None, ""}:
        return "beginner"
    if exercise_days == "3-4":
        return "intermediate"
    return "intermediate"


def _pick_exercises(goal: str, active: str, exercise_days: str) -> List[Dict[str, Any]]:
    all_exercises = _load_exercises()
    difficulty = _difficulty(active, exercise_days)

    if goal == "lose_weight":
        preferred_categories = ["cardio", "legs", "core", "pull", "push"]
    elif goal == "build_muscle":
        preferred_categories = ["push", "pull", "legs", "core"]
    else:
        preferred_categories = ["push", "pull", "legs", "cardio", "core"]

    filtered = [e for e in all_exercises if e.get("difficulty") == difficulty]
    if not filtered:
        filtered = all_exercises

    ordered: List[Dict[str, Any]] = []
    for category in preferred_categories:
        ordered.extend([e for e in filtered if e.get("category") == category])

    seen = set()
    unique = []
    for item in ordered:
        if item["id"] not in seen:
            unique.append(item)
            seen.add(item["id"])
    return unique[:12]


def _pick_ingredients(goal: str) -> List[Dict[str, Any]]:
    all_ingredients = _load_ingredients()
    data_goal = _goal_to_data_goal(goal)
    results = [i for i in all_ingredients if data_goal in i.get("goals", [])]

    if goal == "build_muscle":
        results.sort(key=lambda x: (x.get("protein_g", 0), -x.get("fat_g", 0)), reverse=True)
    elif goal == "lose_weight":
        results.sort(key=lambda x: (x.get("protein_g", 0), -x.get("calories_per_100g", 0)), reverse=True)
    else:
        results.sort(key=lambda x: (x.get("protein_g", 0), -x.get("carbs_g", 0)), reverse=True)
    return results[:6]


def build_rule_based_plan(profile: Dict[str, str]) -> Dict[str, Any]:
    days = _plan_days(profile.get("exercise_days", ""))
    exercises = _pick_exercises(profile.get("goal", ""), profile.get("active", ""), profile.get("exercise_days", ""))
    ingredients = _pick_ingredients(profile.get("goal", ""))

    split = []
    pool = exercises.copy()
    chunk_size = max(2, len(pool) // max(days, 1))

    for day in range(days):
        start = day * chunk_size
        end = start + chunk_size
        block = pool[start:end] or pool[:3]
        split.append(
            {
                "day": f"Day {day + 1}",
                "focus": block[0].get("category", "general").title() if block else "General Fitness",
                "exercises": [
                    {
                        "name": item["name"],
                        "target": ", ".join(item.get("target_muscles", [])),
                        "difficulty": item.get("difficulty", "beginner"),
                    }
                    for item in block[:3]
                ],
            }
        )

    goal_label = {
        "lose_weight": "Lose Weight",
        "build_muscle": "Build Muscle",
        "maintain_health": "Maintain Health",
    }.get(profile.get("goal"), "General Fitness")

    return {
        "source": "rule-based",
        "summary": f"A {days}-day starter plan focused on {goal_label.lower()} with beginner-friendly structure.",
        "workout_days": days,
        "difficulty": _difficulty(profile.get("active", ""), profile.get("exercise_days", "")),
        "weekly_plan": split,
        "nutrition": [
            {
                "name": item["name"],
                "category": item["category"],
                "protein_g": item.get("protein_g", 0),
                "calories_per_100g": item.get("calories_per_100g", 0),
                "reason": item.get("benefits", [""])[0],
            }
            for item in ingredients
        ],
        "tips": [
            "Start with correct form before increasing weight or volume.",
            "Aim for consistency first; intensity can grow each week.",
            "Prioritize sleep, hydration, and protein intake for recovery.",
        ],
    }
