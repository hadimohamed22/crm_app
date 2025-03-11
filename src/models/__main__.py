from fastapi import FastAPI
from contextlib import asynccontextmanager
from ..core.config import config
from ..core.scheduler import start_scheduler
from ..api import auth, profile
from ..models import init_db

app_config = config.get("app", {})

# Run synchronous initialization before async lifespan
init_db()  # Call this outside async context

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Starting CRM App")
    start_scheduler()  # Async-compatible startup tasks go here
    yield
    print("Shutting down CRM App")

app = FastAPI(
    title=app_config.get("title", "CRM App"),
    description=app_config.get("description", "A FastAPI-based CRM application with user authentication and profile management."),
    version=app_config.get("version", "0.1.0"),
    docs_url=app_config.get("docs_url", "/docs"),
    openapi_tags=[
        {"name": "Authentication", "description": "User registration and login"},
        {"name": "Profiles", "description": "Manage CRM profiles"}
    ],
    lifespan=lifespan
)

app.include_router(auth.router)
app.include_router(profile.router)

@app.get("/")
async def read_root():
    return {"message": f"Welcome to the {app_config.get('title', 'CRM App')}", "version": app_config.get("version", "0.1.0")}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=app_config.get("host", "0.0.0.0"),
        port=app_config.get("port", 8000)
    )