import json
from flask import Flask, render_template, request, redirect, url_for, make_response
from PIL import Image
from utils.histogram_embed import embeded_data
import os
import io
import base64
from utils.bit_text_switch import text_to_bits
from utils.histogram_decode import decode_data

app = Flask(__name__, static_folder='static/')

app.config['UPLOAD_FOLDER'] = 'uploads/'
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
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
  peak = request.form['peak']
  if peak == '':
    peak = None
  else:
    peak = int(peak)
  
  if image_file.filename == '':
    return redirect(url_for('index'))
  
  filename = image_file.filename
  path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
  image_file.save(path)
  
  original_img = Image.open(path).convert('L')
  print(original_img)
  
  msg_len = len(secret_text)
  header_bits = format(msg_len, '032b')
  
  msg_bits = header_bits + text_to_bits(secret_text)
  
  peak, embeded_img, hist_path = embeded_data(
    img=original_img,
    msg_bits=msg_bits,
    peak=peak
  )
  print(hist_path)
  embeded_base64 = img_to_base64(embeded_img)

  return render_template(
    'embed_result.html',
    peak=peak,
    image_data=embeded_base64,
    hist_path=hist_path
  )

@app.route('/decode', methods=['POST'])
def decode():
  image_file = request.files['image']
  peak = request.form['peak']
  
  if image_file.filename == '':
    return redirect(url_for('index'))
  
  if peak == '':
    peak = None
  else:
    peak = int(peak)
  
  filename = image_file.filename
  path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
  image_file.save(path)
  
  embedded_img = Image.open(path).convert('L')
  
  decoded_img, secret_text, hist_path = decode_data(
    embedded_img,
    peak=peak
  )
  
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