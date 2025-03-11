import uvicorn
from .core.config import config

app_config = config.get("app", {})

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host=app_config.get("host", "0.0.0.0"),
        port=app_config.get("port", 8000),
        reload=True
    )