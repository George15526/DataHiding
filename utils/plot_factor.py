import matplotlib.pyplot as plt

def plot_factor(embedded, hist_path):
  plt.hist(embedded.flatten(), bins=256, color='blue')
  plt.title('Histogram after Embedding')
  plt.savefig(hist_path)
  plt.close()