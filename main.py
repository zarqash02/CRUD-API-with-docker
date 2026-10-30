from contextlib import asynccontextmanager
from fastapi import FastAPI
from config import get_settings
from models import Base
from repositories import engine, seed_tasks
from routes import router

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    seed_tasks()
    yield

app = FastAPI(title=settings.app_name, lifespan=lifespan)
app.include_router(router)