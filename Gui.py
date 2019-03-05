import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout


def window(data):
    app = QApplication(sys.argv)
    test = QtWidgets.QTextEdit()
    for thing in data:
        QtWidgets.QTextEdit.insertHtml(test, "%s<br />" %str(thing))
    test.setReadOnly(True)
    w = QWidget()
    layout = QVBoxLayout()
    layout.addWidget(test)
    button = QPushButton("YES")
    layout.addWidget(button)
    w.setWindowTitle("PyQt Test")
    w.setLayout(layout)
    w.show()
    sys.exit(app.exec_())


def display_titles(c):
    c.execute("""SELECT title FROM jobs""")
    titles = c.fetchall()
    window(titles)





