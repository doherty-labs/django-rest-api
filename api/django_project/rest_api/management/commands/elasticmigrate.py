from django.core.management.base import BaseCommand

from rest_api.tasks.elastic import create_indexes_safe


class Command(BaseCommand):
    def handle(self):
        create_indexes_safe()
        self.stdout.write(self.style.SUCCESS("Created indexes successfully"))
