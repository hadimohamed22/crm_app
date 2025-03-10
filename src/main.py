from fastapi import FastAPI
from contextlib import asynccontextmanager
from .core.config import config
from .core.scheduler import start_scheduler
from .api import auth, profile
from .models.init import init_db

# Define the lifespan handler
@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    print("Starting CRM App")
    init_db()  # Initialize database tables
    start_scheduler()  # Start the scheduler
    yield
    # Shutdown logic (optional, add if needed)
    print("Shutting down CRM App")

app = FastAPI(
    title="CRM App",
    description="A FastAPI-based CRM application with user authentication and profile management.",
    version="0.1.0",
    docs_url="/docs",
    openapi_tags=[
        {"name": "Authentication", "description": "User registration and login"},
        {"name": "Profiles", "description": "Manage CRM profiles"}
    ],
    lifespan=lifespan  # Pass the lifespan handler here
)

app.include_router(auth.router)
app.include_router(profile.router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the CRM App", "version": "0.1.0"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)