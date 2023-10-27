# 字体粗细识别
import cv2
import pytesseract

img_src = cv2.imread('./image/BoldSingle/3030683Z.bmp')
print(pytesseract.image_to_osd(img_src))