import traceback

from numpy import ndarray
import cv2
import numpy as np
import other.deflection_correction as dfc
from char_recognize import CharRecognize, RecognizeParam


def location(image: ndarray, size=14):
    # 使用腐蚀和膨胀来处理图像
    kernel_size = 2 * size + 1  # 计算核的大小（奇数值）
    kernel = np.ones((kernel_size, kernel_size), np.uint8)

    image_copy = image.copy()
    _, binary_img = cv2.threshold(image_copy, 0, 255, cv2.THRESH_OTSU)
    # 执行腐蚀和膨胀
    kernel1 = np.ones((5, 5), np.uint8)
    eroded_image = cv2.erode(binary_img, kernel1, iterations=1)
    dilated_image = cv2.dilate(eroded_image, kernel, iterations=1)
    contours, _ = cv2.findContours(dilated_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    max_contour = max(contours, key=lambda x: cv2.contourArea(x))
    x, y, w, h = cv2.boundingRect(max_contour)
    ret = image_copy[y:y + h, x:x + w]
    return ret


if __name__ == '__main__':
    img_src = cv2.imread('full_1.png', cv2.IMREAD_GRAYSCALE)
    img_char = location(img_src)
    cv2.imshow('img_char', img_char)

    recognize=CharRecognize(img_char)
    recognize.auto_rotate()
    cv2.imshow('rotated',recognize.img_show)

    try:
        row_imgs = recognize.split_image_by_y(recognize.img)
        # 单个字符h=80 w=50
        row1_params = [RecognizeParam(0, 6, CharRecognize.number_char, 13, 1,char_type=RecognizeParam.TYPE_FURNACE_NUMBER),
                       RecognizeParam(7, 7, CharRecognize.english_capital_char, 13, 0,char_type=RecognizeParam.TYPE_FURNACE_NUMBER)]
        recognize.recognize_row_contours1(row_imgs[0], row1_params)

        row2_params = [RecognizeParam(0, 2, CharRecognize.number_char, 13, 1,char_type=RecognizeParam.TYPE_INDEX),
                       RecognizeParam(3, 6, CharRecognize.number_char, 13, 1,char_type=RecognizeParam.TYPE_LENGTH)]
        # cv2.imshow('row2', row_imgs[1])
        recognize.recognize_row_contours1(row_imgs[1], row2_params)

        white_c= CharRecognize.number_char + CharRecognize.english_capital_char + CharRecognize.english_lowercase_char
        row3_params = [RecognizeParam(0, 6,white_c,12, 1,char_type=RecognizeParam.TYPE_BRAND)]
        recognize.recognize_row_contours1(row_imgs[2], row3_params)

    except Exception as err:
        print(err, err.__traceback__)
        traceback.print_tb(err.__traceback__)

    cv2.imshow('recognized', recognize.img_show)
    cv2.waitKey()
