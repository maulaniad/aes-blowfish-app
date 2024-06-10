import os
import string
import random
from typing import Any

from django.core.files.base import ContentFile, File
from django.core.paginator import Paginator, Page

from core.aes128 import AES
from helpers.dates import dt_now


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
