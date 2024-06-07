from django.core.files.base import ContentFile


def write_bytes_to_file(data: bytes, file_path: str):
    with open(file_path, 'wb') as f:
        f.write(data)

    return ContentFile(data, name=file_path.split("/")[-1])
