from django.shortcuts import render
#from django.urls import path
#from django.contrib.auth import views as auth_views
#from . import views

def home(request):
    return render(request, "base.html")