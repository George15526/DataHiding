import json
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
import os
from utils.bit_text_switch import bits_to_text
from utils.plot_factor import plot_factor

def decode_data(img: Image.Image, peak: int) -> tuple[str, str]:
  img_np = np.array(img, dtype=np.uint8)
  print(img_np)
  
  flat = img_np.flatten()
  print(flat)
  
  hist, _ = np.histogram(flat, bins=256, range=(0, 256))
  print(hist)
  
  if peak is None:
    peak = np.argmax(hist)
  print(peak)
  
  header_bits = []
  extracted_bits = []
  
  decoded = img_np.copy()
  idx_left = np.argwhere((decoded == peak - 1) | (decoded == peak - 2))
  idx_right = np.argwhere((decoded == peak + 1) | (decoded == peak + 2))
  
  
  # 處理 header_bits(秘密訊息長度)
  header_half_len = 32 // 2
  header_count_left, header_count_right = 0, 0
  
  for i in range(len(idx_left)):
    x, y = idx_left[i]
    val = decoded[x, y]
    if val == peak - 2:
      header_bits.append('0')
    elif val == peak - 1:
      decoded[x, y] -= 1
      header_bits.append('1')
    
    header_count_left += 1
    
    if header_count_left >= header_half_len:
      break
    
  for i in range(len(idx_right)):
    x, y = idx_right[i]
    val = decoded[x, y]
    if val == peak + 2:
      header_bits.append('0')
    elif val == peak + 1:
      decoded[x, y] += 1
      header_bits.append('1')
    
    header_count_right += 1
    
    if header_count_right >= header_half_len:
      break
  
  header_bitstring = ''.join(header_bits)
  print(header_bitstring)
  
  msg_len = int(header_bitstring, 2) * 8
  print('msg_len:', msg_len)
  
  
  # 處理 msg_bits(秘密訊息部分)
  half_len = msg_len // 2
  count_left, count_right = 0, 0

  for i in range(header_half_len, len(idx_left)):
    x, y = idx_left[i]
    val = decoded[x, y]
    if val == peak - 2:
      extracted_bits.append('0')
    elif val == peak - 1:
      decoded[x, y] -= 1
      extracted_bits.append('1')
    
    count_left += 1
    
    if count_left >= half_len:
      break
    
  for i in range(header_half_len + 1, len(idx_right)):
    x, y = idx_right[i]
    val = decoded[x, y]
    if val == peak + 2:
      extracted_bits.append('0')
    elif val == peak + 1:
      decoded[x, y] += 1
      extracted_bits.append('1')
    
    count_right += 1
    
    if count_right >= half_len:
      break
  
  hist_left = hist[:peak - 1]
  hist_right = hist[peak + 2:]
  zero_left = np.argmin(hist_left)
  zero_right = np.argmin(hist_right) + peak
  print(hist_right)
  print(zero_left)
  print(zero_right)
  
  for val in range(peak - 2, zero_left, -1):
    decoded[decoded == val] += 1
    
  for val in range(peak + 2, zero_right, 1):
    decoded[decoded == val] -= 1
    
  print(decoded)
  
  decoded_img = Image.fromarray(decoded.astype('uint8'))
  print(decoded_img)
  
  decoded_hist_path = os.path.join('static', 'img', 'decoded_hist.png')
  plot_factor(decoded, decoded_hist_path)
  
  bitstring = ''.join(extracted_bits)
  print(bitstring)
  
  secret_text = bits_to_text(bitstring)
  print('secret_text:', secret_text, len(secret_text))
  
  return decoded_img, secret_text, decoded_hist_path