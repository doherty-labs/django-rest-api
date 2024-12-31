import os

from django.contrib.auth.management.commands import createsuperuser


class Command(createsuperuser.Command):
    help = "Create a superuser"

    def handle(self, *args, **options):
        username = os.environ.get("DJANGO_SUPERUSER_USERNAME")

        # check if user already exists
        if self.UserModel.objects.filter(username=username).exists():
            self.stdout.write(
                self.style.WARNING(f"Superuser {username} already exists"),
            )
            return None

        # create superuser
        return super().handle(*args, **options)
