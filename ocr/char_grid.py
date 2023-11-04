import cv2
import numpy as np
from numpy import ndarray
import cv_utils


class CharGrid:
    def __init__(self, img_src: ndarray):
        self.rows = 3
        self.cols = 8
        self.img_src = img_src
        self.img_char, self.rect_loc = self.location(img_src)

        # 绘制水平线
        for row in range(self.rows):
            for col in range(self.cols):
                rect = self.get_rect(row, col)
                cv_utils.draw_rect(rect, self.img_char)

    def get_rect(self, row: int, col: int):
        x1, y1, x2, y2 = self.rect_loc
        # 计算网格的间距
        spacing_x = (x2 - x1) // self.cols
        spacing_y = (y2 - y1) // self.rows
        ret_x1 = x1 + col * spacing_x
        ret_y1 = y1 + row * spacing_y
        return ret_x1, ret_y1, ret_x1 + spacing_x, ret_y1 + spacing_y

    def get_image(self, row_start, col_start, row_end, col_end):
        rect1 = self.get_rect(row_start, col_start)
        rect2 = self.get_rect(row_end, col_end)
        x1, y1 = rect1[0], rect1[1]
        x2, y2 = rect2[2], rect2[3]
        return self.img_src[y1:y2, x1:x2]

    def location(self, img_src: ndarray):
        img_cpoy = img_src.copy()
        # size-margin=5
        x1, y1, x2, y2 = cv_utils.location(img_cpoy, margin=12)
        return img_cpoy, (x1, y1, x2, y2)


if __name__ == '__main__':
    img_src = cv2.imread('rotated_1.png', cv2.IMREAD_GRAYSCALE)
    char_grid = CharGrid(img_src)
    cv2.imshow('src', char_grid.img_src)
    cv2.imshow('located', char_grid.img_char)
    cv2.imshow('(0,1,2,5)', char_grid.get_image(0, 1, 2, 5))
    cv2.waitKey()
