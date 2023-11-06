import sys
from typing import List

import cv2
import numpy as np
from numpy import ndarray
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidgetItem, QListWidget
from PyQt5.QtGui import QIcon, QPixmap, QImage
from ocr.mouse_cutout import MouseCutOut
from ocr.data.ocr_result import OcrResult
from ocr.pytesseract_wrap import PytesseractWrap

import ocr.ui_helper as ui_helper
from split_ui import Ui_MainWindow
import ocr.cv_utils


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.mouse_cutout = MouseCutOut()
        self.img_src = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        # self.ui.btnRecognize.clicked.connect(self.recognize)
        self.ui.btnOpenFile.clicked.connect(self.open_file)

        self.ui.sliderBinary.valueChanged.connect(lambda x: self.__binary(self.ui.sliderBound.value(), x))
        self.ui.sliderBinary.setRange(0, 255)

        self.ui.sliderBound.valueChanged.connect(lambda x: self.__binary(x, self.ui.sliderBinary.value()))
        self.ui.sliderBound.setRange(0, 80)

        self.ui.cmbThresholdType.addItem("THRESH_OTSU")
        self.ui.cmbThresholdType.addItem("THRESH_BINARY")

    def open_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "",
                                                   "All Files (*);;Text Files (*.txt);;Python Files (*.py)",
                                                   options=options)
        if file_name == '':
            return

        self.img_src = cv2.imread(file_name, cv2.IMREAD_COLOR)

    def find_contours(self, image: ndarray, kernel_size: int):
        kernel = np.ones((1, kernel_size), np.uint8)
        # 执行膨胀操作cv2.erode,
        acts = [cv2.dilate, cv2.erode]
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        iter_img = gray.copy()
        for act in acts:
            iter_img = act(iter_img, kernel, iterations=1)
            # 使用OpenCV进行字符位置检测

        # THRESH_OTSU的效果比较好,而且不需要调参数
        _, binary = cv2.threshold(iter_img, 0, 255, cv2.THRESH_OTSU)
        print(binary.shape)
        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        return binary, contours

    def __binary(self, kernel_size: int, binaryThreshold: int):
        if self.img_src is None:
            return

        binary, contours = self.find_contours(self.img_src.copy(), kernel_size)
        self.ui.lblBinary.setPixmap(ui_helper.cv_to_qpic(binary))

        image_copy = self.img_src.copy()
        # 使用filter函数筛选轮廓
        filtered_contours = self.filter_contours(contours)
        order_c = self.order_contours(filtered_contours, 'y')
        deflection_correction.draw_contours(order_c, image_copy, isRect=True)
        self.ui.lblBound.setPixmap(ui_helper.cv_to_qpic(image_copy))

        x, y, w, h = cv2.boundingRect(order_c[0])
        image_split = self.img_src.copy()[y:y + h, x:x + w]
        self.__y_split(image_split, 2)

    def __y_split(self, image: ndarray, kernel_size: int):
        binary, contours = self.find_contours(image.copy(), kernel_size)
        filtered_contours = deflection_correction.filter_contours(contours, 300)
        order_c = self.order_contours(filtered_contours, 'x')
        self.draw_contours(order_c, image, True)
        cv2.imshow('y_split', image)

    def filter_contours(self, contours: List[np.ndarray]):
        filtered_contours = []
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            if h > 40 and w > 10 and cv2.contourArea(c) > 2000:
                filtered_contours.append(c)
        return filtered_contours

    def order_contours(self, contours: List[np.ndarray], direction: str):
        def contour_sort_key(contour):
            x, y, w, h = cv2.boundingRect(contour)
            return x if direction == 'x' else y

        # 使用自定义排序函数对轮廓列表进行排序
        sorted_contours = sorted(contours, key=contour_sort_key)
        return sorted_contours

    # 按行分割图片
    def split_img(self, image: ndarray, line_pos: int, contours: List[np.ndarray]):
        filter_contours = []
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            if y < line_pos < y + h:
                filter_contours.append(c)
        order_contours = sorted(filter_contours, key=lambda c: cv2.boundingRect(c)[0])
        # order_contours = sorted(order_contours, key=lambda c: cv2.boundingRect(c)[1])
        print('order_contours:', len(order_contours))
        x1, y1, _, _ = cv2.boundingRect(order_contours[0])
        xt, yt, wt, ht = cv2.boundingRect(order_contours[-1])
        x2, y2 = xt + wt, yt + ht
        print(xt, yt)
        return image[y1 - 2:y2 + 2, x1 - 2:x2 + 2]

    def draw_contours(self, contours, image, isRect: bool):
        # 遍历轮廓并绘制实际轮廓
        index = 0
        for contour in contours:
            if isRect:
                x, y, w, h = cv2.boundingRect(contour)
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
                print()
            else:
                cv2.drawContours(image, [contour], -1, (0, 0, 255), 2)

            cv2.putText(image, str(index), (x, y), fontFace=cv2.FONT_HERSHEY_SIMPLEX, fontScale=1,
                        color=(0, 255, 0))  # 绿色文本)
            index += 1

        return image

    def recognize(self):
        self.mouse_cutout.setmode(self.get_str(self.ui.listMode))
        if self.mouse_cutout.img_cut.any():
            wrap = PytesseractWrap(self.mouse_cutout.img_cut)
            wrap.set_whitelist(self.get_str(self.ui.listMode))
            wrap.set_enable_wordlist(self.ui.radWordlist.isChecked())
            ocr_result = wrap.recognize()
            for item in ocr_result.get_map():
                ui_helper.add_item(self.ui.tableWidget, item, OcrResult.get_header())
        # if self.ui.radDefault:

        # ocr_result = self.mouse_cutout.recognize_ocr()
        # for item in ocr_result.get_map():
        #     ui_helper.add_item(self.ui.tableWidget, item, SampleResult.get_header())
        # ocr_result.print_format()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MainWindow()
    icon = QIcon('./icon/ocr.png')
    ui.setWindowIcon(icon)
    ui.show()
    sys.exit(app.exec_())
