import numpy as np
import pytesseract
from pytesseract import Output
import cv2

pytesseract.pytesseract.tesseract_cmd="C:/Program Files (x86)/Tesseract-OCR/tesseract.exe"
try:
    from PIL import Image
    from PIL import ImageDraw
    from PIL import ImageFont
except ImportError:
    import Image

img = cv2.imread('full2.jpg')

gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)[1]
cnts = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = cnts[0] if len(cnts) == 2 else cnts[1]

width_list = []
for c in cnts:
	_, _, w, _ = cv2.boundingRect(c)
	width_list.append(w)
wm = np.median(width_list)

# 配置白名单以只识别数字和英文字符
# custom_config = r'--psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
custom_config =r'--psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
tess_text = pytesseract.image_to_data(img, output_type=Output.DICT,config=custom_config)
for i in range(len(tess_text['text'])):
	word_len = len(tess_text['text'][i])
	if word_len > 1:
		world_w = int(wm * word_len)
		(x, y, w, h) = (tess_text['left'][i], tess_text['top'][i], tess_text['width'][i], tess_text['height'][i])
		cv2.rectangle(img, (x, y), (x + world_w, y + h), (255, 0, 0), 1)
		im = Image.fromarray(img)
		draw = ImageDraw.Draw(im)
		font = ImageFont.truetype(font="simsun.ttc", size=18, encoding="utf-8")
		draw.text((x, y - 20), tess_text['text'][i], (255, 0, 0), font=font)
		img = cv2.cvtColor(np.array(im), cv2.COLOR_RGB2BGR)

print(tess_text['text'])
cv2.imshow("TextBoundingBoxes", img)
cv2.imwrite('fullimg_deal.bmp',img)
cv2.waitKey(0)
