from os import listdir, unlink
from os.path import join, islink, isfile
from typing import Any

from django.conf import settings
from django.core.management.base import BaseCommand

from database import models


class Command(BaseCommand):
    help = "Destroy / Truncate Data in All Tables"

    def handle(self, *args: Any, **options: Any) -> str | None:
        models.Transaction.objects.all().delete()
        models.File.objects.all().delete()
        models.RecentActivity.objects.all().delete()
        models.User.objects.all().delete()
        models.RBAC.objects.all().delete()
        models.Role.objects.all().delete()
        models.Permission.objects.all().delete()

        for filename in listdir(settings.MEDIA_ROOT):
            filepath = join(settings.MEDIA_ROOT, filename)

            try:
                if islink(filepath) or isfile(filepath):
                    unlink(filepath)
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Encountered an error when deleting {filename}. Error: {e}"))
        self.stdout.write(self.style.WARNING("Truncated Data from All Tables"))
