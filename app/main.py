from fastapi import FastAPI
from contextlib import asynccontextmanager
from app.routers import posts, users, auth
from app.database import init_db

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("🚀 App starting... creating DB if needed.")
    init_db()   
    yield
    print("👋 App shutting down...")

app = FastAPI(title="Cenmark", lifespan=lifespan)

app.include_router(auth.router)
app.include_router(users.router)
app.include_router(posts.router)


@app.get("/")
async def root():
    return {"message": "Welcome to cenmark!"}