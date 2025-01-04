from motor.motor_asyncio import AsyncIOMotorClient
from models import Task

client = AsyncIOMotorClient('mongodb://localhost')
# client.<nombre de la base de datos>
database = client.farmtest 
# database.<nombre de la colección/tabla>
collection = database.tasks

async def get_one_task_id(id):
    task = await collection.find_one({'_id': id})
    return task



async def get_all_tasks():
    tasks = []
    cursor = collection.find({})

    async for document in cursor:
        tasks.append(Task(**document))

    return tasks



async def create_task(task):
    new_task = await collection.insert_one(task)
    created_task = await collection.find_one({'_id': new_task.inserted_id})
    return created_task



async def update_task(id: str, task):
    await collection.update_one({'_id': id}, {'$set': task})
    document = await collection.find_one({'_id': id})
    return document



async def delete_task(id: str):
    await collection.delete_one({'_id': id})
    return True