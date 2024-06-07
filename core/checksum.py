import hashlib


def compute_checksum(file_path: str) -> str:
    sha256_hash = hashlib.sha256()
    with open(file_path, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()


def verify_checksum(file_path: str, expected_checksum: str) -> bool:
    computed_checksum = compute_checksum(file_path)
    if computed_checksum == expected_checksum:
        return True

    return False
