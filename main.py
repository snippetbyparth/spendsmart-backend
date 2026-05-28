from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine
from app.models import Base
from app.routers.auth import router as auth_router


# Create all database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="SpendSmart API")

# Allow Flutter app to talk to our API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)

@app.get("/")
def root():
    return {"message": "SpendSmart API is running!"}