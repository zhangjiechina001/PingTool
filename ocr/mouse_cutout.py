import cv2
import cv2
import pytesseract
from PIL import Image
from numpy import  ndarray

pytesseract.pytesseract.tesseract_cmd = "C:/Program Files (x86)/Tesseract-OCR/tesseract.exe"


class MouseCutOut:
    def __init__(self, image):
        self.iy = None
        self.ix = None
        self.image = image
        self.drawing = False
        cv2.setMouseCallback("Image", self.draw_rectangle)

    def draw_rectangle(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            self.drawing = True
            self.ix, self.iy = x, y
        elif event == cv2.EVENT_MOUSEMOVE:
            if self.drawing:
                img_copy = self.image.copy()
                cv2.rectangle(img_copy, (self.ix, self.iy), (x, y), (0, 255, 255), 1)
                cv2.imshow("Image", img_copy)
        elif event == cv2.EVENT_LBUTTONUP:
            self.drawing = False
            img_cut = self.image[self.iy:y, self.ix:x]
            print(self.ix, x, self.iy, y)
            self.draw_ocr(img_cut.copy())

    def draw_ocr(self, img):
        # 将OpenCV图像转换为PIL图像
        pil_image = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        custom_config = r'--psm 6 -c tessedit_char_whitelist=0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
        # 获取识别的字符边界框
        detection_boxes = pytesseract.image_to_boxes(pil_image, output_type=pytesseract.Output.STRING,
                                                     config=custom_config)
        print(pytesseract.image_to_string(pil_image, output_type=pytesseract.Output.STRING,
                                                     config=custom_config))
        img_h, img_w, _ = img.shape
        # 遍历每个字符的边界框并绘制方框
        for box in detection_boxes.splitlines():
            box = box.split()
            # 矩形的两个对角点
            x1, y1, x2, y2 = int(box[1]), int(box[2]), int(box[3]), int(box[4])
            cv2.rectangle(img, (x1, img_h - y1), (x2, img_h - y2), (0, 255, 0), 1)
            # cv2.putText(image_cv, x,(x, h), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.putText(img, box[0], (x1, img_h - y1), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 2)

        cv2.imshow("cut", img)


# 读取图像
img = cv2.imread('image/FineBody/Image_20231024161234704.bmp')
resize_img=cv2.resize(img,(1920,1080))
cv2.imshow("Image", resize_img)
cutout = MouseCutOut(resize_img)
cv2.waitKey()
