import json
import os

def save_embed_record(image_data: str, secret_text_len: int, hist_path: str, json_path: str):
  record = {
    "image_data": image_data,
    "secret_text_len": secret_text_len,
    "hist_path": hist_path
  }
  
  if os.path.exists(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
      data = json.load(f)
  else:
    data = []
    
  data.append(record)
  
  with open(json_path, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
    
  print('Record saved successfully!')