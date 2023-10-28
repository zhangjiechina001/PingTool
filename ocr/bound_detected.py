import cv2
import numpy as np

# 读取图像
image = cv2.imread('image/BoldSingle/3030683Z.png')

cv2.imshow('image', image)


def callBack(x):
    global image
    # 定义膨胀和腐蚀的核（结构元素）
    kernel = np.ones((x, x), np.uint8)
    # 执行膨胀操作
    dilated = cv2.dilate(image, kernel, iterations=1)
    # 执行腐蚀操作
    eroded = cv2.erode(dilated, kernel, iterations=1)

    # 使用OpenCV进行字符位置检测
    gray = cv2.cvtColor(eroded, cv2.COLOR_BGR2GRAY)
    _, binary = cv2.threshold(gray, 180, 255, cv2.THRESH_BINARY)
    contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    image_copy = image.copy()
    # 处理检测到的字符位置
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)
        if w * h < 100:
            continue
        cv2.rectangle(image_copy, (x, y), (x + w, y + h), (0, 255, 0), 2)
        print(f"字符位置: 左上角 ({x}, {y}), 右下角 ({x + w}, {y + h})")
    cv2.imshow('image', image_copy)


cv2.namedWindow('image', cv2.WINDOW_NORMAL)
cv2.namedWindow('image')
cv2.createTrackbar('reszieThreshold', 'image', 0, 40, callBack)

cv2.waitKey()
