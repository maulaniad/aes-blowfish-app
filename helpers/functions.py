import os
import string
import random
from datetime import datetime, timedelta
from typing import Any

from django.core.files.base import ContentFile, File
from django.core.paginator import Paginator, Page
from django.http import HttpRequest

from core.aes128 import AES
from database.models import RecentActivity
from helpers.dates import dt_now
from helpers.enums import RecentActivityType
from helpers.types import ICONS, COLORS, RecentActivityDict


def open_file(file: File | str, size: int | None = None) -> bytes:
    if isinstance(file, File):
        f = file.open(mode="rb")

        if size:
            file_content = f.read(size)
        else:
            file_content = f.read()

        f.close()
        return file_content

    with open(file, 'rb') as f:
        if size:
            return f.read(size)
        return f.read()


def write_bytes_to_file(data: bytes, file_path: str):
    with open(file_path, 'wb') as f:
        f.write(data)

    return ContentFile(data, name=file_path.split("/")[-1])


def generate_random_chars(type: object = str, length: int = 8) -> str | bytes:
    if type == str:
        return "".join(
            random.choice(string.ascii_letters + string.digits) for _ in range(length)
        )

    return os.urandom(length)


def generate_search_code(string: str) -> str:
    cd = dt_now()
    return f"{string.upper()}-{generate_random_chars().upper()}-{cd.day}-{cd.time().hour}-{cd.time().second}"


def format_size(size_in_bytes: int) -> str:
    units = ("B", "KB", "MB", "GB", "TB")
    unit_index = 0
    size = float(size_in_bytes)

    while size >= 1024 and unit_index < len(units) - 1:
        size /= 1024
        unit_index += 1

    return f"{size:.2f} {units[unit_index]}"


def format_time_difference(timestamp: datetime) -> str:
    now = datetime.now()
    time_diff = now - timestamp

    if time_diff < timedelta(minutes=5):
        return "Baru saja"
    elif time_diff < timedelta(hours=1):
        minutes = time_diff.seconds // 60
        return f"{minutes} menit yang lalu"
    elif time_diff < timedelta(days=1):
        hours = time_diff.seconds // 3600
        return f"{hours} jam yang lalu"
    elif time_diff < timedelta(days=2):
        hours = time_diff.seconds // 3600
        return f"Kemarin {hours} jam yang lalu"
    days = time_diff.days
    return f"{days} hari yang lalu"


def paginate(data: Any, page: int = 1, page_size: int = 10) -> tuple[Page, dict[str, Any]]:
    paginator = Paginator(data, page_size)
    page_obj = paginator.get_page(page)
    meta = {
        'page_size': paginator.per_page,
        'current_page': page_obj.number,
        'total_pages': paginator.num_pages
    }

    return page_obj, meta


def encrypt_file(file: File | str, key: bytes, initial_vector: bytes) -> bytes:
    plaintext = open_file(file)

    aes = AES(key)

    ciphertext = aes.encrypt_cbc(plaintext, initial_vector)
    return ciphertext


def decrypt_file(file: File | str, key: bytes, initial_vector: bytes):
    ciphertext = open_file(file)

    aes = AES(key)

    plaintext = aes.decrypt_cbc(ciphertext, initial_vector)
    return plaintext


def get_recent_activities(length: int) -> list[RecentActivityDict]:
    results = []
    recent_activities = tuple(RecentActivity.objects.all().order_by('-issued')[:length])

    for recent_activity in recent_activities:
        results.append({
            'action': recent_activity.action,
            'box_icon': recent_activity.box_icon,
            'tw_color': recent_activity.tw_color,
            'user': recent_activity.user.fullname,
            'time_difference': format_time_difference(recent_activity.issued),
        })

    return results


def create_recent_activity(request: HttpRequest, type: RecentActivityType, timestamp: datetime = dt_now()):
    RecentActivity.objects.create(
        action=type.value,
        box_icon=ICONS[type],
        tw_color=COLORS[type],
        issued=timestamp,
        user=request.user
    )
