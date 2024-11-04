import os

from django.contrib.auth import get_user_model
from django.core.management import CommandError
from django.core.management.base import BaseCommand
from dotenv import load_dotenv

load_dotenv()


class Command(BaseCommand):
    """A command that creates a superuser"""

    def handle(self, *args, **kwargs):
        """
        A method that creates a superuser
        :return: User model
        """
        user = get_user_model()

        username = os.environ.get("ADMIN_USERNAME")
        email = os.environ.get("ADMIN_EMAIL")
        password = os.environ.get("ADMIN_PASSWORD")

        # Check if a user with the same username or email already exists
        if user.objects.filter(username=username).exists():
            raise CommandError(f"Superuser with username '{username}' already exists")

        if user.objects.filter(email=email).exists():
            raise CommandError(f"Superuser with email '{email}' already exists")

        if all((username, email, password)):
            user.objects.create_superuser(
                username=username, email=email, password=password
            )

            self.stdout.write(
                self.style.SUCCESS(
                    f" ===Successfully created superuser '{username}'=== "
                )
            )
        else:
            self.stdout.write(
                self.style.ERROR(
                    f" ===Failed to create superuser. Please provide all credentials correctly=== "
                )
            )