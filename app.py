from uuid import uuid4
from typing import Dict

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, constr

app = FastAPI(
    title="Task API",
    version="0.1.0",
    description="Tiny demo API for portfolio (create, list, get, update, delete).",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

class Task(BaseModel):
    title: constr(min_length=1, max_length=200) = Field(..., example="Write docs")
    done: bool = Field(False, example=False)

class TaskOut(Task):
    id: str

DB: Dict[str, Task] = {}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/tasks", response_model=Dict[str, Task], tags=["Tasks"])
def list_tasks():
    return DB

@app.get("/tasks/{tid}", response_model=TaskOut, tags=["Tasks"])
def get_task(tid: str):
    if tid not in DB:
        raise HTTPException(status_code=404, detail="Not found")
    return {"id": tid, **DB[tid].dict()}

@app.post("/tasks", response_model=TaskOut, status_code=201, tags=["Tasks"])
def create_task(task: Task):
    tid = str(uuid4())
    DB[tid] = task
    return {"id": tid, **task.dict()}

@app.put("/tasks/{tid}", response_model=TaskOut, tags=["Tasks"])
def update_task(tid: str, task: Task):
    if tid not in DB:
        raise HTTPException(status_code=404, detail="Not found")
    DB[tid] = task
    return {"id": tid, **task.dict()}

@app.delete("/tasks/{tid}", status_code=204, tags=["Tasks"])
def delete_task(tid: str):
    if tid not in DB:
        raise HTTPException(status_code=404, detail="Not found")
    del DB[tid]
