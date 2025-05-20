from django.core.management.base import BaseCommand

from rest_api.tasks.elastic import rebuild_indexes


class Command(BaseCommand):
    def handle(self, *_, **__) -> None:
        rebuild_indexes()
        self.stdout.write(self.style.SUCCESS("Rebuilt indexes successfully"))
