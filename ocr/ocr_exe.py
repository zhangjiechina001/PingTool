import sys

import cv2
from PyQt5.QtCore import QModelIndex
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QMessageBox, QTableWidget

import ui_helper
from ocr.mouse_cutout import MouseCutOut
from ocr.ui.ocr_ui import Ui_MainWindow
from ocr_bussiness import OcrProcess, SampleResult


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.mouse_cutout = MouseCutOut()
        self.img_src = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.setWindowTitle('字符识别')
        self.recognize_items = []
        self.ui.btnOpenFile.clicked.connect(self.open_file)
        self.ui.btnRecognize.clicked.connect(self.recognize)
        ui_helper.set_table_header(self.ui.tableWidget, SampleResult.get_header())
        self.ui.tableWidget.setSelectionBehavior(QTableWidget.SelectRows)
        self.ui.tableWidget.clicked.connect(self.on_tableWidget_clicked)
        psm_names = ['方向及语言检测', '自动图片分割', '自动图片分割(No OSD)', '完全的自动图片分割',
                     '假设有一列不同大小的文本', '假设有一个垂直对齐的文本块', '假设有一个对齐的文本块',
                     '图片为单行文本', '图片为单词', '图片为圆形的单词', '图片为单个字符', '稀疏文本', 'OSD稀疏文本',
                     '将图像视为单个文本行']
        ui_helper.set_list(psm_names, self.ui.listPsm)

    def open_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "",
                                                   "Picture Files (*.png);;All Files (*)",
                                                   options=options)
        if file_name == '':
            return

        self.img_src = cv2.imread(file_name, cv2.IMREAD_COLOR)
        self.ui.lblSrc.setPixmap(ui_helper.cv_to_qpic(self.img_src.copy()))

    def on_tableWidget_clicked(self,index:QModelIndex):
        item=self.recognize_items[index.row()]
        self.update_pic(item)

    def recognize(self):
        try:
            ocr_process = OcrProcess(self.img_src.copy())
            item = ocr_process.recognize()
            self.update_pic(item)

            self.recognize_items.append(item)
            ui_helper.add_item(self.ui.tableWidget, item.get_map(), item.get_header())
        except Exception as err:
            QMessageBox.warning(self, '错误', err.__traceback__ + str(err))
            print(err, err.__traceback__)

    def update_pic(self, item:SampleResult):
        self.ui.lblSrc.setPixmap(ui_helper.cv_to_qpic(item.img_src))
        self.ui.lblRecognize.setPixmap(ui_helper.cv_to_qpic(item.img_recognized))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui = MainWindow()
    icon = QIcon('./ui/icon/ocr.png')
    ui.setWindowIcon(icon)
    ui.show()
    sys.exit(app.exec_())
