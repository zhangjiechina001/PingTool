import cv2
import numpy as np
import ocr.cv_utils as dfc


def draw_grid(image:np.ndarray):
    # 定义网格的行数和列数
    rows, cols = 3, 8

    # 计算网格的间距
    spacing_x = image.shape[1] // cols
    spacing_y = image.shape[0] // rows
    # 绘制水平线
    for i in range(1, rows):
        y = i * spacing_y
        cv2.line(image, (0, y), (image.shape[1], y), (200, 255, 0), 1)

    # 绘制垂直线
    for i in range(1, cols):
        x = i * spacing_x
        cv2.line(image, (x, 0), (x, image.shape[0]), (200, 0, 255), 1)

# 初始化回调函数，将在Trackbar值更改时调用
def on_trackbar_change(x):
    # 使用腐蚀和膨胀来处理图像
    kernel_size = 2 * x + 1  # 计算核的大小（奇数值）
    kernel = np.ones((kernel_size, kernel_size), np.uint8)

    image_copy = image.copy()
    _, binary_img = cv2.threshold(image_copy, 0, 255, cv2.THRESH_OTSU)
    # 执行腐蚀和膨胀
    kernel1 = np.ones((5, 5), np.uint8)
    eroded_image = cv2.erode(binary_img, kernel1, iterations=1)
    dilated_image = cv2.dilate(eroded_image, kernel, iterations=1)
    # dilated_image = cv2.erode(dilated_image, kernel, iterations=1)
    contours, _ = cv2.findContours(dilated_image, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    dfc.draw_contours(contours, image_copy, True, margin=6)

    x1,y1,x2,y2=dfc.get_rect(contours[0],6)
    draw_grid(image_copy[y1:y2,x1:x2])
    # 显示处理后的图像
    cv2.imshow("src image", image_copy)
    cv2.imshow("dealed Image", dilated_image)


# 读取图像
image = cv2.imread("../rotated_11.png", cv2.IMREAD_GRAYSCALE)

# 创建图像窗口
cv2.namedWindow("src image")
cv2.namedWindow("dealed Image")

# 创建Trackbar来调节核的大小
cv2.createTrackbar("Kernel Size", "src image", 0, 20, on_trackbar_change)

# 初始化Trackbar位置
on_trackbar_change(0)

cv2.waitKey(0)
cv2.destroyAllWindows()
