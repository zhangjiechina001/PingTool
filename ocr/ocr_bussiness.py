import traceback

from numpy import ndarray
import cv2
import numpy as np
from typing import Tuple
import cv_utils as dfc
from char_recognize import CharRecognize, RecognizeParam
import cv_utils
from char_grid import CharGrid

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


class OcrProcess:
    '''
    1.识别区域定位，截取
    2.歪斜矫正
    3.网格划分
    4.字符识别
    '''

    def __init__(self,img_src=ndarray):
        self.img_src=img_src
        img_copy=img_src.copy()
        x1, y1, x2, y2 = cv_utils.location(img_copy, -30)
        self.img_location = img_copy[y1:y2, x1:x2]
        self.img_rotated = cv_utils.auto_rotate(self.img_location)
        self.grid=CharGrid(self.img_rotated)


def recognize(img_char: ndarray) -> Tuple[ndarray, SampleResult]:
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
    ocr_p=OcrProcess(img_src)
    # img_show = location(img_src)
    cv2.imshow('img_src', ocr_p.img_src)
    cv2.imshow('img_location', ocr_p.img_location)
    cv2.imshow('img_rotated', ocr_p.img_rotated)
    cv2.imshow('img_grid', ocr_p.grid.img_show)
    cv2.waitKey()
