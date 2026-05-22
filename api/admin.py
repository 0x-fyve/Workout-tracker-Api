from django.contrib import admin
from .models import WorkoutPlan, WorkoutExercise
# Register your models here.
admin.site.register(WorkoutPlan)
admin.site.register(WorkoutExercise)