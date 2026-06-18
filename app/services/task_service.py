from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app.repositories.task_repository import TaskRepository
from app.models.task import TaskStatus, TaskPriority
from app.schemas.task_schema import TaskCreate, TaskUpdate, TaskResponse


class TaskService:
    def __init__(self, db: Session):
        self.repo = TaskRepository(db)

    def get_all(
        self,
        owner_id: int,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
        skip: int = 0,
        limit: int = 20
    ) -> List[TaskResponse]:
        tasks = self.repo.get_all_by_owner(owner_id, status, priority, skip, limit)
        return [TaskResponse.model_validate(t) for t in tasks]

    def get_one(self, task_id: int, owner_id: int) -> TaskResponse:
        task = self.repo.get_by_id(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
        if task.owner_id != owner_id:
            raise HTTPException(status_code=403, detail="No tienes acceso a esta tarea")
        return TaskResponse.model_validate(task)

    def create(self, data: TaskCreate, owner_id: int) -> TaskResponse:
        task = self.repo.create(data.title, owner_id, data.description, data.priority)
        return TaskResponse.model_validate(task)

    def update(self, task_id: int, data: TaskUpdate, owner_id: int) -> TaskResponse:
        task = self.repo.get_by_id(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
        if task.owner_id != owner_id:
            raise HTTPException(status_code=403, detail="No tienes acceso a esta tarea")
        updated = self.repo.update(
            task,
            title=data.title,
            description=data.description,
            status=data.status,
            priority=data.priority
        )
        return TaskResponse.model_validate(updated)

    def delete(self, task_id: int, owner_id: int) -> dict:
        task = self.repo.get_by_id(task_id)
        if not task:
            raise HTTPException(status_code=404, detail="Tarea no encontrada")
        if task.owner_id != owner_id:
            raise HTTPException(status_code=403, detail="No tienes acceso a esta tarea")
        self.repo.delete(task)
        return {"message": "Tarea eliminada correctamente"}
