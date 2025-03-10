from fastapi import FastAPI
from .core.config import config
from .core.scheduler import start_scheduler
from .api import auth, profile

app = FastAPI(title="CRM App")

app.include_router(auth.router)
app.include_router(profile.router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the CRM App", "version": "0.1.0"}

@app.on_event("startup")
async def startup_event():
    print("Starting CRM App")
    start_scheduler()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)