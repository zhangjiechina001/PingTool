import traceback

from numpy import ndarray
import cv2
import numpy as np
from typing import Tuple

import other.deflection_correction as dfc
from char_recognize import CharRecognize, RecognizeParam


class SampleResult:
    def __init__(self, furnace_number='', index='', length='', brand=''):
        self.img_recognized = None
        self.img_src = None
        self.furnace_number = furnace_number
        self.index = index
        self.length = length
        self.brand = brand

    def set_img_src(self, img_src: ndarray):
        self.img_src = img_src.copy()

    def set_img_recognized(self, img_recognized: ndarray):
        self.img_recognized = img_recognized.copy()

    def get_map(self):
        ret = []
        map1 = {
            '炉号': self.furnace_number,
            '序号': self.index,
            '长度': self.length,
            '牌号': self.brand
        }
        ret.append(map1)
        return ret

    @staticmethod
    def get_header():
        ret = ['炉号', '序号', '长度', '牌号']
        return ret


def location(image: ndarray, size=14):
    # 使用腐蚀和膨胀来处理图像
    kernel_size = 2 * size + 1  # 计算核的大小（奇数值）
    kernel = np.ones((kernel_size, kernel_size), np.uint8)

    image_copy = image.copy()
    img_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    _, binary_img = cv2.threshold(img_gray, 0, 255, cv2.THRESH_OTSU)
    # 执行腐蚀和膨胀
    kernel1 = np.ones((5, 5), np.uint8)
    eroded_image = cv2.erode(binary_img, kernel1, iterations=1)
    dilated_image = cv2.dilate(eroded_image, kernel, iterations=1)
    contours, _ = cv2.findContours(dilated_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    max_contour = max(contours, key=lambda x: cv2.contourArea(x))
    x, y, w, h = cv2.boundingRect(max_contour)
    ret = image_copy[y:y + h, x:x + w]
    return ret


def recognize(img_char: ndarray) -> Tuple[ndarray,SampleResult]:
    recognize = CharRecognize(img_char)
    recognize.auto_rotate()
    ocr_ret = SampleResult()
    try:
        row_imgs = recognize.split_image_by_y(recognize.img)
        # 单个字符h=80 w=50
        row1_params = [
            RecognizeParam(0, 6, CharRecognize.number_char, 13, 1, char_type=RecognizeParam.TYPE_FURNACE_NUMBER),
            RecognizeParam(7, 7, CharRecognize.english_capital_char, 13, 0,
                           char_type=RecognizeParam.TYPE_FURNACE_NUMBER)]
        ret_row1 = recognize.recognize_row_contours1(row_imgs[0], row1_params)
        ocr_ret.furnace_number = ret_row1

        row2_params = [RecognizeParam(0, 2, CharRecognize.number_char, 13, 1, char_type=RecognizeParam.TYPE_INDEX),
                       RecognizeParam(3, 6, CharRecognize.number_char, 13, 1, char_type=RecognizeParam.TYPE_LENGTH)]
        # cv2.imshow('row2', row_imgs[1])
        ret_row2 = recognize.recognize_row_contours1(row_imgs[1], row2_params)
        ocr_ret.index = ret_row2.split(' ')[0]
        ocr_ret.length = ret_row2.split(' ')[1]

        white_c = CharRecognize.number_char + CharRecognize.english_capital_char + CharRecognize.english_lowercase_char
        row3_params = [RecognizeParam(0, 6, white_c, 13, 1, char_type=RecognizeParam.TYPE_BRAND)]
        ret_row3 = recognize.recognize_row_contours1(row_imgs[2], row3_params)
        ocr_ret.brand = ret_row3
        ocr_ret.set_img_src(img_char)
        ocr_ret.set_img_recognized(recognize.img_show)

    except Exception as err:
        print(err, err.__traceback__)
        traceback.print_tb(err.__traceback__)

    return recognize.img_show, ocr_ret


if __name__ == '__main__':
    img_src = cv2.imread('12.png', cv2.IMREAD_COLOR)
    img_char = location(img_src)
    cv2.imshow('img_char', img_char)

    recognized_img, _ = recognize(img_char)
    cv2.imshow('recognized', recognized_img)
    cv2.waitKey()
