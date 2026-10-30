from fastapi import HTTPException, status
from repositories import TaskRepository
from models import Task
from schemas import TaskCreate, TaskUpdate, TaskRead


class TaskService:
    def __init__(self, task_repository: TaskRepository):
        self.task_repository = task_repository

    def view_task(self, task_id: int):
        task = self.task_repository.get_task_by_id(task_id)
        if task is None:
            raise HTTPException(status_code=404, detail=f"task {task_id} does not exist")
        return task


    def view_all_tasks(self):
        tasks = self.task_repository.get_all_tasks()
        if tasks is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="There aren't any tasks yet")
        return tasks


    def create_task(self, data:TaskCreate) ->Task:
        new_task = Task(title = data.title, done = data.done)
        return self.task_repository.add_task(new_task)


    def update_task(self, id: int, data: TaskUpdate) -> Task:
        to_update = self.view_task(id)
        return self.task_repository.update_task(to_update, data)


    def delete_task(self, id: int):
        to_delete = self.view_task(id)
        deleted = TaskRead.model_validate(to_delete)
        self.task_repository.delete_task(to_delete)
        return deleted

