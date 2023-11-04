from typing import List

import cv2
import numpy as np
from numpy import ndarray
import cv_utils as dfc
from pytesseract_wrap import PytesseractWrap
from ocr.char_valid import FurnaceNumberValid, IndexValid, LengthValid, BrandValid


class RecognizeParam:
    psms = range(1, 14)
    oems = [1, 0]
    brands = ['20CrMoH']

    # 炉号
    TYPE_FURNACE_NUMBER = 1
    # 序列号
    TYPE_INDEX = 2
    # 扁棒长度
    TYPE_LENGTH = 3
    # 牌号
    TYPE_BRAND = 4

    def __init__(self, start, end, whitelist, psm, oem, char_type=0):
        self.start = start
        self.end = end
        self.whitelist = whitelist
        self.psm = psm
        self.oem = oem
        # self.is_brand = is_brand
        self.char_type = char_type

    def compare(self, input) -> bool:
        dic = {
            RecognizeParam.TYPE_FURNACE_NUMBER: FurnaceNumberValid(),
            RecognizeParam.TYPE_INDEX: IndexValid(),
            RecognizeParam.TYPE_LENGTH: LengthValid(),
            RecognizeParam.TYPE_BRAND: BrandValid()
        }
        if self.char_type in dic:
            return dic[self.char_type].valid(input)
        else:
            return True


class CharRecognize:
    '''
    1.寻找边界
    2.过滤边界
    3.边界按行排序
    4.获取角度
    5.放射变换，矫正图像
    6.重复1-3，获取多行分割好的字符
    7.依次对不同行的字符进行分割
    :return:
    '''

    def __init__(self, img: ndarray):
        self.img = img
        self.img_show = img.copy()

    number_char = '0123456789'
    english_capital_char = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    english_lowercase_char = english_capital_char.lower()

    def auto_rotate(self):
        img_copy = self.img.copy()
        binary, contours = dfc.find_contours(img_copy, 100)
        filtered_c = dfc.filter_contours(contours, 5000)
        order_c = dfc.order_contours(filtered_c, 'y')
        angle_avg = dfc.get_angle_avg(order_c)
        center = img_copy.shape[0] / 2, img_copy.shape[1] / 2
        print('angle_avg', angle_avg)
        self.img = dfc.rotate(img_copy, angle_avg, center)
        cv2.imwrite('rotated.png', self.img)
        self.img_show = self.img.copy()

    def split_image_by_y(self, img: ndarray, margin=2):
        binary, contours = dfc.find_contours(img, 100)
        filtered_c = dfc.filter_contours(contours, 5000)
        order_c = dfc.order_contours(filtered_c, 'y')
        (x1, y1), (x2, y2) = self.combine_contours(order_c, 0, 0, margin=10)
        dfc.draw_rect((x1, y1, x2, y2), self.img_show)
        return order_c

    def draw_contours(self, contours: List[np.ndarray]):
        dfc.draw_contours(contours, self.img_show, True)

    def split_image_by_x(self, img: ndarray, margin=2):
        binary, contours = dfc.find_contours(img, 1)
        filtered_c = dfc.filter_contours(contours, 500)
        order_c = dfc.order_contours(filtered_c, 'y')
        ret = []
        for c in order_c:
            x, y, w, h = cv2.boundingRect(c)
            iter_img = img[y - margin:y + h + margin, x - margin:x + w + margin]
            ret.append(iter_img)
        return ret

    def get_split_img(self, img: ndarray, start: int, end: int, margin=1):
        binary, contours = dfc.find_contours(img, 1)
        filtered_c = dfc.filter_contours(contours, 100)
        order_c = dfc.order_contours(filtered_c, 'x')
        x1, y1, _, _ = cv2.boundingRect(order_c[start])
        x, y, w, h = cv2.boundingRect(order_c[end])
        x2, y2 = x + w, y + h
        ret = img[y1 - margin:y2 + margin, x1 - margin:x2 + margin].copy()
        return ret

    def recognize_row1(self, img_src):
        ret = ''
        number_img = self.get_split_img(img_src, 0, 6, margin=0)
        cv2.imshow('number_img', number_img)
        tessacter = PytesseractWrap(cv2_img=number_img)
        tessacter.set_enable_wordlist(True)
        tessacter.set_whitelist(CharRecognize.number_char)
        ret += tessacter.image_to_string(13, 0, isTrim=True)
        alphabet_img = self.get_split_img(img_src, 7, 7, margin=0)
        tessacter = PytesseractWrap(cv2_img=alphabet_img)
        tessacter.set_enable_wordlist(True)
        tessacter.set_whitelist(CharRecognize.english_capital_char)
        ret += tessacter.image_to_string(10, 0, isTrim=True)
        print(ret)

    def get_image(self, img: ndarray, contours, start: int, end: int, margin=1):
        (x1, y1), (x2, y2) = self.combine_contours(contours, start, end)
        ret = img[y1 - margin:y2 + margin, x1 - margin:x2 + margin]
        return ret

    def combine_contours(self, contours, start: int, end: int, margin=0):
        x1, y1, _, _ = cv2.boundingRect(contours[start])
        end=end if end<len(contours)-1 else len(contours)-1
        x, y, w, h = cv2.boundingRect(contours[end])
        x2, y2 = x + w, y + h
        correct = lambda val: val if val >= 0 else 0

        return (correct(x1 - margin), correct(y1 - margin)), (x2 + margin, y2 + margin)

    def recognize_row_contours1(self, contour, params: List[RecognizeParam]):
        (x_start, y_start), (x_end, y_end) = self.combine_contours([contour], 0, 0, 10)
        img_ = self.img[y_start:y_end, x_start:x_end]

        if len(params) == 1:
            dfc.draw_rect((x_start, y_start, x_end, y_end), self.img_show)
            ret = self.recognize_img(params[0], img_)
            print(ret)
            return ret

        _, contours = dfc.find_contours(img_, 1)
        order_contours = dfc.order_contours(contours, 'x')
        order_contours = dfc.filter_contours(order_contours, 300)

        ret = ''
        for p in params:
            start, end = p.start, p.end
            (x1, y1), (x2, y2) = self.combine_contours(order_contours, start, end, margin=10)
            (x1, y1), (x2, y2) = (x1 + x_start, y1 + y_start), (x2 + x_start, y2 + y_start)
            margin = 0
            number_img = self.img[y1 - margin:y2 + margin, x1 - margin:x2 + margin]
            dfc.draw_rect((x1 - margin, y1 + margin, x2 - margin, y2 + margin), self.img_show)
            ret += self.recognize_img(p, img=number_img)
            ret += ' '
        print(ret)
        return ret

    def recognize_img(self, p: RecognizeParam, img: ndarray):
        tessacter = PytesseractWrap(img)
        tessacter.set_whitelist(p.whitelist)
        tessacter.set_enable_wordlist(True)
        recognize_result = tessacter.image_to_string(p.psm, p.oem, isTrim=True)
        if p.compare(recognize_result):
            return recognize_result

        for oem in p.oems:
            for i in p.psms:
                recognize_result = tessacter.image_to_string(i, oem, isTrim=True)
                if p.compare(recognize_result):
                    return recognize_result
        return recognize_result

    def recognize_row2(self, img_src):
        tessacter = PytesseractWrap(cv2_img=img_src)
        tessacter.set_enable_wordlist(True)
        tessacter.set_whitelist(CharRecognize.number_char)
        ret = tessacter.image_to_string(13, 0)
        print(ret.replace("\n", ""))

    def recognize_row3(self, img_src):
        tessacter = PytesseractWrap(cv2_img=img_src)
        tessacter.set_enable_wordlist(True)
        tessacter.set_whitelist("")
        ret = tessacter.image_to_string(8, 1)
        print(ret.replace("\n", ""))
