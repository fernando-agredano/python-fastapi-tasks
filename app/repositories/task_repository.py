from sqlalchemy.orm import Session
from typing import Optional, List
from app.models.task import Task, TaskStatus, TaskPriority


class TaskRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, task_id: int) -> Optional[Task]:
        return self.db.query(Task).filter(Task.id == task_id).first()

    def get_all_by_owner(
        self,
        owner_id: int,
        status: Optional[TaskStatus] = None,
        priority: Optional[TaskPriority] = None,
        skip: int = 0,
        limit: int = 20
    ) -> List[Task]:
        query = self.db.query(Task).filter(Task.owner_id == owner_id)
        if status:
            query = query.filter(Task.status == status)
        if priority:
            query = query.filter(Task.priority == priority)
        return query.offset(skip).limit(limit).all()

    def create(self, title: str, owner_id: int, description: Optional[str], priority: TaskPriority) -> Task:
        task = Task(title=title, description=description, priority=priority, owner_id=owner_id)
        self.db.add(task)
        self.db.commit()
        self.db.refresh(task)
        return task

    def update(self, task: Task, **fields) -> Task:
        for key, value in fields.items():
            if value is not None:
                setattr(task, key, value)
        self.db.commit()
        self.db.refresh(task)
        return task

    def delete(self, task: Task) -> None:
        self.db.delete(task)
        self.db.commit()
