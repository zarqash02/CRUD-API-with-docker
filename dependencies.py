from fastapi import Depends
from sqlalchemy.orm import Session
from repositories import TaskRepository, get_db
from service import TaskService


def get_repository(db: Session = Depends(get_db)) -> TaskRepository:
    return TaskRepository(db)


def get_service(repo: TaskRepository = Depends(get_repository)) -> TaskService:
    return TaskService(repo)