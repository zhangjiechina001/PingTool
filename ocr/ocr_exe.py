import sys

import cv2
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidgetItem, QListWidget
from PyQt5.QtGui import QIcon
from ocr.mouse_cutout import MouseCutOut
from ocr.data.ocr_result import OcrResult
from ocr.ui.ocr_ui import Ui_MainWindow
from ocr.pytesseract_wrap import PytesseractWrap
import ui_helper


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.mouse_cutout = MouseCutOut()
        self.img_src = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle('字符识别')
        self.ui.btnOpenFile.clicked.connect(self.open_file)
        # self.ui.btnRecognize.clicked.connect(self.recognize)

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
        self.mouse_cutout = MouseCutOut(self.img_src.copy())
        self.mouse_cutout.show()

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
        #     ui_helper.add_item(self.ui.tableWidget, item, OcrResult.get_header())
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
    icon = QIcon('../ui/icon/ocr.png')
    ui.setWindowIcon(icon)
    ui.show()
    sys.exit(app.exec_())