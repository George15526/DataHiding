def text_to_bits(text: str) -> str:
  return ''.join(format(ord(c), '08b') for c in text)

def bits_to_text(bits: str) -> str:
  chars = [chr(int(bits[i: i + 8], 2)) for i in range(0, len(bits), 8)]
  return ''.join(chars)