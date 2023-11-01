from typing import List

import cv2
import numpy as np
from numpy import ndarray


def find_contours(image: ndarray, kernel_size: int):
    kernel = np.ones((1, kernel_size), np.uint8)
    # 执行膨胀操作cv2.erode,
    acts = [cv2.dilate, cv2.erode]
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    iter_img = gray.copy()
    for act in acts:
        iter_img = act(iter_img, kernel, iterations=1)
        # 使用OpenCV进行字符位置检测

    # THRESH_OTSU的效果比较好,而且不需要调参数
    _, binary = cv2.threshold(iter_img, 0, 255, cv2.THRESH_OTSU)
    print(binary.shape)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    return binary, contours


def filter_contours(contours: List[np.ndarray], threshold: int):
    filtered_contours = []
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        if h > 40 and w > 10 and cv2.contourArea(c) > threshold:
            filtered_contours.append(c)
    return filtered_contours


def order_contours(contours: List[np.ndarray], direction: str):
    def contour_sort_key(contour):
        x, y, w, h = cv2.boundingRect(contour)
        return x if direction == 'x' else y

    # 使用自定义排序函数对轮廓列表进行排序
    sorted_contours = sorted(contours, key=contour_sort_key)
    return sorted_contours


def draw_contours(contours, image, isRect: bool):
    # 遍历轮廓并绘制实际轮廓
    index = 0
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        if isRect:
            rotated_rect = cv2.minAreaRect(contour)
            center, size, angle = rotated_rect
            print('angle:', angle)
            box = cv2.boxPoints(rotated_rect)  # 获取外接矩形的四个顶点
            box = np.intp(box)
            cv2.drawContours(image, [box], 0, (0, 255, 0), 2)  # 绘制带方向的外接矩形
        else:
            cv2.drawContours(image, [contour], -1, (0, 0, 255), 2)

        cv2.putText(image, str(index), (x, y), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                    color=(0, 255, 0))  # 绿色文本)
        index += 1

    return image


def get_angle(contours: List[np.ndarray]):
    ret = []
    for contour in contours:
        rotated_rect = cv2.minAreaRect(contour)  # 计算带方向的外接矩形
        center, size, angle = rotated_rect
        if angle < -45:
            angle += 90  # 使角度范围在-45到45度之间
        print(angle)
        ret.append(angle)
    return ret

# def deflection(img:ndarray,):



if __name__ == '__main__':
    img = cv2.imread('../image/ThinSingle/3030138Z_blur.png')
    binary, contours = find_contours(img, 40)
    filtered_c = filter_contours(contours, 5000)
    order_c = order_contours(filtered_c, 'y')

    cv2.imshow('image', draw_contours(order_c, img.copy(), isRect=True))

    rectified_regions = []
    for contour in order_c:
        rotated_rect = cv2.minAreaRect(contour)  # 计算带方向的外接矩形
        center, size, angle = rotated_rect
        if angle < -45:
            angle += 90  # 使角度范围在-45到45度之间
        print(angle)
        # 创建仿射变换矩阵
        M = cv2.getRotationMatrix2D(center, angle, 1.0)

        # 执行仿射变换
        rectified_region = cv2.warpAffine(img.copy(), M, (img.shape[1], img.shape[0]))

        # 截取校正后的区域
        x, y, w, h = cv2.boundingRect(contour)
        # rectified_region = rectified_region[y:y + h, x:x + w]
        # rectified_region = rectified_region[y:y + h, x:x + w]

        # 存储校正后的区域
        rectified_regions.append(rectified_region)

    # 显示校正后的区域
    for i, region in enumerate(rectified_regions):
        cv2.imshow(f'Rectified Region {i}', region)

    cv2.waitKey()
# ordered_c=order_contours(filtered_c,)
