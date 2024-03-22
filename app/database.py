import json
from app.models import Story

with open('initial_data.json', encoding='utf-8') as f:
  data = json.load(f)

db = {story['id']: Story(**story) for story in data}
