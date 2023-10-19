import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
import pywt
import pywt.data


# Load image
# 读取图像文件
image = Image.open(r"C:\Users\GS-YF-ZJ\Pictures\Saved Pictures\mount.jpg")  # 替换为你的图像文件路径

original = np.array(image)

# Wavelet transform of image, and plot approximation and details
titles = ['Approximation', ' Horizontal detail',
          'Vertical detail', 'Diagonal detail']
coeffs2 = pywt.dwt2(original, 'bior1.3')
LL, (LH, HL, HH) = coeffs2
fig = plt.figure(figsize=(12, 3))
for i, a in enumerate([LL, LH, HL, HH]):
    ax = fig.add_subplot(1, 4, i + 1)
    ax.imshow(a, interpolation="nearest", cmap=plt.cm.gray)
    ax.set_title(titles[i], fontsize=1)
    ax.set_xticks([])
    ax.set_yticks([])

fig.tight_layout()
plt.show()