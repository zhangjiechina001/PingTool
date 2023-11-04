import sys
from typing import List

import cv2
import numpy as np
from numpy import ndarray
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidgetItem, QListWidget
from PyQt5.QtGui import QIcon, QPixmap, QImage
from bound_ui import Ui_MainWindow
from ocr.mouse_cutout import MouseCutOut
from ocr.data.ocr_result import OcrResult
from ocr.pytesseract_wrap import PytesseractWrap

import ocr.ui_helper as ui_helper


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
        self.ui.sliderBound.setRange(0, 40)

    def set_listWidget(self, names, listWidget: QListWidget):
        for index in range(len(names)):
            item = QListWidgetItem()
            # item.setCheckState(Qt.Checked)
            item.setData(Qt.DisplayRole, '{0}.{1}'.format(index, names[index]))
            listWidget.addItem(item)

    def open_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "",
                                                   "All Files (*);;Text Files (*.txt);;Python Files (*.py)",
                                                   options=options)
        if file_name == '':
            return

        self.img_src = cv2.imread(file_name, cv2.IMREAD_COLOR)

    def __binary(self, kernel_size: int, binaryThreshold: int):
        if self.img_src is None:
            return

        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        # 执行膨胀操作cv2.erode,
        acts = [cv2.dilate, cv2.erode]
        iter_img = self.img_src.copy()
        for act in acts:
            iter_img = act(iter_img, kernel, iterations=1)

        # 使用OpenCV进行字符位置检测
        gray = cv2.cvtColor(iter_img, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, binaryThreshold, 255, cv2.THRESH_OTSU)
        # cv2.imshow('binary',binary)
        # cv2.waitKey()
        print(binary.shape)
        pixmap = QPixmap.fromImage(ui_helper.cv_to_qt(binary))
        self.ui.lblBinary.setPixmap(pixmap)

        contours, _ = cv2.findContours(binary, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        image_copy = self.img_src.copy()
        # 使用filter函数筛选轮廓
        filtered_contours = []
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            if h > 40 and w > 10 and cv2.contourArea(c) > 300:
                print(h, w)
                filtered_contours.append(c)

        self.draw_contours(filtered_contours, image_copy, True)
        self.ui.lblBound.setPixmap(QPixmap.fromImage(ui_helper.cv_to_qt(image_copy)))
        print(self.recognize_type(filtered_contours))

    def recognize_type(self, contours: List[np.ndarray]):
        max_contour = max(contours, key=lambda c:cv2.contourArea(c))
        print(cv2.contourArea(max_contour))
        return "粗体" if cv2.contourArea(max_contour)<70000 else "细体"

    def draw_contours(self, contours, image, isRect: bool):
        # 遍历轮廓并绘制实际轮廓
        for contour in contours:
            if isRect:
                x, y, w, h = cv2.boundingRect(contour)
                if w * h < 100:
                    continue
                cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            else:
                cv2.drawContours(image, [contour], -1, (0, 0, 255), 2)
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

    def get_values(self, listWidget: QListWidget):
        ret = []
        # temp=listWidget.items()
        for index in range(listWidget.count()):
            ret.append(listWidget.item(index).data(Qt.DisplayRole))
        return ret

    def get_str(self, listWidget: QListWidget):
        ret = []
        # temp=listWidget.items()
        for index in range(listWidget.count()):
            if listWidget.item(index).checkState() == Qt.Checked:
                ret.append(listWidget.item(index).text())
        return ''.join(ret)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MainWindow()
    icon = QIcon('./icon/ocr.png')
    ui.setWindowIcon(icon)
    ui.show()
    sys.exit(app.exec_())
