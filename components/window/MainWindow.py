from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from PySide6.QtCore import Qt
from components.buttons import Directories, TopButtons
from components.ui import SystemTray, ContextMenu
from components.window.SettingsWindow import SettingsWindow
import os, sys

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Compass')
        self.window().setFixedSize(self.sizeHint())
        self.window().setMaximumSize(2000, 2000)

        # big vars
        self.folded = True
        self.move_enabled = True
        self.toobig = False
        
        self.version = 'v1.0.0'

        self.main_layout = QVBoxLayout()

        # main
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)
        
        # enable mouse tracking
        self.setAttribute(Qt.WidgetAttribute.WA_Hover)

        # show/hide button
        self.topbar = TopButtons.TopButtons(self)
        self.topbar.fold_signal.connect(self.fold)
        self.topbar.dropdown_signal.connect(self.regen_dirs)

        # sys tray
        tray = SystemTray.SystemTray(self)
        tray.close_signal.connect(self.closeEvent)

        # set directory widget!
        self.dirs = Directories.Directories(self)
        self.dirpath = self.dirs.get_dirpath()
        self.dirwidget = self.dirs.generate(os.path.join(self.dirpath, self.topbar.dropdown.currentText()), self.toobig)

        # create settings menu but do not show
        self.settings = SettingsWindow(self)
        self.settings.chain_dir_signal.connect(self.regen_dirs)
        self.settings.refresh_signal.connect(self.topbar.refresh_dropdown)

        # right-click menu
        self.menu = ContextMenu.ContextMenu(self, self.version)
        self.menu.close_signal.connect(self.closeEvent)
        self.menu.open_settings_signal.connect(self.open_settings)
        self.menu.movable_signal.connect(self.toggle_movable)
        self.menu.refresh_signal_context_menu.connect(self.topbar.refresh_dropdown)
        self.main_widget.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.main_widget.customContextMenuRequested.connect(self.contextMenuEvent)

        # WIDGET CONTROLS
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        # below is WITHOUT dock icon. WARNING - DO NOT USE UNLESS YOU HAVE ANOTHER WAY TO EXIT THE PROGRAM
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool)
        # WITH dock icon
        #self.setWindowFlags(Qt.WindowType.FramelessWindowHint)

        # add widgets to layout
        self.main_layout.addWidget(self.topbar, alignment=Qt.AlignmentFlag.AlignLeft)
        self.main_layout.addWidget(self.dirwidget)
        
        self.setCentralWidget(self.main_widget)

        # cache size for fold/unfold
        self.cached_size = self.main_widget.sizeHint()
        self.dirs.cached_size.connect(self.cache_size)

        self.show()

    def open_settings(self):
        self.settings.show()

    def cache_size(self, size):
        self.cached_size = size

    def fold(self):
        self.folded = not self.folded
        if self.folded == True:
            self.topbar.button.setText('Hide')
            self.setFixedSize(max(self.cached_size.width(), 500), self.cached_size.height() + 120)
        else:
            self.topbar.button.setText('Show')
            self.setFixedSize(max(self.cached_size.width(), 500), 120)
        self.dirs.fold(self.folded, self.dirwidget)

    def regen_dirs(self):
        # get rid of old dirwidget
        self.main_layout.removeWidget(self.dirwidget)
        self.dirwidget.setParent(None)
        self.dirwidget.destroy()
        # make new dirwidget
        self.dirpath = self.dirs.get_dirpath()
        self.dirwidget = self.dirs.generate(os.path.join(self.dirpath, self.topbar.dropdown.currentText()), self.toobig)
        self.main_layout.addWidget(self.dirwidget)
        try:
            self.dirwidget.setCurrentIndex(0)
        except Exception as e:
            print(e)
        self.window().setFixedSize(self.dirwidget.baseSize())
        self.activateWindow()

    def toggle_movable(self, boolean):
        self.move_enabled = boolean

    def mousePressEvent(self, event):
        if self.move_enabled == True:
            if event.button() == Qt.MouseButton.LeftButton:
                self.adj_point = event.position().toPoint()
                self.old_pos = event.globalPosition().toPoint()
        else:
            event.accept()

    def mouseMoveEvent(self, event):
        if self.move_enabled == True:
            self.setCursor(Qt.CursorShape.DragMoveCursor)
            self.new_pos = event.globalPosition().toPoint()
            delta = self.new_pos - self.old_pos
            new_point = self.old_pos + delta - self.adj_point
            self.move(new_point)
            self.old_pos = new_point
        else:
            pass

    def mouseReleaseEvent(self, event):
        self.setCursor(Qt.CursorShape.ArrowCursor)

    def contextMenuEvent(self, event):
        self.menu.move(self.mapToGlobal(event))
        self.menu.show()
    
    def closeEvent(self):
        sys.exit()
