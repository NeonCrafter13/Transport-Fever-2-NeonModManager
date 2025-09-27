from types import FunctionType
from PyQt6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QLineEdit
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QKeyEvent


class SearchBox(QWidget):
    def __init__(self, callback: FunctionType):
        super().__init__()
        self.callback = callback
        self.initMe()

    def initMe(self):
        self.h = QHBoxLayout()
        self.textbox = QLineEdit()

        self.h.addWidget(self.textbox)

        self.button = QPushButton('Search')
        self.h.addWidget(self.button)
        self.button.clicked.connect(self.search)

        self.setLayout(self.h)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key.Key_Return:
            self.search()
            return
        return super().keyPressEvent(event)

    def search(self):
        keyword = self.textbox.text()

        self.callback(keyword)
