from PySide6.QtWidgets import QDialog, QVBoxLayout, QWidget, QHBoxLayout, QLineEdit, QLabel, QPushButton, QCheckBox
from PySide6.QtCore import Signal, Qt
from components.ui.HLine import HLine
import os, json

class SettingsWindow(QDialog):

    chain_dir_signal = Signal()
    refresh_signal = Signal()

    def __init__(self, parent):
        super().__init__(parent)

        layout = QVBoxLayout()

        entrywidget = QWidget()
        entrylayout = QHBoxLayout()
        entrywidget.setLayout(entrylayout)

        with open(os.path.join('res','settings.json'), 'r') as file:
            data = json.load(file)
            self.color1 = QLineEdit(data['color1'])
            self.color2 = QLineEdit(data['color2'])
            self.color3 = QLineEdit(data['color3'])
            self.fontcolor = QLineEdit(data['fontcolor'])
            self.ascending = QCheckBox('Ascending?')
            self.ascending.setChecked(data['ascending'])

        self.setWindowTitle('Settings')

        dirtext = QLabel()
        dirtext.setText('Enter the parent directory.')
        dirtext.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.directorypath = QLineEdit(data['dirpath'])
        self.directorypath.setMinimumWidth(250)

        savebutton = QPushButton('Save Settings')
        savebutton.setFixedSize(100, 25)
        savebutton.clicked.connect(self.save_data)

        entrylayout.addWidget(self.directorypath)

        layout.addWidget(dirtext)
        layout.addWidget(entrywidget, alignment=Qt.AlignmentFlag.AlignHCenter)
        layout.addWidget(HLine(self))
        layout.addWidget(QLabel(text='Level 1 Folder Color:'))
        layout.addWidget(self.color1)
        layout.addWidget(QLabel(text='Level 2 Folder Color:'))
        layout.addWidget(self.color2)
        layout.addWidget(QLabel(text='Level 3 Folder Color:'))
        layout.addWidget(self.color3)
        layout.addWidget(QLabel(text='Font Color:'))
        layout.addWidget(self.fontcolor)
        layout.addWidget(self.ascending)
        layout.addWidget(HLine(self))
        layout.addWidget(savebutton, alignment=Qt.AlignmentFlag.AlignHCenter)

        self.setLayout(layout)

    def save_data(self):
        with open(os.path.join('res','settings.json'), 'r+') as file:
            data = json.load(file)
            new_dirpath = self.directorypath.text()
            data['dirpath'] = new_dirpath
            data['color1'] = self.color1.text()
            data['color2'] = self.color2.text()
            data['color3'] = self.color3.text()
            data['fontcolor'] = self.fontcolor.text()
            data['ascending'] = self.ascending.isChecked()
            file.seek(0)
            json.dump(data, file)
            file.truncate()
        self.chain_dir_signal.emit()
        self.refresh_signal.emit()
        self.close()
