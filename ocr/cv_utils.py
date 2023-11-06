from typing import List

import cv2
import numpy as np
from numpy import ndarray


def find_contours(image: ndarray, kernel_size: int):
    kernel = np.ones((1, kernel_size), np.uint8)
    # 执行膨胀操作cv2.erode,
    acts = [cv2.dilate, cv2.erode]
    gray = cvt2gray(image)
    iter_img = gray.copy()
    for act in acts:
        iter_img = act(iter_img, kernel, iterations=1)
        # 使用OpenCV进行字符位置检测

    # THRESH_OTSU的效果比较好,而且不需要调参数
    _, binary = cv2.threshold(iter_img, 0, 255, cv2.THRESH_OTSU)
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


def draw_contours(contours, image, isRect: bool, margin=0):
    # 遍历轮廓并绘制实际轮廓
    index = 0
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if isRect:
            draw_rect((x + margin, y + margin, x + w - margin, y + h - margin), image)
        else:
            cv2.drawContours(image, [contour], -1, (0, 0, 255), 1)

        cv2.putText(image, str(index), (x, y), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                    color=(0, 0, 255))  # 绿色文本)
        index += 1

    return image


def get_rect(contour: ndarray, margin=0):
    x, y, w, h = cv2.boundingRect(contour)
    correct=lambda x:x if x>0 else 0
    return correct(x + margin), correct(y + margin), x + w - margin, y + h - margin


def draw_rect(pos, image):
    x1, y1, x2, y2 = pos
    cv2.rectangle(image, (x1, y1), (x2, y2), (255, 255, 0), 1)  # 绘制带方向的外接矩形


def get_angles(contours: List[np.ndarray]):
    ret = []
    for contour in contours:
        rotated_rect = cv2.minAreaRect(contour)  # 计算带方向的外接矩形
        center, size, angle = rotated_rect
        if angle < -45:
            angle += 90  # 使角度范围在-45到45度之间
        ret.append((angle, center))
    return ret


def get_angle_avg(contours: List[np.ndarray]):
    angles = get_angles(contours)
    angle_avg = np.mean([angle for angle, _ in angles])
    return angle_avg


def rotate(img: ndarray, angle, center):
    # 创建仿射变换矩阵
    M = cv2.getRotationMatrix2D(center, angle, 1.0)
    # 执行仿射变换
    rectified_region = cv2.warpAffine(img.copy(), M, (img.shape[1], img.shape[0]))
    return rectified_region


def correct(img: ndarray):
    binary, contours = find_contours(img, 40)
    filtered_c = filter_contours(contours, 5000)
    order_c = order_contours(filtered_c, 'y')
    angle = get_angle_avg(order_c)
    center = img.shape[0] / 2, img.shape[1] / 2
    # 执行仿射变换
    rectified_region = rotate(img, angle, center)
    return rectified_region


def location(image: ndarray, margin: int, size=14):
    # 使用腐蚀和膨胀来处理图像
    kernel_size = 2 * size + 1  # 计算核的大小（奇数值）
    kernel = np.ones((kernel_size, kernel_size), np.uint8)

    image_copy = image.copy()
    img_gray = cvt2gray(image_copy)
    _, binary_img = cv2.threshold(img_gray, 0, 255, cv2.THRESH_OTSU)
    # 执行腐蚀和膨胀
    kernel1 = np.ones((5, 5), np.uint8)
    eroded_image = cv2.erode(binary_img, kernel1, iterations=1)
    dilated_image = cv2.dilate(eroded_image, kernel, iterations=1)
    contours, _ = cv2.findContours(dilated_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    max_contour = max(contours, key=lambda x: cv2.contourArea(x))
    x1, y1, x2, y2 = get_rect(max_contour, margin)

    return x1, y1, x2, y2


def auto_rotate(img: ndarray):
    img_copy = img.copy()
    binary, contours = find_contours(img_copy, 100)
    filtered_c = filter_contours(contours, 5000)
    order_c = order_contours(filtered_c, 'y')
    angle_avg = get_angle_avg(order_c)
    center = img_copy.shape[0] / 2, img_copy.shape[1] / 2
    print('angle_avg', angle_avg)
    rotated_img = rotate(img_copy, angle_avg, center)
    return rotated_img,angle_avg


def cvt2gray(img_src: ndarray):
    return img_src.copy() if len(img_src.shape) == 2 else cv2.cvtColor(img_src, cv2.COLOR_BGR2GRAY)


if __name__ == '__main__':
    # pass
    img = cv2.imread('../image/ThinSingle/3030138Z_blur.png')
    binary, contours = find_contours(img, 40)
    filtered_c = filter_contours(contours, 5000)
    order_c = order_contours(filtered_c, 'y')

    cv2.imshow('image', draw_contours(order_c, img.copy(), isRect=True))
    angles = get_angles(order_c)
    angle_avg = np.mean([angle for angle, _ in angles])
    center = angles[0][1]
    center = img.shape[0] / 2, img.shape[1] / 2
    # 执行仿射变换
    rectified_region = rotate(img, angle_avg, center)
    cv2.imshow(f'Rectified Region', rectified_region)
    rectified_regions = []
    cv2.waitKey()
