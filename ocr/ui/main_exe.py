import sys

import cv2
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidgetItem, QListWidget
from main_ui import Ui_MainWindow
from ocr.mouse_cutout import MouseCutOut


class MainWindow(QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.img_src = None
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.set_listWidget()
        self.setWindowTitle('字符识别')
        self.ui.btnOpenFile.clicked.connect(self.open_file)

    def set_listWidget(self):
        for i in range(2):
            item = QListWidgetItem()
            item.setCheckState(Qt.Checked)
            item.setData(Qt.DisplayRole, i)
            self.ui.listOem.addItem(item)

        for i in range(14):
            item = QListWidgetItem()
            item.setCheckState(Qt.Checked)
            item.setData(Qt.DisplayRole, i)
            self.ui.listPsm.addItem(item)

    def open_file(self):
        options = QFileDialog.Options()
        file_name, _ = QFileDialog.getOpenFileName(self, "Open File", "",
                                                   "All Files (*);;Text Files (*.txt);;Python Files (*.py)",
                                                   options=options)
        if file_name == '':
            return

        self.img_src = cv2.imread(file_name, cv2.IMREAD_COLOR)
        mouse_cutout = MouseCutOut(self.img_src.copy())
        mouse_cutout.setmode(self.get_values(self.ui.listOem), self.get_values(self.ui.listPsm),
                             self.get_str(self.ui.listMode))
        mouse_cutout.show()

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
    ui.show()
    sys.exit(app.exec_())
