import json
import os

def find_record_by_image_data(target_image_data: str, json_path: str):
  with open(json_path, 'r', encoding='utf-8') as f:
    records = json.load(f)
  
  for record in records:
    if record['image_data'] == target_image_data:
      return record
    
  return None