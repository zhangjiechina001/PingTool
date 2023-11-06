import cv2
from numpy import ndarray

from ocr import cv_utils
from ocr.char_grid import CharGrid

def img_corrrect90(img: ndarray):
    img_copy = img.copy()
    x1, y1, x2, y2 = cv_utils.location(img_copy, -30)
    w = x2 - x1
    h = y2 - y1
    if w < h:
        center = ((x1 + x2) / 2, (y1 + y2) / 2)
        return cv_utils.rotate(img_copy, -90, center)
    return img_copy


def img_corrrect180(img: ndarray):
    img_copy = img.copy()
    rotated_img,_ = cv_utils.auto_rotate(img_copy)
    grid=CharGrid(rotated_img)
    img = grid.get_image(1,3,1,3)

    _,binary_img=cv2.threshold(cv_utils.cvt2gray(img),200,255,cv2.THRESH_BINARY)
    cv2.imshow('img_(1,3,1,3)', binary_img)
    # 计算值为1的像素数量
    ones_pixels = cv2.countNonZero(binary_img)
    # 计算1的比例
    ratio = ones_pixels / binary_img.size
    if ratio>0.05:
        x1, y1, x2, y2 = cv_utils.location(img_copy, -30)
        center = ((x1 + x2) / 2, (y1 + y2) / 2)
        cv_utils.rotate(img_copy,-180,)
    print('ratio:',ratio)
    return None


if __name__ == '__main__':
    img_src = cv2.imread('skew.png')
    img_c = img_corrrect90(img_src)
    img_c1=img_corrrect180(img_c)
    cv2.imshow('corrected', img_c)
    cv2.waitKey()
