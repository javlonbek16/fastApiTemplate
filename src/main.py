from fastapi import FastAPI
from .auth import router as auth_router

app = FastAPI()

# Startup event handler to include auth_router
@app.on_event("startup")
def on_startup():
    print("Starting up...")
    # Include auth_router with prefix and tags
    app.include_router(auth_router.router, prefix="/auth", tags=["auth"])

# Shutdown event handler
@app.on_event("shutdown")
def on_shutdown():
    print("Shutting down...")

# Root endpoint handler
@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI application!"}
