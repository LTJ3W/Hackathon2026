# FitGuide

A beginner-friendly fitness web app that helps users improve their health through personalized workout plans, nutrition guidance, and smart recommendations.

---

## Overview

FitGuide is a fitness application built to support people who want to start or improve their fitness journey. The app focuses on helping users set goals, follow workout plans, and get simple nutrition advice in one place.

This project is especially designed for beginners who need clear guidance and an easy-to-use platform.

---

## Mission

Our mission is to help people achieve their fitness goals by providing accessible tools for exercise planning, nutrition support, and personalized recommendations.

---

## Problem

Many people want to get fit but do not know where to start. They may struggle with:
- choosing the right workouts
- creating a healthy meal plan
- staying consistent
- finding advice that matches their level

FitGuide solves this by giving users a simple platform with structured fitness and nutrition support.

---

## Features

### Fitness Assessment
Users complete a short form including:
- fitness goals (weight loss, muscle gain, maintenance)
- activity level
- available workout days

The system generates a structured weekly plan based on this information.

### Workout Plan Generation
Plans are generated using a rule-based system that:
- filters exercises by difficulty and category
- distributes exercises across multiple days
- focuses on goal-specific training

### Nutrition Guidance
The system recommends ingredients based on user goals:
- high protein for muscle gain
- lower calorie density for weight loss
- balanced options for general health

### Assistant Page
A separate assistant interface allows users to ask:
- workout-related questions
- nutrition questions
- beginner fitness guidance

## Tech Stack

- Backend: Django
- Frontend: HTML, CSS, JavaScript
- Data: JSON datasets (exercises and ingredients)
- Styling: Bootstrap + custom CSS

## Architecture

The application uses a modular structure:

- `views.py` → request handling
- `services/ai_coach.py` → recommendation logic and assistant responses
- `templates/` → UI rendering
- `static/` → CSS and JavaScript

The assistant is decoupled from the main plan generation system, allowing independent interaction.

## Setup

1. Install dependencies:
   ```bash
   pip install django


