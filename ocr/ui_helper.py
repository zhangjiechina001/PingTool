import cv2
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt
from typing import List, Dict
from numpy import ndarray


def add_item(tableWidget: QTableWidget, val_map: Dict, header: List[str]):
    if tableWidget.columnCount() != len(header):
        set_table_header(tableWidget, header)

    newRowIndex = tableWidget.rowCount()
    tableWidget.insertRow(newRowIndex)

    for i, key in enumerate(header):
        newItem1 = QTableWidgetItem()
        if key in val_map:
            newItem1.setData(Qt.DisplayRole, str(val_map[key]))
        else:
            newItem1.setData(Qt.DisplayRole, "--")
        newItem1.setTextAlignment(Qt.AlignCenter)
        tableWidget.setItem(newRowIndex, i, newItem1)

    tableWidget.resizeRowsToContents()
    tableWidget.show()


def set_table_header(tableWidget, header):
    tableWidget.clear()
    tableWidget.setColumnCount(len(header))
    tableWidget.setRowCount(0)
    tableWidget.setHorizontalHeaderLabels(header)
    tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
    tableWidget.setAlternatingRowColors(True)


def cv_to_qt(image: ndarray):
    # 增加灰度图判断
    if len(image.shape) == 2:
        image = cv2.cvtColor(image.copy(), cv2.COLOR_GRAY2RGB)
    # 将 OpenCV 图像转换为 QImage
    height, width, channel = image.shape
    bytes_per_line = 3 * width
    q_image = QImage(image.data, width, height, bytes_per_line, QImage.Format_RGB888)
    return q_image

def cv_to_qpic(image: ndarray):
    q_image=cv_to_qt(image)
    return QPixmap.fromImage(cv_to_qt(q_image))