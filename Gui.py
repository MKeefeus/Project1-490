import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import *


def window(data):
    gui_app = QApplication(sys.argv)
    db_table = QTableWidget()
    db_table.setRowCount(1000)
    db_table.setColumnCount(8)
    db_table.setColumnWidth(0 , 500)
    increment_row = 0
    for titles in data:
        name = titles[0]
        db_table.setItem(increment_row, 0, QTableWidgetItem(name))
        increment_row += 1
    title_text = QTextEdit()
    title_text.setReadOnly(True)
    gui_window = QWidget()
    layout = QVBoxLayout()
    layout.addWidget(db_table)
    gui_window.setWindowTitle("PyQt Test")
    gui_window.setGeometry(0, 0, 1600, 900)
    gui_window.setLayout(layout)
    gui_window.show()
    gui_app.exec_()


def display_titles(c):
    job_titles = c.execute("""SELECT title FROM jobs""")
    window(job_titles)





