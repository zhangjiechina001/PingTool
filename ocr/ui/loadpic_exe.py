import sys

import cv2
from PyQt5 import QtGui,QtWidgets
from PyQt5.QtWidgets import QApplication, QFileDialog, QWidget

from loadpic_ui import Ui_Form


class MainWindow(QWidget):
    def __init__(self, parent=None):
        super(QWidget, self).__init__(parent)
        self.mouse_cutout = None
        self.img_src = None
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.setWindowTitle('图片读取')
        self.ui.btnOpenFile.clicked.connect(self.open_file)

        # 设置QLabel的大小策略，允许QLabel自动调整大小
        self.ui.label.setSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        # 设置QLabel的图片缩放模式为适应大小
        self.ui.label.setScaledContents(True)

    def open_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "",
                                                   "All Files (*);;Text Files (*.txt);;Python Files (*.py)",
                                                   options=options)
        if file_name == '':
            return

        self.img_src = cv2.imread(file_name, cv2.IMREAD_COLOR)
        self.setImage(self.img_src)

    def setImage(self, cv2_img):
        img = cv2_img  # opencv读取图片
        img2 = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # opencv读取的bgr格式图片转换成rgb格式
        _image = QtGui.QImage(img2[:], img2.shape[1], img2.shape[0], img2.shape[1] * 3,
                              QtGui.QImage.Format_RGB888)  # pyqt5转换成自己能放的图片格式
        jpg_out = QtGui.QPixmap(_image).scaled(self.ui.label.width(), self.ui.label.height())  # 设置图片大小
        self.ui.label.setPixmap(jpg_out)  # 设置图片显示


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())
