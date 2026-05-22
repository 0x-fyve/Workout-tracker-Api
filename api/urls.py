from django.urls import path
from .views import WorkoutCreateView

urlpatterns = [
    path("api/workout", WorkoutCreateView.as_view()),
]
