import json
from app.models import Story

with open('initial_data.json') as f:
  data = json.load(f)

db = {story['id']: Story(**story) for story in data}