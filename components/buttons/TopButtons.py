from PySide6.QtWidgets import QWidget, QHBoxLayout, QPushButton, QComboBox, QGraphicsOpacityEffect
from PySide6.QtCore import Qt, Signal
import os, json, webbrowser

class TopButtons(QWidget):

    fold_signal = Signal()
    dropdown_signal = Signal(str)

    def __init__(self, parent):
        super().__init__(parent)

        layout = QHBoxLayout()

        self.parent_dir = ''

        self.button = QPushButton("Hide")
        self.button.setGraphicsEffect(QGraphicsOpacityEffect(opacity=1.0))
        self.button.setStyleSheet('background-color: #2b2d31; color: white;')
        self.button.setFixedSize(100, 25)
        self.button.clicked.connect(self.trigger_fold)

        self.open = QPushButton("Open")
        self.open.setGraphicsEffect(QGraphicsOpacityEffect(opacity=1.0))
        self.open.setStyleSheet('background-color: #2b2d31; color: white;')
        self.open.setFixedSize(100, 25)
        self.open.clicked.connect(self.open_dir)

        self.dropdown = QComboBox()
        self.dropdown.setFixedHeight(25)
        self.dropdown.setMaximumWidth(500)
        self.dropdown.setMinimumWidth(200)
        self.dropdown.setStyleSheet('background-color: #2b2d31; color: white;')
        self.refresh_dropdown()
        self.dropdown.currentIndexChanged.connect(self.dropdown_selected)

        # set translucent background
        self.setAttribute(Qt.WidgetAttribute.WA_StyledBackground)
        self.setStyleSheet('background-color: rgba(0,0,0,0.5); border-radius: 10px;')

        self.setMinimumWidth(450)

        layout.addWidget(self.dropdown)
        layout.addWidget(self.open)
        layout.addWidget(self.button)

        self.setLayout(layout)

    def dropdown_selected(self):
        self.dropdown_signal.emit(self.dropdown.currentText())

    def open_dir(self):
        opsys = os.name
        if opsys == 'posix':
            webbrowser.open(os.path.join(self.parent_dir, self.dropdown.currentText()))
        elif opsys == 'nt':
            os.startfile(os.path.join(self.parent_dir, self.dropdown.currentText()))

    # this function triggers the fold toggle - the actual fold true/false variable is in the MAINWINDOW
    def trigger_fold(self):
        self.fold_signal.emit()

    def refresh_dropdown(self):
        self.dropdown.clear()
        with open(os.path.join('res','settings.json'), 'r') as file:
            data = json.load(file)
            self.parent_dir = data['dirpath']
            ascending = data['ascending']
        try:
            hidden_prefixes = ['.', '$']
            lv1 = sorted(os.listdir(self.parent_dir))
            lv1 = [d for d in lv1 if os.path.isdir(os.path.join(self.parent_dir, d)) and d[0] not in hidden_prefixes]
            if ascending == False:
                for i in range(len(lv1), 0, -1):
                    self.dropdown.addItem(lv1[i-1])
            else:
                for folder in lv1:
                    self.dropdown.addItem(folder)
        except FileNotFoundError:
            self.dropdown.addItem('No file/directory selected.')
