import string
import random
from typing import Any

from django.core.files.base import ContentFile
from django.core.paginator import Paginator, Page

from helpers.dates import dt_now


def write_bytes_to_file(data: bytes, file_path: str):
    with open(file_path, 'wb') as f:
        f.write(data)

    return ContentFile(data, name=file_path.split("/")[-1])


def generate_random_chars(length: int = 8) -> str:
    return "".join(
        random.choice(string.ascii_letters + string.digits) for _ in range(length)
    )


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


def paginate(data: Any, page: int = 1, page_size: int = 10) -> tuple[Page, dict[str, Any]]:
    paginator = Paginator(data, page_size)
    page_obj = paginator.get_page(page)
    meta = {
        'page_size': paginator.per_page,
        'current_page': page_obj.number,
        'total_pages': paginator.num_pages
    }

    return page_obj, meta
