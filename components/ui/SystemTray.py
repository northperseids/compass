from PySide6.QtWidgets import QSystemTrayIcon, QMenu
from PySide6.QtCore import Signal, Qt
from PySide6.QtGui import QIcon, QAction
from components.window import AboutWindow
import os

class SystemTray(QSystemTrayIcon):

    close_signal = Signal()

    def __init__(self, parent):
        super().__init__(parent)

        self.setIcon(QIcon(os.path.join('res','assets','icon.png')))

        tray_menu = QMenu()

        quit_action = QAction("Quit", tray_menu)
        quit_action.triggered.connect(self.send_closed)

        about_action = QAction("About", tray_menu)
        about_action.triggered.connect(self.show_about)

        show_action = QAction("Show", tray_menu)
        show_action.triggered.connect(self.show_main)

        tray_menu.addAction(show_action)
        tray_menu.addAction(about_action)
        tray_menu.addAction(quit_action)

        self.setContextMenu(tray_menu)

        self.show()

    def send_closed(self):
        self.close_signal.emit()

    def show_about(self):
        AboutWindow(self.parent())

    def show_main(self):
        if self.parent().windowState() == Qt.WindowState.WindowMinimized:
            self.parent().setWindowState(Qt.WindowState.WindowActive)
        else:
            self.parent().activateWindow()
