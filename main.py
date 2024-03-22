import os
from typing import Optional
from fastapi import FastAPI
from models import Story, Task
from database import db
from jose import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from dotenv import load_dotenv

load_dotenv()

secret_key = os.getenv('SECRET_KEY')

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_token(token: str = Depends(oauth2_scheme)):
  try:
    payload = jwt.decode(token, secret_key, algorithms=["HS256"])
    return payload
  except jwt.JWTError:
    raise HTTPException(
      status_code=status.HTTP_403_FORBIDDEN,
      detail="Invalid token"
    )

app = FastAPI(dependencies=[Depends(verify_token)])

@app.get("/stories/")
async def read_stories() -> dict:
  return db

@app.post("/stories/")
async def create_story(story: Story) -> Story:
  db[story.id] = story
  return story

@app.put("/stories/{story_id}")
async def update_story(story_id: int, story: Story) -> Story:
  db[story_id] = story
  return story

@app.delete("/stories/{story_id}")
async def delete_story(story_id: int) -> None:
  return db.pop(story_id, None)

@app.post("/stories/{story_id}/tasks/")
async def create_task(story_id: int, task: Task) -> Task:
  db[story_id].tasks.append(task)
  return task

@app.put("/stories/{story_id}/tasks/{task_id}")
async def update_task(story_id: int, task_id: int, task: Task) -> Optional[Task]:
  for i, existing_task in enumerate(db[story_id].tasks):
    if existing_task.id == task_id:
      db[story_id].tasks[i] = task
      return task
  return None

@app.delete("/stories/{story_id}/tasks/{task_id}")
async def delete_task(story_id: int, task_id: int) -> None:
  db[story_id].tasks = [task for task in db[story_id].tasks if task.id != task_id]
  return None