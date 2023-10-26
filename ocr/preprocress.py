import cv2
import numpy as np

# 读取图像并将其转为灰度图像
image = cv2.imread('full_1.png', 0)
# 显示原始图像和开闭运算后的图像
cv2.imshow('Original Image', image)
# 创建一个椭圆形的核（也可以使用其他形状的核）
kernel = np.ones((6, 6), np.uint8)
# 设置阈值
threshold_value = 128
# 二值化
_,image=cv2.threshold(image, threshold_value, 255, cv2.THRESH_BINARY)
# 执行开运算
opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)

# 执行闭运算
closing = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)


cv2.imshow('Opening', opening)
cv2.imshow('Closing', closing)

cv2.waitKey(0)
cv2.destroyAllWindows()


# if __name__=='__main__':
