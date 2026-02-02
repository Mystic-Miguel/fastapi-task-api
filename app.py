from fastapi import FastAPI
from pydantic import BaseModel
from typing import Dict

app = FastAPI(title="Task API")
class Task(BaseModel):
    title: str
    done: bool = False

DB: Dict[str, Task] = {}

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/tasks")
def list_tasks():
    return DB

@app.post("/tasks")
def create_task(task: Task):
    tid = str(len(DB)+1)
    DB[tid] = task
    return {"id": tid, **task.dict()}
