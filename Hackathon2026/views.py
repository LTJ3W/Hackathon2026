import json
import random
from pathlib import Path

from django.conf import settings
from django.shortcuts import render, redirect


def _load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def _save_json(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2)


def _load_ingredients():
    return _load_json(settings.INGREDIENTS_JSON)


def _load_fitness():
    return _load_json(settings.EXERCISES_JSON)


def _load_saved_plans():
    fitness_json_path = settings.FITNESS_PLANS_JSON
    if not Path(fitness_json_path).exists():
        return {"plans": []}

    try:
        data = _load_json(fitness_json_path)
        if isinstance(data, dict) and "plans" in data:
            return data
        return {"plans": []}
    except Exception:
        return {"plans": []}


def _save_saved_plans(data):
    _save_json(settings.FITNESS_PLANS_JSON, data)


def _normalize_goal(goal):
    mapping = {
        "lose_weight": "weight_loss",
        "build_muscle": "muscle_gain",
        "maintain_health": "general_health",
        "improve_endurance": "general_health",
    }
    return mapping.get(goal, "general_health")


def _pretty_goal(goal):
    mapping = {
        "weight_loss": "Lose Weight",
        "muscle_gain": "Build Muscle",
        "general_health": "Maintain Health",
    }
    return mapping.get(goal, goal.replace("_", " ").title())


def _determine_level(active, exercise_days):
    if active == "no" or exercise_days in ["0", "1-2"]:
        return "beginner"
    elif exercise_days == "3-4":
        return "intermediate"
    return "advanced"


def _goal_cardio(level, goal):
    cardio_map = {
        ("beginner", "weight_loss"): [
            "15 min incline walk after lifting",
            "15 min bike or elliptical",
            "10 min incline treadmill cool-down",
        ],
        ("beginner", "muscle_gain"): [
            "5 min light treadmill warm-up",
            "5 min rowing warm-up",
            "5 min bike warm-up",
        ],
        ("beginner", "general_health"): [
            "10 min brisk walk",
            "10 min cycling",
            "10 min easy cardio",
        ],
        ("intermediate", "weight_loss"): [
            "15 min incline walk",
            "15 min moderate row",
            "10 min treadmill cool-down",
            "25 min zone-2 cardio",
        ],
        ("intermediate", "muscle_gain"): [
            "5 min warm-up",
            "5 min warm-up",
            "5 min warm-up",
            "5 min easy cardio",
        ],
        ("intermediate", "general_health"): [
            "10 min cycling",
            "10 min brisk walk",
            "10 min row",
            "15 min easy cardio",
        ],
        ("advanced", "weight_loss"): [
            "15 min HIIT bike",
            "15 min zone-2 row",
            "10 min cool-down walk",
            "25 min steady-state cardio",
            "15 min incline walk",
        ],
        ("advanced", "muscle_gain"): [
            "5 min warm-up",
            "5 min warm-up",
            "5 min warm-up",
            "10 min easy cardio",
            "5 min warm-up",
        ],
        ("advanced", "general_health"): [
            "10 min cycling",
            "10 min row",
            "10 min brisk walk",
            "15 min zone-2 cardio",
            "10 min easy walk",
        ],
    }
    return cardio_map[(level, goal)]


def _plan_meta(level, goal):
    meta = {
        ("beginner", "weight_loss"): {
            "title": "Beginner Fat-Loss Starter",
            "description": "A 3-day push, pull, and legs routine built for beginners who want to lose fat while building basic strength and consistency.",
            "benefits": "This plan helps increase calorie burn, improve workout consistency, and preserve muscle while losing weight.",
            "ingredient_categories": ["protein", "vegetable", "fruit", "hydration"],
        },
        ("beginner", "muscle_gain"): {
            "title": "Beginner Muscle Foundation",
            "description": "A 3-day push, pull, and legs split made for beginners who want to build muscle with manageable weekly volume.",
            "benefits": "This plan supports steady muscle growth, improves lifting form, and gives enough recovery between sessions.",
            "ingredient_categories": ["protein", "carbohydrate", "fruit", "hydration"],
        },
        ("beginner", "general_health"): {
            "title": "Beginner Healthy Habit Plan",
            "description": "A 3-day routine for beginners who want to feel stronger, healthier, and more active.",
            "benefits": "This plan improves daily energy, supports long-term health, and helps build sustainable habits.",
            "ingredient_categories": ["protein", "vegetable", "fruit", "hydration"],
        },
        ("intermediate", "weight_loss"): {
            "title": "Intermediate Cutting Split",
            "description": "A 4-day plan for intermediate users who want to lose fat while keeping muscle and training intensity high.",
            "benefits": "This plan increases weekly activity, raises calorie burn, and helps preserve lean muscle.",
            "ingredient_categories": ["protein", "vegetable", "fruit", "hydration"],
        },
        ("intermediate", "muscle_gain"): {
            "title": "Intermediate Hypertrophy Split",
            "description": "A 4-day hypertrophy-focused split for intermediate lifters aiming to build more muscle.",
            "benefits": "This plan adds training volume where it matters most and supports steady strength and size gains.",
            "ingredient_categories": ["protein", "carbohydrate", "fruit", "hydration"],
        },
        ("intermediate", "general_health"): {
            "title": "Intermediate Balanced Fitness",
            "description": "A 4-day balanced routine for users who want overall fitness, strength, and better health.",
            "benefits": "This plan supports cardiovascular health, posture, core strength, and full-body balance.",
            "ingredient_categories": ["protein", "vegetable", "fruit", "hydration"],
        },
        ("advanced", "weight_loss"): {
            "title": "Advanced Cutting Program",
            "description": "A 5-day advanced split for experienced users who want to lose fat while maintaining performance.",
            "benefits": "This plan creates high weekly energy output, supports muscle retention, and keeps workouts challenging.",
            "ingredient_categories": ["protein", "vegetable", "fruit", "hydration"],
        },
        ("advanced", "muscle_gain"): {
            "title": "Advanced Hypertrophy Program",
            "description": "A 5-day advanced split built for users chasing higher muscle-building volume and progression.",
            "benefits": "This plan supports muscle growth through more weekly volume, specialization, and structured recovery.",
            "ingredient_categories": ["protein", "carbohydrate", "fruit", "hydration"],
        },
        ("advanced", "general_health"): {
            "title": "Advanced Athletic Maintenance",
            "description": "A 5-day routine for advanced users who want to maintain strength, muscle, and overall health.",
            "benefits": "This plan helps maintain fitness, body composition, and performance without losing balance or recovery.",
            "ingredient_categories": ["protein", "vegetable", "fruit", "hydration"],
        },
    }
    return meta[(level, goal)]


def _get_day_structure(level, goal):
    if level == "beginner":
        return ["push", "pull", "legs"]

    if level == "intermediate":
        if goal == "weight_loss":
            return ["push", "pull", "legs", "abs"]
        if goal == "muscle_gain":
            return ["push", "pull", "legs", "push"]
        return ["push", "pull", "legs", "abs"]

    # advanced
    return ["push", "pull", "legs", "abs", "pull"]


def _get_day_labels(level, goal):
    if level == "beginner":
        return ["Push Day", "Pull Day", "Leg Day"]

    if level == "intermediate":
        if goal == "weight_loss":
            return ["Push Day", "Pull Day", "Leg Day", "Core & Cardio Day"]
        if goal == "muscle_gain":
            return ["Push Day", "Pull Day", "Leg Day", "Shoulder Focus Day"]
        return ["Push Day", "Pull Day", "Leg Day", "Core Day"]

    return ["Push Day", "Pull Day", "Leg Day", "Core Day", "Arm Focus Day"]


def _allowed_difficulties(level):
    if level == "beginner":
        return {"beginner"}
    if level == "intermediate":
        return {"beginner", "intermediate"}
    return {"beginner", "intermediate", "advanced"}


def _filter_exercises_by_category(exercises, category, level):
    allowed = _allowed_difficulties(level)

    filtered = [
        item for item in exercises
        if item.get("category") == category and item.get("difficulty") in allowed
    ]

    if category == "pull":
        return filtered

    return filtered


def _pick_exercises_for_day(exercises, category, level, desired_count):
    pool = _filter_exercises_by_category(exercises, category, level)

    # Arm focus day uses bicep-heavy pull exercises
    if category == "pull":
        bicep_pool = [
            item for item in pool
            if "biceps" in item.get("target_muscles", [])
            or "forearms" in item.get("target_muscles", [])
        ]
        if len(bicep_pool) >= desired_count:
            pool = bicep_pool

    # Shoulder focus fallback on push day
    if category == "push" and desired_count == 5:
        shoulder_first = [
            item for item in pool
            if "shoulders" in item.get("target_muscles", [])
        ]
        chest_triceps = [
            item for item in pool
            if item not in shoulder_first
        ]
        mixed = shoulder_first + chest_triceps
        if len(mixed) >= desired_count:
            pool = mixed

    random.shuffle(pool)
    return pool[:desired_count]


def _pick_ingredients(ingredients, goal, categories, limit=6):
    matches = []
    for item in ingredients:
        item_goals = item.get("goals", [])
        item_category = item.get("category", "")
        if goal in item_goals and item_category in categories:
            matches.append(item)

    # remove duplicates by name
    unique = []
    seen = set()
    for item in matches:
        key = item.get("name", "").lower()
        if key and key not in seen:
            unique.append(item)
            seen.add(key)

    return unique[:limit]



def _next_plan_number(saved_plans):
    plans = saved_plans.get("plans", [])
    if not plans:
        return 1
    return max(plan.get("plan_number", 0) for plan in plans) + 1


def _generate_plan(payload):
    exercises = _load_fitness()
    ingredients = _load_ingredients()

    normalized_goal = _normalize_goal(payload["goal"])
    level = _determine_level(payload["active"], payload["exercise_days"])
    meta = _plan_meta(level, normalized_goal)

    day_categories = _get_day_structure(level, normalized_goal)
    day_labels = _get_day_labels(level, normalized_goal)
    cardio_list = _goal_cardio(level, normalized_goal)
    exercise_count = 4 if level == "beginner" else 5

    workout_days = []
    for index, category in enumerate(day_categories):
        day_exercises = _pick_exercises_for_day(
            exercises,
            category=category,
            level=level,
            desired_count=exercise_count
        )

        workout_days.append({
            "day": index + 1,
            "focus": category,
            "focus_label": day_labels[index],
            "cardio": cardio_list[index],
            "exercises": day_exercises,
        })

    prioritized_ingredients = _pick_ingredients(
        ingredients,
        goal=normalized_goal,
        categories=meta["ingredient_categories"],
        limit=6,
    )

    return {
        "level": level,
        "goal": normalized_goal,
        "goal_label": _pretty_goal(normalized_goal),
        "title": meta["title"],
        "description": meta["description"],
        "benefits": meta["benefits"],
        "days_per_week": len(workout_days),
        "ingredient_priorities": prioritized_ingredients,
        "workout_days": workout_days,
        "template_key": f"{level}_{normalized_goal}",
    }


def home(request):
    return render(request, "base.html")


def dashboard(request):
    if request.method == "POST":
        payload = {
            "age": request.POST.get("age"),
            "height": request.POST.get("height"),
            "weight": request.POST.get("weight"),
            "nutrition": request.POST.get("nutrition"),
            "meals_per_day": request.POST.get("meals_per_day"),
            "eat_out": request.POST.get("eat_out"),
            "active": request.POST.get("active"),
            "exercise_days": request.POST.get("exercise_days"),
            "goal": request.POST.get("goal"),
        }

        plan = _generate_plan(payload)
        saved = _load_saved_plans()
        plan_number = _next_plan_number(saved)

        record = {
            "plan_number": plan_number,
            "user_answers": payload,
            "plan": plan,
        }

        saved["plans"].append(record)
        _save_saved_plans(saved)

        return render(
            request,
            "plan_result.html",
            {
                "plan_number": plan_number,
                "plan": plan,
            },
        )

    return render(request, "dashboard.html")


def search_ingredients(request):
    all_items = _load_ingredients()

    q = (request.GET.get("q") or "").strip().lower()
    category = request.GET.get("category") or ""
    goal = request.GET.get("goal") or ""

    results = all_items

    if q:
        results = [
            i for i in results
            if q in i["name"].lower()
            or q in i["category"].lower()
            or any(q in b.lower() for b in i.get("benefits", []))
        ]

    if category:
        results = [i for i in results if i["category"] == category]

    if goal:
        results = [i for i in results if goal in i.get("goals", [])]

    categories = sorted({i["category"] for i in all_items})
    goals = sorted({g for i in all_items for g in i.get("goals", [])})

    context = {
        "results": results,
        "q": q,
        "selected_category": category,
        "selected_goal": goal,
        "categories": categories,
        "goals": goals,
        "total": len(all_items),
    }
    return render(request, "search_ingredients.html", context)


def search_fitness(request):
    all_items = _load_fitness()

    q = (request.GET.get("q") or "").strip().lower()
    category = request.GET.get("category") or ""
    target_muscle = request.GET.get("target_muscle") or ""

    results = all_items

    if q:
        results = [
            i for i in results
            if q in i["name"].lower()
            or q in i["category"].lower()
            or q in i.get("description", "").lower()
            or any(q in m.lower() for m in i.get("target_muscles", []))
        ]

    if category:
        results = [i for i in results if i["category"] == category]

    if target_muscle:
        results = [
            i for i in results
            if target_muscle in i.get("target_muscles", [])
        ]

    categories = sorted({i["category"] for i in all_items})
    target_muscles = sorted(
        {m for i in all_items for m in i.get("target_muscles", [])}
    )

    context = {
        "results": results,
        "q": q,
        "selected_category": category,
        "selected_target_muscle": target_muscle,
        "categories": categories,
        "target_muscles": target_muscles,
        "total": len(all_items),
    }
    return render(request, "search_fitness.html", context)


def search_plans(request):
    saved = _load_saved_plans()
    q = (request.GET.get("q") or "").strip()

    result = None
    not_found = False

    if q:
        try:
            number = int(q)
            result = next(
                (plan for plan in saved.get("plans", []) if plan.get("plan_number") == number),
                None,
            )
            if result is None:
                not_found = True
        except ValueError:
            not_found = True

    context = {
        "q": q,
        "result": result,
        "not_found": not_found,
        "total": len(saved.get("plans", [])),
    }
    return render(request, "search_plans.html", context)