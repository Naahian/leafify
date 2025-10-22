import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth_route, plantguide_route, product_route
from database import create_tables, engine, Base
from app.models import *
import health_check

app = FastAPI()

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Update this with your allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_check.router)
app.include_router(auth_route.router)
app.include_router(product_route.router)
app.include_router(plantguide_route.router)


@app.on_event("startup")
def startup():
    create_tables()


@app.get("/")
def root():
    return {
        "message": "Welcome to the Leafify Backend",
        "health check":
        {
            "/health"          : "basic health check",
            "/health/detailed" : "detailed health status"
            ,"/health/live"     : "Liveness check - for Kubernetes/container(if any)",
            "/health/db-stats" : "Database statistics (Auth Required)"
        },
    }



if __name__ == "__main__":
    import uvicorn
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
