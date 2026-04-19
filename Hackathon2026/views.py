import json
from django.conf import settings
from django.shortcuts import render


def _load_ingredients():
    with open(settings.INGREDIENTS_JSON, "r", encoding="utf-8") as f:
        return json.load(f)


def home(request):
    return render(request, "base.html")


def dashboard(request):
    if request.method == "POST":
        # Placeholder — later you can save this or generate a plan.
        _ = {
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

    return render(request, "dashboard.html")


def search_ingredients(request):
    """Search the ingredients.json file by name, category, and goal."""
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
    return render(request, "coming_soon.html", {"label": "Fitness"})


def search_plans(request):
    return render(request, "coming_soon.html", {"label": "Fitness Plans"})