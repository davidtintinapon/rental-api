from fastapi import FastAPI
from app.database import engine, Base
from app.routers import auth

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Rental Management API",
    description="API for managing rental properties, units and leases",
    version="1.0.0"
)

app.include_router(auth.router)

@app.get("/health")
def health_check():
    return {"status": "ok"}