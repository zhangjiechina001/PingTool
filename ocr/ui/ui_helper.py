from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView
from PyQt5.QtCore import Qt
from typing import List, Dict


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
