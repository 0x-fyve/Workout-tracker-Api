import json
from pathlib import Path

from django.core.management.base import BaseCommand

from exercises.models import Exercise


class Command(BaseCommand):

    help = "Seed exercises into database"

    def handle(self, *args, **kwargs):

        json_path = (
            Path(__file__)
            .resolve()
            .parent.parent.parent
            / "data"
            / "exercises.json"
        )

        with open(json_path, "r", encoding="utf-8") as file:

            exercises = json.load(file)

        for exercise in exercises:

            obj, created = Exercise.objects.get_or_create(

                name=exercise["name"],

                defaults={
                    "description": exercise["description"],
                    "category": exercise["category"],
                    "muscle_group": exercise["muscle_group"],
                }
            )

            if created:

                self.stdout.write(
                    self.style.SUCCESS(
                        f"Added: {exercise['name']}"
                    )
                )

            else:

                self.stdout.write(
                    self.style.WARNING(
                        f"Already exists: {exercise['name']}"
                    )
                )

        self.stdout.write(
            self.style.SUCCESS(
                "Exercise seeding complete."
            )
        )