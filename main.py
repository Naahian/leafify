from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes import auth, item, user
from database import engine, Base

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
app.include_router(auth.router)
app.include_router(item.router)
app.include_router(user.router)

@app.on_event("startup")
async def startup():
    # Create the database tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI application!"}