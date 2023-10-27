# 字体粗细识别
import cv2
import pytesseract
import pytesseract_wrap
from pytesseract import Output

from PIL import Image

image_to_test = Image.open('./image/hanzi.png')
osd = pytesseract.image_to_osd(image_to_test, lang='eng', config='--oem 0')
print(osd)
cmd = r'--oem {0} -c tessedit_char_whitelist={1} '.format(0, '0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZ')
