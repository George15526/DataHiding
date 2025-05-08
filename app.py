import json
from flask import Flask, render_template, request, redirect, url_for, make_response
from PIL import Image
from utils.histogram_embed import embeded_data
import os
import io
import base64
from utils.bit_text_switch import text_to_bits
from utils.histogram_decode import decode_data
from utils.save_embed_record import save_embed_record
from utils.find_record import find_record_by_image_data

app = Flask(__name__, static_folder='static/')

app.config['UPLOAD_FOLDER'] = 'uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
os.makedirs(os.path.join('static', 'data'), exist_ok=True)
os.makedirs(os.path.join('static', 'img'), exist_ok=True)

def img_to_base64(img):
  buffer = io.BytesIO()
  img.save(buffer, format='PNG')
  return base64.b64encode(buffer.getvalue()).decode()

@app.route('/')
def index():
  return render_template('index.html')

@app.route('/embed', methods=['POST'])
def embed():
  image_file = request.files['image']
  secret_text = request.form['secret_text']
  if image_file.filename == '':
    return redirect(url_for('index'))
  
  filename = image_file.filename
  path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
  image_file.save(path)
  
  original_img = Image.open(path).convert('L')
  print(original_img)
  
  msg_bits = text_to_bits(secret_text)
  
  embeded_img, hist_path = embeded_data(original_img, msg_bits)
  print(hist_path)
  embeded_base64 = img_to_base64(embeded_img)
  
  save_embed_record(
    image_data=embeded_base64,
    secret_text_len=len(secret_text),
    hist_path=hist_path,
    json_path='static/data/data.json'
  )
  
  return render_template(
    'embed_result.html',
    image_data=embeded_base64,
    hist_path=hist_path
  )

@app.route('/decode', methods=['POST'])
def decode():
  image_file = request.files['image']
  if image_file.filename == '':
    return redirect(url_for('index'))
  
  filename = image_file.filename
  path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
  image_file.save(path)
  
  embedded_img = Image.open(path).convert('L')
  
  record = find_record_by_image_data(
    target_image_data=img_to_base64(embedded_img),
    json_path='static/data/data.json'
  )
  
  msg_len = record['secret_text_len'] * 8
  
  decoded_img, secret_text, hist_path = decode_data(embedded_img, msg_len=msg_len)
  
  decoded_base64 = img_to_base64(decoded_img)
  
  return render_template(
    'decode_result.html',
    image_data=decoded_base64,
    secret_text=secret_text,
    hist_path=hist_path
  )

if __name__ == '__main__':
  app.run(
    host='0.0.0.0',
    port=8001,
    debug=True
  )