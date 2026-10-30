from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker
from schemas import TaskUpdate
from config import get_settings
from models import Task

engine = create_engine(get_settings().database_url, pool_pre_ping=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_task_by_id(self, task_id: int) -> Task | None:
        return self.db.query(Task).filter(Task.id == task_id).first()

    def get_all_tasks(self) -> list[Task] | None:
        return self.db.query(Task).order_by(Task.id).all()

    def add_task(self, new_task:Task) -> Task:
        self.db.add(new_task)
        self.db.commit()
        self.db.refresh(new_task)
        return new_task

    def update_task(self, to_update: Task, data: TaskUpdate) -> Task:
        update_data = data.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(to_update, key, value)
            
        self.db.commit()
        self.db.refresh(to_update)
        return to_update


    def delete_task(self, to_delete:Task):
        id = to_delete.id
        self.db.delete(to_delete)
        self.db.commit()