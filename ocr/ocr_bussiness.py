import traceback

from numpy import ndarray
import cv2
import numpy as np
from typing import Tuple, List
import cv_utils as dfc
from char_recognize import CharRecognize
import cv_utils
from char_grid import CharGrid
from ocr.char_valid import FurnaceNumberValid, IndexValid, LengthValid, BrandValid
from ocr.pytesseract_wrap import PytesseractWrap


class SampleResult:
    def __init__(self, furnace_number='', index='', length='', brand='', angle=0):
        self.img_recognized = None
        self.img_src = None
        self.furnace_number = furnace_number
        self.index = index
        self.length = length
        self.brand = brand
        self.angle = angle

    def set_img_src(self, img_src: ndarray):
        self.img_src = img_src.copy()

    def set_img_recognized(self, img_recognized: ndarray):
        self.img_recognized = img_recognized.copy()

    def get_map(self):
        map1 = {
            '炉号': self.furnace_number,
            '序号': self.index,
            '长度': self.length,
            '牌号': self.brand,
            '倾斜角度': self.angle
        }
        return map1

    @staticmethod
    def get_header():
        ret = ['炉号', '序号', '长度', '牌号','倾斜角度']
        return ret

    def __str__(self):
        return str(self.get_map())


class OcrRecognizeParam:
    psms = range(1, 14)
    oems = [1, 0]
    brands = ['20CrMoH']

    char_number = '0123456789'
    char_english_capital = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    char_english_lowercase = char_english_capital.lower()

    # 炉号
    TYPE_FURNACE_NUMBER = 1
    # 序列号
    TYPE_INDEX = 2
    # 扁棒长度
    TYPE_LENGTH = 3
    # 牌号
    TYPE_BRAND = 4

    def __init__(self, start_pos, end_pos, whitelist, psm, oem, char_type=0, margin=(0, 0)):
        self.start = start_pos
        self.end = end_pos
        self.whitelist = whitelist
        self.psm = psm
        self.oem = oem
        # self.is_brand = is_brand
        self.char_type = char_type
        self.margin = margin

    def valid(self, input) -> bool:
        dic = {
            OcrRecognizeParam.TYPE_FURNACE_NUMBER: FurnaceNumberValid(),
            OcrRecognizeParam.TYPE_INDEX: IndexValid(),
            OcrRecognizeParam.TYPE_LENGTH: LengthValid(),
            OcrRecognizeParam.TYPE_BRAND: BrandValid()
        }
        if self.char_type in dic:
            return dic[self.char_type].valid(input)
        else:
            return True


class OcrProcess:
    """
    1.识别区域定位，截取
    2.歪斜矫正
    3.网格划分
    4.字符识别
    """

    def __init__(self, img_src: ndarray):
        self.sample_result = None
        self.img_src = img_src
        img_copy = img_src.copy()
        x1, y1, x2, y2 = cv_utils.location(img_copy, -30)
        self.img_location = img_copy[y1:y2, x1:x2]
        self.img_rotated, self.angle = cv_utils.auto_rotate(self.img_location)
        self.grid = CharGrid(self.img_rotated)

    def recognize(self) -> SampleResult:
        brand_white_list = OcrRecognizeParam.char_number + OcrRecognizeParam.char_english_capital + OcrRecognizeParam.char_english_lowercase
        params = [
            OcrRecognizeParam((0, 0), (0, 6), OcrRecognizeParam.char_number, 13, 1,
                              char_type=OcrRecognizeParam.TYPE_FURNACE_NUMBER),
            OcrRecognizeParam((0, 7), (0, 7), OcrRecognizeParam.char_english_capital, 10, 0,
                              char_type=OcrRecognizeParam.TYPE_FURNACE_NUMBER),
            OcrRecognizeParam((1, 0), (1, 2), OcrRecognizeParam.char_number, 13, 1,
                              char_type=OcrRecognizeParam.TYPE_INDEX),
            OcrRecognizeParam((1, 4), (1, 7), OcrRecognizeParam.char_number, 13, 1,
                              char_type=OcrRecognizeParam.TYPE_LENGTH, margin=(14, 6)),
            OcrRecognizeParam((2, 0), (2, 7), brand_white_list, 13, 1, char_type=OcrRecognizeParam.TYPE_BRAND),
        ]
        recognize_result = []
        for p in params:
            recognize_result.append(self.recognize_img(p))
        self.sample_result = SampleResult(recognize_result[0] + recognize_result[1], recognize_result[2],
                                          recognize_result[3], recognize_result[4], self.angle)
        self.sample_result.set_img_src(self.img_location)
        self.sample_result.set_img_recognized(self.grid.img_show)
        print(self.sample_result)
        return self.sample_result

    def recognize_img(self, p: OcrRecognizeParam):
        (start_row, start_col), (end_row, end_col) = p.start, p.end
        img_ = self.grid.get_image(start_row, start_col, end_row, end_col, margin=p.margin)
        tessacter = PytesseractWrap(img_)
        tessacter.set_whitelist(p.whitelist)
        tessacter.set_enable_wordlist(True)
        recognize_result = tessacter.image_to_string(p.psm, p.oem, isTrim=True)
        if p.valid(recognize_result):
            return recognize_result

        for oem in p.oems:
            for i in p.psms:
                recognize_result = tessacter.image_to_string(i, oem, isTrim=True)
                if p.valid(recognize_result):
                    return recognize_result
        return recognize_result

    def draw_rect(self):
        pass


if __name__ == '__main__':
    img_src = cv2.imread('12.png', cv2.IMREAD_COLOR)
    ocr_p = OcrProcess(img_src)
    # img_show = location(img_src)
    cv2.imshow('img_src', ocr_p.img_src)
    cv2.imshow('img_location', ocr_p.img_location)
    cv2.imshow('img_rotated', ocr_p.img_rotated)
    cv2.imshow('grid', ocr_p.grid.img_show)
    cv2.waitKey()
