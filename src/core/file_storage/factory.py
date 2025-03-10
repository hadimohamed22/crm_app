from .minio import MinioStorage
from . import config

def get_file_storage():
    backend = config.get("file_storage", {}).get("backend", "minio")
    if backend == "minio":
        return MinioStorage()
    raise ValueError(f"Unsupported backend: {backend}")

file_storage = get_file_storage()