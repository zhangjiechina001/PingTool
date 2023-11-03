import cv2
import numpy as np

# 读取图像
image = cv2.imread("full_1.png", cv2.IMREAD_GRAYSCALE)

# 使用Sobel算子进行边缘检测
sobel_x = cv2.Sobel(image, cv2.CV_64F, 1, 0, ksize=3)
sobel_y = cv2.Sobel(image, cv2.CV_64F, 0, 1, ksize=3)

# 计算梯度幅度
gradient_magnitude = np.sqrt(sobel_x ** 2 + sobel_y ** 2)

# 应用阈值来得到二值图像
threshold = 50
binary_image = cv2.threshold(gradient_magnitude, threshold, 255, cv2.THRESH_BINARY)[1]

# 显示原始图像和检测到的边缘
cv2.imshow("Original Image", image)
cv2.imshow("Edge Detection", binary_image)
cv2.waitKey(0)
cv2.destroyAllWindows()
