from numpy import ndarray
import cv2
import numpy as np
import other.deflection_correction as dfc


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
    max_contour = max(contours, lambda x: cv2.contourArea(x))
    x,y,w,h=cv2.boundingRect(max_contour)
    ret=image_copy[y:y+h,x:x+w]
    return ret
    # dfc.draw_contours([max_contour], image_copy, True, margin=0)
    # # 显示处理后的图像
    # cv2.imshow("src image", image_copy)
    # cv2.imshow("dealed Image", dilated_image)
    # return


if __name__ == '__main__':
    img_src = cv2.imread('full_1.png',cv2.IMREAD_GRAYSCALE)
    img_char = location(img_src)
    cv2.imshow('img_char',img_char)
    cv2.waitKey()