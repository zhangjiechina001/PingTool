import cv2
import numpy as np

# 读取灰度图像
image = cv2.imread("../rotated_11.png", cv2.IMREAD_GRAYSCALE)

# 通过阈值将灰度图像转换为二值图像
threshold_value = 128
_, binary_image = cv2.threshold(image, threshold_value, 255, cv2.THRESH_OTSU)

# 定义一个卷积核，可以根据需要进行调整
kernel = np.ones((5, 5), np.uint8)

# 执行开操作
opening_result = cv2.morphologyEx(binary_image, cv2.MORPH_OPEN, kernel)

# 执行闭操作
closing_result = cv2.morphologyEx(binary_image, cv2.MORPH_CLOSE, kernel)

# 显示原始图像、二值图像、开操作结果和闭操作结果
cv2.imshow("Original Image", image)
cv2.imshow("Binary Image", binary_image)
cv2.imshow("Opening Result", opening_result)
cv2.imshow("Closing Result", closing_result)

cv2.waitKey(0)
cv2.destroyAllWindows()
