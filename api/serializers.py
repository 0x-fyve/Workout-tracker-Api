from rest_framework import serializers

from .models import (
    WorkoutPlan,
    WorkoutExercise,
    WorkoutLog,
)
from exercises.models import Exercise


class ExerciseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Exercise
        fields = [
            "id",
            "name",
            "description",
            "category",
            "muscle_group",
            "created_at",
        ]


class WorkoutExerciseSerializer(serializers.ModelSerializer):

    exercise_id = serializers.UUIDField(write_only=True)

    exercise = ExerciseSerializer(read_only=True)

    class Meta:
        model = WorkoutExercise
        fields = [
            "id",
            "exercise_id",
            "exercise",
            "sets",
            "reps",
            "weight",
            "duration_minutes",
            "rest_seconds",
            "notes",
            "created_at",
        ]

    def create(self, validated_data):

        exercise_id = validated_data.pop("exercise_id")

        exercise = Exercise.objects.get(id=exercise_id)

        validated_data["exercise"] = exercise

        return WorkoutExercise.objects.create(**validated_data)


class WorkoutPlanSerializer(serializers.ModelSerializer):

    exercises = WorkoutExerciseSerializer(
        many=True,
        source="workout_exercises"
    )

    class Meta:
        model = WorkoutPlan
        fields = [
            "id",
            "title",
            "description",
            "scheduled_date",
            "status",
            "comments",
            "created_at",
            "updated_at",
            "exercises",
        ]

    def create(self, validated_data):

        exercises_data = validated_data.pop(
            "workout_exercises",
            []
        )

        workout = WorkoutPlan.objects.create(
            user=self.context["request"].user,
            **validated_data
        )

        for exercise_data in exercises_data:

            exercise_id = exercise_data.pop(
                "exercise_id"
            )

            exercise = Exercise.objects.get(
                id=exercise_id
            )

            WorkoutExercise.objects.create(
                workout=workout,
                exercise=exercise,
                **exercise_data
            )

        return workout

    def update(self, instance, validated_data):

        exercises_data = validated_data.pop(
            "workout_exercises",
            None
        )

        instance.title = validated_data.get(
            "title",
            instance.title
        )

        instance.description = validated_data.get(
            "description",
            instance.description
        )

        instance.scheduled_date = validated_data.get(
            "scheduled_date",
            instance.scheduled_date
        )

        instance.status = validated_data.get(
            "status",
            instance.status
        )

        instance.comments = validated_data.get(
            "comments",
            instance.comments
        )

        instance.save()

        # optional full replacement
        if exercises_data is not None:

            instance.workout_exercises.all().delete()

            for exercise_data in exercises_data:

                exercise_id = exercise_data.pop(
                    "exercise_id"
                )

                exercise = Exercise.objects.get(
                    id=exercise_id
                )

                WorkoutExercise.objects.create(
                    workout=instance,
                    exercise=exercise,
                    **exercise_data
                )

        return instance


class WorkoutLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = WorkoutLog
        fields = [
            "id",
            "workout",
            "completed_at",
            "calories_burned",
            "duration_minutes",
            "notes",
            "created_at",
        ]