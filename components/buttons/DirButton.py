from PySide6.QtWidgets import QPushButton, QGraphicsOpacityEffect
import os, webbrowser, textwrap

class DirButton(QPushButton):
    def __init__(self, path, title, color, fontcolor, lvl):
        super().__init__()
        if len(title) > 14 and type(title) == str:
            #arr = [title[i:i+9] for i in range(0,len(title), 9)]
            if lvl == 1:
                wwidth = 12
            elif lvl == 2:
                wwidth = 10
            elif lvl == 3:
                wwidth = 8
            arr = textwrap.wrap(title, wwidth)
            text = '\n'.join(arr)
            lines = len(arr)
        else:
            text = title
            lines = 1
        self.setText(text)
        self.path = path
        self.setStyleSheet(f'font-size: 25px; color: {fontcolor}; background-color: {color}; text-align: left; padding-left: 10px; border-radius: 5px;')
        self.setFixedHeight(30 * lines)
        self.setGraphicsEffect(QGraphicsOpacityEffect(opacity=1.0))
        self.clicked.connect(self.open_dir)

    def open_dir(self):
        opsys = os.name
        if opsys == 'posix':
            webbrowser.open(self.path)
        elif opsys == 'nt':
            os.startfile(self.path)
