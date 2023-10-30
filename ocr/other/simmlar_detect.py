# import cv2
#
# # 读取两张图像
# image1 = cv2.imread('../image/BoldSingle/3030683Z_blur.png', cv2.IMREAD_COLOR)
# image2 = cv2.imread('../image/BoldSingle/3030683Z.png', cv2.IMREAD_COLOR)
#
# # 提取特征
# sift = cv2.SIFT_create()
#
# keypoints1, descriptors1 = sift.detectAndCompute(image1, None)
# keypoints2, descriptors2 = sift.detectAndCompute(image2, None)
#
# # 使用BFMatcher进行特征匹配
# bf = cv2.BFMatcher()
# matches = bf.knnMatch(descriptors1, descriptors2, k=2)
#
# # 应用比率测试来筛选匹配
# good_matches = []
# for m, n in matches:
#     if m.distance < 0.75 * n.distance:
#         good_matches.append(m)
#
# # 计算相似度得分
# similarity = len(good_matches) / len(keypoints1)
#
# print(f"相似度得分: {similarity}")

import cv2 as cv
import cv2
import numpy as np


def sift_compare(path1: str, path2: str):
    image1 = cv2.imread(path1, cv2.IMREAD_COLOR)
    image2 = cv2.imread(path2, cv2.IMREAD_COLOR)
    sift = cv2.SIFT_create()
    keypoints1, descriptors1 = sift.detectAndCompute(image1, None)
    keypoints2, descriptors2 = sift.detectAndCompute(image2, None)
    # # 使用BFMatcher进行特征匹配
    bf = cv2.BFMatcher()
    matches = bf.knnMatch(descriptors1, descriptors2, k=2)
    # # 应用比率测试来筛选匹配
    good_matches = []
    for m, n in matches:
        if m.distance < 0.8 * n.distance:
            good_matches.append(m)

    # 计算相似度得分
    similarity = len(good_matches) / len(keypoints1)

    print(f"相似度得分: {similarity}")


def sift(title, img_src):
    # 实例化sift
    sift = cv.SIFT_create()
    # 检测关键点
    gray_img = cv.cvtColor(img_src, cv.COLOR_BGR2GRAY)
    kp, des = sift.detectAndCompute(gray_img, None)
    # gray:灰度图像
    # kp:关键点信息（位置、尺度、方向）
    # des:关键点描述符，每个关键点对应28个梯度信息的特征向量
    # 绘制关键点信息
    cv.drawKeypoints(img_src, kp, img_src, flags=cv.DRAW_MATCHES_FLAGS_DRAW_RICH_KEYPOINTS)
    cv.imshow(title, img_src)


if __name__ == '__main__':
    # 读取图像，转换成灰度图
    # img = cv.imread('../image/BoldSingle/3030683Z_blur.png')
    # sift('blur', img)
    #
    # img = cv.imread('../image/BoldSingle/3030683Z.png')
    # sift('source', img)

    sift_compare('../image/BoldSingle/3030683Z_blur.png', '../image/BoldSingle/3030683Z.png')
    sift_compare('../image/BoldSingle/3030683Z.png', '../image/BoldSingle/3030683Z_blur.png')

    cv.waitKey(0)
