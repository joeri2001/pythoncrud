from typing import List, Optional
from pydantic import BaseModel

class Task(BaseModel):
  id: int
  name: str
  points: Optional[int] = None
  tags: List[str] = []

class Story(BaseModel):
  id: int
  name: str
  tasks: List[Task] = []
  points: Optional[int] = None
  tags: List[str] = []
  epic: bool = False
