from fastapi import APIRouter, Depends, status
from dependencies import get_service
from schemas import TaskRead, TaskCreate, TaskUpdate
from service import TaskService

router = APIRouter(prefix="/tasks", tags=["tasks"])


@router.get("", response_model=list[TaskRead])
def get_all_tasks(service: TaskService = Depends(get_service)):
    return service.view_all_tasks()



@router.get("/{id}", response_model=TaskRead)
def get_task(id: int, service: TaskService = Depends(get_service)):
    return service.view_task(id)


@router.post("", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
def add_task(payload: TaskCreate, service: TaskService = Depends(get_service)):
    return service.create_task(payload)


@router.put("/{id}", response_model=TaskRead, status_code=status.HTTP_200_OK)
def update_task(id: int, payload: TaskUpdate, service: TaskService = Depends(get_service)):
    return service.update_task(id, payload)


@router.delete("/{id}", response_model=TaskRead, status_code=status.HTTP_200_OK)
def delete_task(id: int, service: TaskService = Depends(get_service)):
    return service.delete_task(id)