from fastapi import FastAPI, HTTPException
from database import get_all_tasks, create_task, get_one_task, get_one_task_id, update_task, delete_task
from models import Task

app = FastAPI()


@app.get("/")
def welcome():
    return {"message": "Welcome to FastAPI!"}


@app.get('/api/tasks')
async def get_tasks():
    tasks = await get_all_tasks()
    return tasks


@app.post('/api/tasks', response_model=Task)
async def save_task(task: Task):

    taskFound = await get_one_task(task.title)

    if taskFound:
        raise HTTPException(409, 'Task already exists')

    doc = task.model_dump(by_alias=True, exclude_unset=True, exclude_none=True)
    print(doc)
    response = await create_task(doc)
    if response:
        return Task(**response)
    raise HTTPException(400,'Something went wrong')


@app.get('/api/tasks/{id}')
async def get_task():
    return 'single task'


@app.put('/api/tasks/{id}')
async def update_task():
    return 'updating task'


@app.delete('/api/tasks/{id}')
async def delete_tasks():
    return 'delete task'


