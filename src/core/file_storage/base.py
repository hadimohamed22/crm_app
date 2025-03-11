from abc import ABC, abstractmethod
from typing import Dict, Tuple, Optional
from PIL import Image
import io
from . import config

class BaseFileStorage(ABC):
    def __init__(self):
        self.config = config.get("file_storage", {})
        self.enabled = self.config.get("enabled", True)
        thumb_config = self.config.get("thumbnail", {})
        self.thumbnail_enabled = thumb_config.get("enabled", True)
        self.thumbnail_size = tuple(thumb_config.get("size", [200, 200]))

    @abstractmethod
    def upload(self, file_name: str, content: bytes, content_type: str) -> Dict:
        pass

    @abstractmethod
    def download(self, object_name: str) -> Tuple[bytes, str]:
        pass

    @abstractmethod
    def get_url(self, object_name: str) -> str:
        pass

    @abstractmethod
    def delete(self, object_name: str) -> None:
        pass

    def _create_thumbnail(self, content: bytes, content_type: str) -> Optional[bytes]:
        if not self.thumbnail_enabled or "image" not in content_type:
            return None
        img = Image.open(io.BytesIO(content))
        img.thumbnail(self.thumbnail_size)
        thumb_buffer = io.BytesIO()
        img.save(thumb_buffer, format=img.format)
        return thumb_buffer.getvalue()