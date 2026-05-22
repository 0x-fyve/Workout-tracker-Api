from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ReadOnlyModelViewSet

from .models import Exercise
from api.serializers import ExerciseSerializer


class ExerciseViewSet(ReadOnlyModelViewSet):

    queryset = Exercise.objects.all()

    serializer_class = ExerciseSerializer