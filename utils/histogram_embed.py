import numpy as np
from PIL import Image
import matplotlib
import matplotlib.pyplot as plt
import os
from utils.plot_factor import plot_factor

matplotlib.use('Agg')

def embeded_data(img: Image.Image, msg_bits: str, peak: int) -> tuple[str, Image.Image, str]:
  img_np = np.array(img)
  print(img_np)
  
  flat = img_np.flatten()
  print(flat)
  
  original_hist_path = os.path.join('static', 'img', 'embedded_hist_original.png')
  plot_factor(flat, original_hist_path)
  
  hist, _ = np.histogram(flat, bins=256, range=(0, 256))
  print('hist:\n', hist)
  
  if peak is None:
    peak = np.argmax(hist)
  print(peak)
  
  hist_left = hist[0: peak]
  hist_right = hist[peak + 1::]
  
  zero_left = np.argmin(hist_left)
  zero_right = np.argmin(hist_right) + peak
  
  print(zero_left, zero_right)
  
  embedded = img_np.copy()
  
  for val in range(zero_left + 1, peak, 1):
    embedded[embedded == val] -= 1
  
  for val in range(zero_right - 1, peak, -1):
    embedded[embedded == val] += 1
    
  print(embedded)
    
  header_bits = msg_bits[0: 33]
  header_bits_left = header_bits[:16]
  header_bits_right = header_bits[16:]
  
  secret_bits = msg_bits[32:]
  print('secret_bits:', secret_bits, len(secret_bits))
  
  secret_bits_half_len = len(secret_bits) // 2
  msg_left = header_bits_left + secret_bits[:secret_bits_half_len]
  msg_right = header_bits_right + secret_bits[secret_bits_half_len:]
  print('msg_left:', msg_left, len(msg_left))
  print('msg_right:', msg_right, len(msg_right))
  
  idx_left = np.argwhere(embedded == peak - 2)
  idx_right = np.argwhere(embedded == peak + 2)
  
  print(idx_left)
  print(idx_right)
  
  if len(msg_left) > len(idx_left) or len(msg_right) > len(idx_right):
    raise ValueError("資訊太長，超出容量")
  
  for i, bit in enumerate(msg_left):
    if bit == '1':
      x, y = idx_left[i]
      embedded[x, y] += 1
  
  for i, bit in enumerate(msg_right):
    if bit == '1':
      x, y = idx_right[i]
      embedded[x, y] -= 1
  
  print(msg_bits)
  print(len(msg_bits))
  print(embedded)
  
  new_img = Image.fromarray(embedded.astype('uint8'))
  print(new_img)
  
  hist_filename = f'embeded_hist_new.png'
  new_hist_path = os.path.join('static', 'img', hist_filename)
    
  plot_factor(embedded, new_hist_path)
  
  return peak, new_img, new_hist_path