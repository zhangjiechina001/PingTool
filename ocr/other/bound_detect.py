import cv2
import numpy as np

# 读取图像
image = cv2.imread("3030138Z_blur.png")
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 进行边缘检测（使用Canny算法）
edges = cv2.Canny(gray, threshold1=50, threshold2=150, apertureSize=3)

# 进行Hough线变换
lines = cv2.HoughLines(edges, 1, np.pi / 180, threshold=100)

# 绘制直线
for line in lines:
    rho, theta = line[0]
    a = np.cos(theta)
    b = np.sin(theta)
    x0 = a * rho
    y0 = b * rho
    x1 = int(x0 + 1000 * (-b))
    y1 = int(y0 + 1000 * (a))
    x2 = int(x0 - 1000 * (-b))
    y2 = int(y0 - 1000 * (a))
    cv2.line(image, (x1, y1), (x2, y2), (0, 0, 255), 2)

# 显示图像
cv2.imshow("Hough Lines", image)
cv2.waitKey(0)
cv2.destroyAllWindows()

