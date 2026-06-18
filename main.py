from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.database import engine, Base
from app.routes.auth_routes import router as auth_router
from app.routes.task_routes import router as task_router

import app.models.user
import app.models.task

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="P1 — Task Manager API",
    description="API de gestión de tareas con arquitectura en capas (Layered Architecture)",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router)
app.include_router(task_router)


@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "project": "P1 - FastAPI Layered Architecture"}
