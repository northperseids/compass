from PySide6.QtWidgets import QPushButton, QGraphicsOpacityEffect
import os, webbrowser

class DirButton(QPushButton):
    def __init__(self, path, title, color, fontcolor):
        super().__init__()
        if len(title) > 16 and type(title) == str:
            arr = [title[i:i+13] for i in range(0,len(title), 13)]
            text = '\n'.join(arr)
            lines = len(arr)
        else:
            text = title
            lines = 1
        self.setText(text)
        self.path = path
        self.setStyleSheet(f'font-size: 17px; color: {fontcolor}; background-color: {color}; text-align: left; padding-left: 10px;')
        self.setFixedHeight(25 * lines)
        self.setGraphicsEffect(QGraphicsOpacityEffect(opacity=1.0))
        self.clicked.connect(self.open_dir)

    def open_dir(self):
        opsys = os.name
        if opsys == 'posix':
            webbrowser.open(self.path)
        elif opsys == 'nt':
            os.startfile(self.path)
