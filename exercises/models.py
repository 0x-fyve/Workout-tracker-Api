from django.db import models

# Create your models here.
import uuid


class Exercise(models.Model):

    CATEGORY_CHOICES = [
        ("strength", "Strength"),
        ("cardio", "Cardio"),
        ("flexibility", "Flexibility"),
    ]

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False
    )

    name = models.CharField(
        max_length=255,
        unique=True
    )

    description = models.TextField()

    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES
    )

    muscle_group = models.CharField(
        max_length=100
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name