from .base import BaseFileStorage
import uuid
from minio import Minio
import io
from typing import Tuple, Dict, Optional

class MinioStorage(BaseFileStorage):
    def __init__(self):
        super().__init__()
        minio_config = self.config.get("minio", {})
        self.client = Minio(
            minio_config.get("endpoint", "localhost:9000"),
            access_key=minio_config.get("access_key", "minioadmin"),
            secret_key=minio_config.get("secret_key", "miniopassword"),
            secure=minio_config.get("secure", False)
        )
        self.bucket = minio_config.get("bucket", "crm-bucket")
        self.domain = minio_config.get("domain", f"http://{minio_config.get('endpoint')}/")
        if not self.client.bucket_exists(self.bucket):
            self.client.make_bucket(self.bucket)

    def upload(self, file_name: str, content: bytes, content_type: str) -> Dict:
        object_name = f"{uuid.uuid4()}.{file_name.split('.')[-1]}"
        self.client.put_object(self.bucket, object_name, io.BytesIO(content), len(content), content_type)
        result = {"file_path": f"{self.domain}{self.bucket}/{object_name}", "object_name": object_name}
        thumb_content = self._create_thumbnail(content, content_type)
        if thumb_content:
            thumb_name = f"thumbnails/{object_name}"
            self.client.put_object(self.bucket, thumb_name, io.BytesIO(thumb_content), len(thumb_content), content_type)
            result["thumbnail_path"] = f"{self.domain}{self.bucket}/{thumb_name}"
        return result

    def download(self, object_name: str) -> Tuple[bytes, str]:
        response = self.client.get_object(self.bucket, object_name)
        try:
            return response.read(), response.headers.get("Content-Type", "application/octet-stream")
        finally:
            response.close()
            response.release_conn()

    def get_url(self, object_name: str) -> str:
        return self.client.presigned_get_object(self.bucket, object_name)

    def delete(self, object_name: str) -> None:
        self.client.remove_object(self.bucket, object_name)