import cv2
import numpy as np
from numpy import ndarray
from other import deflection_correction as dfc
from pytesseract_wrap import PytesseractWrap


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

    def auto_rotate(self):
        img = self.img.copy()
        binary, contours = dfc.find_contours(img, 100)
        filtered_c = dfc.filter_contours(contours, 5000)
        order_c = dfc.order_contours(filtered_c, 'y')
        angle_avg = dfc.get_angle_avg(order_c)
        center = img.shape[0] / 2, img.shape[1] / 2
        # dfc.draw_contours(order_c,img,True)
        print('angle_avg', angle_avg)
        return dfc.rotate(img, angle_avg, center)

    def split_image_by_y(self, img: ndarray, margin=2):
        binary, contours = dfc.find_contours(img, 100)
        filtered_c = dfc.filter_contours(contours, 5000)
        order_c = dfc.order_contours(filtered_c, 'y')
        ret = []
        for c in order_c:
            x, y, w, h = cv2.boundingRect(c)
            iter_img = img[y - margin:y + h + margin, x - margin:x + w + margin]
            ret.append(iter_img)
        return ret

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

    def get_split_img(self,img:ndarray,margin=1):
        binary, contours = dfc.find_contours(img, 1)
        filtered_c = dfc.filter_contours(contours, 500)
        order_c = dfc.order_contours(filtered_c, 'x')
        x1,y1,_,_=cv2.boundingRect(order_c[0])
        x,y,w,h=cv2.boundingRect(order_c[6])
        x2,y2=x+w,y+h
        ret=img[y1 - margin:y2 + margin, x1 - margin:x2 + margin].copy()
        return ret
    def recognize_row1(self, img_src):
        first_img = self.get_split_img(img_src, 0)
        cv2.imshow('first_img',first_img)
        tessacter = PytesseractWrap(cv2_img=first_img)
        tessacter.set_enable_wordlist(True)
        tessacter.set_whitelist('0123456789')
        print(tessacter.image_to_string(13,0))
        # ret=[]
        # for img in col_imgs[0:-2]:
        #     tessacter=PytesseractWrap(cv2_img=img)
        #     tessacter.set_enable_wordlist(True)
        #     tessacter.set_whitelist('0123456789')
        #     ret.append(tessacter.image_to_string(12,1))
        #
        # for img in col_imgs[-2:]:
        #     tessacter=PytesseractWrap(cv2_img=img)
        #     tessacter.set_enable_wordlist(True)
        #     tessacter.set_whitelist('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
        #     ret.append(tessacter.image_to_string(12,1))
        #
        # print(ret)


if __name__ == '__main__':
    img = cv2.imread('full4.bmp')
    recognize = CharRecognize(img)
    rotated_img = recognize.auto_rotate()
    cv2.imshow('rotated', rotated_img)
    row_imgs = recognize.split_image_by_y(rotated_img)
    recognize.recognize_row1(row_imgs[0])
    cv2.waitKey()
