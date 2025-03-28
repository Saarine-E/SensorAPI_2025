from fastapi import FastAPI
from contextlib import asynccontextmanager
from .database.database import create_db
from .routers import sensors

@asynccontextmanager
async def lifespan(app:FastAPI):
    create_db()
    yield

app = FastAPI(lifespan=lifespan)

app.include_router(sensors.router)