from typing import Any

from django.core.management.base import BaseCommand

from database.models import Role


class Command(BaseCommand):
    help = "Seeds the Role Table"

    def handle(self, *args: Any, **options: Any) -> str | None:
        if not Role.objects.filter(rolename="ADMIN").exists():
            Role.objects.create(rolename="ADMIN").save()
        if not Role.objects.filter(rolename="USER").exists():
            Role.objects.create(rolename="USER").save()

        self.stdout.write(self.style.SUCCESS("Seeded Role Table."))
