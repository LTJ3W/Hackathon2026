from django.shortcuts import render
#from django.urls import path
#from django.contrib.auth import views as auth_views
#from . import views

def home(request):
    return render(request, "base.html")


def dashboard(request):
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

        # later you can save this data or generate a plan

    return render(request, "dashboard.html")

