from django.shortcuts import render
#from django.urls import path
#from django.contrib.auth import views as auth_views
#from . import views

def home(request):
    return render(request, "base.html")


def dashboard(request):
    plan = None

    if request.method == "POST":
        age = int(request.POST.get("age"))
        height = int(request.POST.get("height"))
        weight = int(request.POST.get("weight"))
        nutrition = request.POST.get("nutrition")
        meals_per_day = request.POST.get("meals_per_day")
        eat_out = request.POST.get("eat_out")
        active = request.POST.get("active")
        exercise_days = request.POST.get("exercise_days")
        goal = request.POST.get("goal")

        # Fitness level
        if active == "no" or exercise_days in ["0", "1-2"]:
            fitness_level = "Beginner"
        elif exercise_days == "3-4":
            fitness_level = "Intermediate"
        else:
            fitness_level = "Advanced"

        # Nutrition level
        if nutrition == "poor" or eat_out in ["3-5", "6+"]:
            nutrition_level = "Needs Improvement"
        elif nutrition == "medium":
            nutrition_level = "Moderate"
        else:
            nutrition_level = "Strong"

        # Plan suggestion
        if goal == "lose_weight":
            workout_plan = f"{fitness_level} fat-loss workout plan"
            meal_plan = "Calorie-conscious meal plan with balanced portions"
        elif goal == "build_muscle":
            workout_plan = f"{fitness_level} strength training plan"
            meal_plan = "High-protein meal plan for muscle growth"
        elif goal == "improve_endurance":
            workout_plan = f"{fitness_level} endurance training plan"
            meal_plan = "Energy-support meal plan with balanced carbs and protein"
        else:
            workout_plan = f"{fitness_level} general fitness plan"
            meal_plan = "Balanced nutrition plan for overall health"

        plan = {
            "fitness_level": fitness_level,
            "nutrition_level": nutrition_level,
            "workout_plan": workout_plan,
            "meal_plan": meal_plan,
        }

    return render(request, "dashboard.html", {"plan": plan})

