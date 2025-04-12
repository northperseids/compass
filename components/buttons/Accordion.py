from PySide6.QtWidgets import QStackedWidget, QPushButton, QWidget, QVBoxLayout, QHBoxLayout
from PySide6.QtCore import Qt
import DirButton
import os

class Accordion(QStackedWidget):
    def __init__(self, parentdirpath, folderlist, color, fontcolor):
        super().__init__()

        self.toggle_button_closed = QPushButton(self, text=f'>')
        self.toggle_button_closed.setFixedSize(50,25)
        self.toggle_button_closed.setStyleSheet(f'color: {fontcolor}; background-color: {color}')
        self.toggle_button_closed.clicked.connect(self.open_accordion)
        self.toggle_button_open = QPushButton(self, text=f'v')
        self.toggle_button_open.setFixedSize(50,25)
        self.toggle_button_open.setStyleSheet(f'color: {fontcolor}; background-color: {color}')
        self.toggle_button_open.clicked.connect(self.close_accordion)

        self.setStyleSheet('padding-left: 20px;')

        self.widget1 = QWidget()
        self.layout1 = QVBoxLayout()
        self.widget1.setLayout(self.layout1)
        self.widget1.setContentsMargins(0,0,0,0)
        self.layout1.setContentsMargins(0,0,0,0)
        self.layout1.setAlignment(Qt.AlignmentFlag.AlignLeft)

        self.widget2 = QWidget()
        self.layout2 = QVBoxLayout()
        self.widget2.setLayout(self.layout2)
        self.widget2.setContentsMargins(0,0,0,0)
        self.layout2.setContentsMargins(0,0,0,0)
        self.layout2.setAlignment(Qt.AlignmentFlag.AlignLeft)

        hwidget1 = QWidget()
        hlayout1 = QHBoxLayout()
        hwidget1.setLayout(hlayout1)
        hlayout1.addWidget(self.toggle_button_closed, alignment=Qt.AlignmentFlag.AlignLeft)
        hlayout1.setContentsMargins(0,0,0,0)
        hwidget1.setContentsMargins(0,0,0,0)

        hwidget2 = QWidget()
        hlayout2 = QHBoxLayout()
        hwidget2.setLayout(hlayout2)
        hlayout2.addWidget(self.toggle_button_open, alignment=Qt.AlignmentFlag.AlignLeft)
        hlayout2.setContentsMargins(0,0,0,0)
        hwidget2.setContentsMargins(0,0,0,0)

        self.layout1.addWidget(hwidget1)
        self.layout2.addWidget(hwidget2)

        for subfolder in folderlist:
            subpath = os.path.join(parentdirpath, subfolder)
            button = DirButton(subpath, subfolder, color, fontcolor)
            button.setFixedWidth(130)
            self.layout2.addWidget(button)

        self.addWidget(self.widget1)
        self.addWidget(self.widget2)

        self.widget1.setFixedHeight(30)
        self.setFixedHeight(30)

    def open_accordion(self):
        self.setCurrentIndex(1)
        self.setFixedHeight(self.widget2.sizeHint().height())

    def close_accordion(self):
        self.setCurrentIndex(0)
        self.widget1.setFixedHeight(30)
        self.setFixedHeight(30)
