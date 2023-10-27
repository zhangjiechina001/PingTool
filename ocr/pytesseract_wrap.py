import pytesseract
import os
import cv2

if os.path.exists("C:/Program Files/Tesseract-OCR/tesseract.exe"):
    pytesseract.pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"
elif os.path.exists("C:/Program Files (x86)/Tesseract-OCR/tesseract.exe"):
    pytesseract.pytesseract.tesseract_cmd = "C:/Program Files (x86)/Tesseract-OCR/tesseract.exe"

print(pytesseract.get_languages(config=''))
print(pytesseract.get_tesseract_version())


class PytesseractWrap:
    def __init__(self):
        pass


def cv_to_pil(cv_src):
    cvt_img = cv2.cvtColor(cv_src, cv2.COLOR_BGR2RGB)
    return cvt_img
