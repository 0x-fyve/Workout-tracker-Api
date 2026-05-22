from django.shortcuts import render
from django.http import JsonResponse
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import WorkoutPlanSerializer

from .models import WorkoutPlan, WorkoutExercise, WorkoutLog
from exercises.models import Exercise

# Create your views here.

class WorkoutCreateView(APIView):

    permission_classes = [IsAuthenticated]

    def post(self, request):

        serializer = WorkoutPlanSerializer(data=request.data)

        if serializer.is_valid():

            # create workout plan
            workout = WorkoutPlan.objects.create(
                user=request.user,
                title=serializer.validated_data["title"],
                description=serializer.validated_data.get(
                    "description",
                    ""
                ),
                scheduled_date=serializer.validated_data[
                    "scheduled_date"
                ],
            )

            # create workout exercises
            exercises_data = serializer.validated_data.get(
                "exercises",
                []
            )

            for item in exercises_data:

                exercise = Exercise.objects.get(
                    id=item["exercise_id"]
                )

                WorkoutExercise.objects.create(
                    workout=workout,
                    exercise=exercise,
                    sets=item["sets"],
                    reps=item["reps"],
                    weight=item.get("weight", 0),
                    duration_minutes=item.get(
                        "duration_minutes"
                    ),
                    rest_seconds=item.get(
                        "rest_seconds",
                        60
                    ),
                    notes=item.get("notes", ""),
                )

            return Response(
                {
                    "message": "Workout created successfully",
                    "workout_id": workout.id,
                },
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )
    
    

    def get(self, request):

        workouts = WorkoutPlan.objects.filter(user=request.user)

        serializer = WorkoutPlanSerializer(workouts, many=True)

        return Response(serializer.data)
