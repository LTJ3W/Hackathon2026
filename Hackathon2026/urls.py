from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("search/ingredients/", views.search_ingredients, name="search_ingredients"),
    path("search/fitness/", views.search_fitness, name="search_fitness"),
    path("search/plans/", views.search_plans, name="search_plans"),
    path("admin/", admin.site.urls),
]