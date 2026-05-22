from django.urls import path
from .views import WorkoutCreateView

urlpatterns = [
    path("api/createworkout", WorkoutCreateView.as_view()),
]
