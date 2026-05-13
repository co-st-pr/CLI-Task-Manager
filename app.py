from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import json, os

app = FastAPI(title="practice")

class TaskCreate(BaseModel):
    task: str
    done: bool | None = None

file_name = "tasks.json"

def load_tasks(file_name):
    if not os.path.exists(file_name):
        return []
    with open(file_name, "r") as f: return json.load(f)

def save_tasks(task_list, file_name):
    with open(file_name, "w") as f: return json.dump(task_list, f)

def add(task, file_name, done = None):
    tasks = load_tasks(file_name)
    task_id = len(tasks)+1
    task_dict = {"id":task_id, "title": task, "done":done}
    tasks.append(task_dict)
    save_tasks(tasks, file_name)

def list_tasks(file_name):
    task_list = json.load(file_name)
    if not task_list:
        print(f"No tasks in file")
        return
    
    for task in task_list:
        if task["done"]:
            print(f"[{task['id']}] [✔] {task['title']}")

        else:
            print(f"[{task['id']}] [ ] {task['title']}")
    





@app.get("/")
async def root():
    print("Welcome")


@app.get("/tasks")
async def load(file_name):
    list_tasks(file_name)

@app.get("/tasks/{task_id}")
async def load_task(task_id, file_name):
    task_list = load_tasks(file_name)
    task = [t for t in task_list if t["id"] == task_id]



@app.post("/tasks", status_code=201)
async def create_task(body: TaskCreate):
    add(body.task, file_name, body.done)


@app.put("/tasks/{task_id}")
async def update_task(task_id:int):
    task_list = load_tasks(file_name)
    task = next((t for t in task_list if t["id"] == task_id), None)
    if not task: raise HTTPException(404, "task not found")
    task["done"] = True
    add(task_list, file_name)
    return task

@app.delete("/tasks/{task_id}")
async def delete_task(task_id:int):
    task_list = load_tasks(file_name)
    new_task_list = [t for t in task_list if t['id'] != task_id]
    if len(task_list) == len(new_task_list): raise HTTPException(404, "task not found")
    for i, t in enumerate(new_task_list):
        t["id"] = i+1
    save_tasks(new_task_list, file_name)



@app.exception_handler(Exception)
async def global_handler(equest, exc):
    from fastapi.responses import JSONResponse
    return JSONResponse(status_code= 500,
                        content = {"detail":"Internal Server Error"})


