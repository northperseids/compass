from PySide6.QtWidgets import QMenu
from PySide6.QtCore import Signal
from PySide6.QtGui import QAction
from components.window.AboutWindow import AboutWindow

class ContextMenu(QMenu):

    open_settings_signal = Signal()
    movable_signal = Signal(bool)
    close_signal = Signal()
    refresh_signal_context_menu = Signal()
    
    def __init__(self, parent, version):
        super().__init__(parent)

        self.toggle = True
        self.version = version

        quit_action = QAction("Quit", self)
        quit_action.triggered.connect(self.send_closed)

        about_action = QAction("About", self)
        about_action.triggered.connect(self.show_about)

        settings_action = QAction("Settings", self)
        settings_action.triggered.connect(self.open_settings)

        self.lock_action = QAction(" ", self)
        if self.toggle == True:
            self.lock_action.setText("Lock position")
        else:
            self.lock_action.setText("Unlock position")
        self.lock_action.triggered.connect(self.toggle_movable)

        refresh_action = QAction("Refresh", self)
        refresh_action.triggered.connect(self.refresh_signal)

        self.addAction(about_action)
        self.addAction(self.lock_action)
        self.addAction(settings_action)
        self.addAction(refresh_action)
        self.addAction(quit_action)

    def open_settings(self):
        self.open_settings_signal.emit()

    def refresh_signal(self):
        self.refresh_signal_context_menu.emit()

    def toggle_movable(self):
        self.toggle = not self.toggle
        if self.toggle == True:
            self.lock_action.setText("Lock position")
        else:
            self.lock_action.setText("Unlock position")
        self.movable_signal.emit(self.toggle)
    
    def send_closed(self):
        self.close_signal.emit()

    def show_about(self):
        AboutWindow(self.parent(), self.version)
