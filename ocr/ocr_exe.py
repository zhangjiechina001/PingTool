import sys

import cv2
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidgetItem, QListWidget
from PyQt5.QtGui import QIcon, QPixmap,QImage
from ocr.mouse_cutout import MouseCutOut
from ocr.data.ocr_result import OcrResult
from ocr.ui.ocr_ui import Ui_MainWindow
from ocr.pytesseract_wrap import PytesseractWrap
import ui_helper
import ocr_bussiness as obs


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.mouse_cutout = MouseCutOut()
        self.img_src = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle('字符识别')
        self.ui.btnOpenFile.clicked.connect(self.open_file)
        self.ui.btnRecognize.clicked.connect(self.recognize)
        ui_helper.set_table_header(self.ui.tableWidget, obs.SampleResult.get_header())

    def open_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "",
                                                   "Picture Files (*.png);;All Files (*)",
                                                   options=options)
        if file_name == '':
            return

        self.img_src = cv2.imread(file_name, cv2.IMREAD_COLOR)
        self.ui.lblSrc.setPixmap(ui_helper.cv_to_qpic(self.img_src.copy()))

    def recognize(self):
        img_char = obs.location(self.img_src)
        _, ocr_ret = obs.recognize(img_char)
        self.ui.lblSrc.setPixmap(ui_helper.cv_to_qpic(ocr_ret.img_src))
        self.ui.lblRecognize.setPixmap(ui_helper.cv_to_qpic(ocr_ret.img_recognized))
        for item in ocr_ret.get_map():
            ui_helper.add_item(self.ui.tableWidget, item, obs.SampleResult.get_header())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MainWindow()
    icon = QIcon('./ui/icon/ocr.png')
    ui.setWindowIcon(icon)
    ui.show()
    sys.exit(app.exec_())
