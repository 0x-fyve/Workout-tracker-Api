from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()
from exercises.models import Exercise




class WorkoutPlan(models.Model):

    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("completed", "Completed"),
        ("cancelled", "Cancelled"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="workouts"
    )

    title = models.CharField(max_length=255)

    description = models.TextField(blank=True)

    scheduled_date = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )

    comments = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["scheduled_date"]

    def __str__(self):
        return f"{self.user.username} - {self.title}"


class WorkoutExercise(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    workout = models.ForeignKey(
        WorkoutPlan,
        on_delete=models.CASCADE,
        related_name="workout_exercises"
    )

    exercise = models.ForeignKey(
        Exercise,
        on_delete=models.CASCADE,
        related_name="exercise_workouts"
    )

    sets = models.PositiveIntegerField()

    reps = models.PositiveIntegerField()

    weight = models.DecimalField(
        max_digits=6,
        decimal_places=2,
        default=0
    )

    duration_minutes = models.PositiveIntegerField(
        null=True,
        blank=True
    )

    rest_seconds = models.PositiveIntegerField(
        default=60
    )

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["created_at"]

    def __str__(self):
        return f"{self.exercise.name} - {self.workout.title}"


class WorkoutLog(models.Model):

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="workout_logs"
    )

    workout = models.ForeignKey(
        WorkoutPlan,
        on_delete=models.CASCADE,
        related_name="logs"
    )

    completed_at = models.DateTimeField(auto_now_add=True)

    calories_burned = models.PositiveIntegerField(default=0)

    duration_minutes = models.PositiveIntegerField(default=0)

    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-completed_at"]

    def __str__(self):
        return f"{self.user.username} - {self.workout.title}"