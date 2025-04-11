# compass using Qt instead of wxPython
# project started 11/22/24
#
# To use PyInstaller on LINUX: deactivate venv, then python3 -m PyInstaller main.py
#
# if you get stuck with the thing running and can't close it:
# use terminal, `ps -ef | grep python`
# kill the main.py that shows up
#
#
# version:
compassVersion = 'v1.0.0'
#
#
# ⠀⠀⠀⠀⠀⠀ ⠀⠀ ⣀⠀⠀⠀  ⠀⠀⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢹⣄⠀⠀⠀⠀⣠⡟⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⣤⡀⠀⢀⣤⣶⣿⣿⣿⣿⣿⣿⣿⣿⣶⣤⡀⣀⣤⣶⡟⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠈⣻⣾⣿⣿⣿⡿⠟⠛⠛⠛⠛⠻⢿⣿⣿⣿⡿⣻⡟⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⣴⣿⣿⣿⠟⠁⠀⠀⠀⠀⢀⣠⣴⣿⣿⡿⠋⣼⣿⣦⠀⠀⠀⠀⠀
#⠀⢠⣄⣀⣼⣿⣿⡿⠁⠀⠀⠀⣀⣤⣾⣿⣿⣿⡿⠋⢀⣼⢿⣿⣿⣧⣀⣠⡄⠀
#⠀⠀⠀⠙⣿⣿⣿⠁⠀⠀⠀⣼⠛⢿⣿⣿⡿⠋⠀⢀⡾⠃⠈⣿⣿⣿⠋⠀⠀⠀
#⠀⠀⠀⠀⣿⣿⣿⠀⠀⢀⣾⠃⠀⠀⢙⡋⠀⠀⢠⡿⠁⠀⠀⣿⣿⣿⠀⠀⠀⠀
#⠀⠀⠀⣠⣿⣿⣿⡀⢀⡾⠁⠀⢀⣴⣿⣿⣦⣠⡟⠁⠀⠀⢀⣿⣿⣿⣄⠀⠀⠀
#⠀⠘⠋⠉⢻⣿⣿⣷⡿⠁⢀⣴⣿⣿⣿⡿⠟⠋⠀⠀⠀⢀⣾⣿⣿⡟⠉⠙⠃⠀
#⠀⠀⠀⠀⠀⢻⣿⡟⢀⣴⣿⣿⠿⠋⠁⠀⠀⠀⠀⢀⣴⣿⣿⣿⡟⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⣼⢟⣴⣿⣿⣿⣷⣦⣤⣤⣤⣤⣴⣶⣿⣿⣿⡿⣯⡀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⣼⠿⠛⠉⠉⠛⠿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⠉⠀⠈⠛⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⣸⠋⠀⠉⠉⠀⠙⣧⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
#⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀⠀⠀⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀


import sys
import webbrowser, os
import json
from PySide6.QtCore import Qt, Signal, Signal, QSize
from PySide6.QtGui import QAction, QIcon
from PySide6.QtWidgets import QApplication, QLineEdit, QWidget, QMenu, QPushButton, QMainWindow, QVBoxLayout, QGraphicsOpacityEffect, QComboBox, QFrame, QHBoxLayout, QStackedWidget, QLabel, QDialog, QSystemTrayIcon

opsys = os.name
if opsys == 'posix':
    delim = '/'
else:
    delim = '\\'

# big vars
columns = 9
rows = 7
maxrows = 15
maxsize = 100

fontsize = '17px'
fontcolor = 'white'

hidden_prefixes = ['.', '$']
toobig = False

parent_dir = ''

# GET DIRECTORY FUNCTIONS

def nested_len(arr):
    if type(arr) == list:
        return sum(nested_len(entry) for entry in arr)
    else:
        return 1

def get_directories(source):

    toobig = False

    # parent array
    folderslist = []

    try:
        lv1 = sorted(os.listdir(source))
        lv1 = [d for d in lv1 if os.path.isdir(os.path.join(source, d)) and d[0] not in hidden_prefixes]

        if len(lv1) > columns:
            lv1 = lv1[0:columns]
            lv1.append('...')

        for i, entry in enumerate(lv1):

            if entry == '...':
                subarray.append(entry)
                continue

            # make wrapper array for individual lv1 folders
            subarray = []

            # add header folders
            subarray.append(entry)

            # get level 2 dirs
            folder2 = sorted(os.listdir(os.path.join(source, entry)))
            folder2 = [d for d in folder2 if os.path.isdir(os.path.join(source, entry, d)) and d[0] not in hidden_prefixes]
            
            if len(folder2) > rows:
                folder2 = folder2[0:rows]
                folder2.append('...')

            # make another wrapper array for lv2 folders
            subfolders = []

            for i, subentry in enumerate(folder2):

                if subentry == '...':
                    subfolders.append(subentry)
                    continue

                # add lv2 header folders
                subfolders.append(subentry)

                # get level 3 dirs
                folder3 = sorted(os.listdir(os.path.join(source, entry, subentry)))
                folder3 = [d for d in folder3 if os.path.isdir(os.path.join(source, entry, subentry, d)) and d[0] not in hidden_prefixes]

                if len(folder3) > rows:
                    folder3 = folder3[0:rows]
                    folder3.append('...')

                # append to wrapper array
                subfolders.append(folder3)

                if nested_len(subfolders) > maxrows:
                    subfolders = subfolders[0:maxrows]
                    subfolders.append('p...')
                    toobig = True
                    break
            
            # append to wrapper array
            subarray.append(subfolders)
            
            if nested_len(subarray) > maxsize:
                toobig = True
                break

            # append to parent array
            folderslist.append(subarray)
    except FileNotFoundError:
        folderslist = 'filenotfound'

    except PermissionError:
        folderslist = 'permerror'

    return [toobig, folderslist]


# MAIN
class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('Compass')
        self.window().setFixedSize(self.sizeHint())
        self.window().setMaximumSize(2000, 2000)

        # big vars
        self.folded = True
        self.move_enabled = True

        self.main_layout = QVBoxLayout()

        # main
        self.main_widget = QWidget()
        self.main_widget.setLayout(self.main_layout)
        
        # enable mouse tracking
        self.setAttribute(Qt.WidgetAttribute.WA_Hover)

        # show/hide button
        self.topbar = TopButtons(self)
        self.topbar.fold_signal.connect(self.fold)
        self.topbar.dropdown_signal.connect(self.regen_dirs)

        # sys tray
        tray = SystemTray(self)
        tray.close_signal.connect(self.closeEvent)

        # set directory widget!
        self.dirs = Directories(self)
        self.dirpath = self.dirs.get_dirpath()
        self.dirwidget = self.dirs.generate(os.path.join(self.dirpath, self.topbar.dropdown.currentText()))

        # create settings menu but do not show
        self.settings = SettingsWindow(self)
        self.settings.chain_dir_signal.connect(self.regen_dirs)
        self.settings.refresh_signal.connect(self.topbar.refresh_dropdown)

        # right-click menu
        self.menu = ContextMenu(self)
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
        self.dirwidget = self.dirs.generate(os.path.join(self.dirpath, self.topbar.dropdown.currentText()))
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
        self.setStyleSheet(f'font-size: {fontsize}; color: {fontcolor}; background-color: {color}; text-align: left; padding-left: 10px;')
        self.setFixedHeight(25 * lines)
        self.setGraphicsEffect(QGraphicsOpacityEffect(opacity=1.0))
        self.clicked.connect(self.open_dir)

    def open_dir(self):
        if opsys == 'posix':
            webbrowser.open(self.path)
        elif opsys == 'nt':
            os.startfile(self.path)

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

class Directories(QWidget):

    cached_size = Signal(QSize)

    def __init__(self, parent):
        super().__init__(parent)

        self.get_colors()

    def get_colors(self):
        with open(os.path.join('res','settings.json'), 'r') as file:
            data = json.load(file)
            self.color1 = data['color1']
            self.color2 = data['color2']
            self.color3 = data['color3']
            self.fontcolor = data['fontcolor']

    def get_dirpath(self):
        with open(os.path.join('res','settings.json'), 'r') as file:
            data = json.load(file)
            return data['dirpath']
        
    def generate(self, dirpath):

        self.get_colors()

        if dirpath == '':
            defaultwidget = QWidget()
            defaultlayout = QVBoxLayout()
            defaulttext = QLabel()
            defaulttext.setText('No directory specified.\n\nRight-click, choose Settings, and enter a directory.')
            defaultlayout.addWidget(defaulttext)
            defaultwidget.setLayout(defaultlayout)
            return defaultwidget
        
        # if it ends in a / or \, fine; if not, add delim
        if dirpath[-1] != delim:
            dirpath += delim

        dirs = get_directories(dirpath)

        self.toobig = dirs[0]
        self.array = dirs[1]

        if toobig == True:
            defaultwidget = QWidget()
            defaultlayout = QVBoxLayout()
            defaulttext = QLabel()
            defaulttext.setText('Directory entered is too big.')
            defaultlayout.addWidget(defaulttext)
            defaultwidget.setLayout(defaultlayout)
            return defaultwidget
        elif self.array == 'filenotfound':
            defaultwidget = QWidget()
            defaultlayout = QVBoxLayout()
            defaulttext = QLabel()
            defaulttext.setText('Directory not found. Please enter a new directory in Settings.')
            defaultlayout.addWidget(defaulttext)
            defaultwidget.setLayout(defaultlayout)
            return defaultwidget
        elif self.array == 'permerror':
            defaultwidget = QWidget()
            defaultlayout = QVBoxLayout()
            defaulttext = QLabel()
            defaulttext.setText('Permissions error. Please enter a new directory in Settings.')
            defaultlayout.addWidget(defaulttext)
            defaultwidget.setLayout(defaultlayout)
            return defaultwidget
        else:

            # make horizontal box for cols
            cols = QWidget()
            colslayout = QHBoxLayout()
            cols.setLayout(colslayout)
            for col in self.array:
                # make vertical box for folder buttons
                column = QWidget()
                collayout = QVBoxLayout()
                column.setLayout(collayout)

                collayout.setContentsMargins(0, 0, 0, 0)

                if col == []:
                    pass
                elif type(col) == list:

                    for folder in col:

                        parentdirpath = dirpath + col[0]

                        # make vertical box for subfolder buttons
                        folders = QWidget()
                        folderslayout = QVBoxLayout()
                        folders.setLayout(folderslayout)
                        folderslayout.setContentsMargins(0, 0, 0, 0)

                        if folder == []:
                            pass

                        elif type(folder) == str:
                            # this is TIER ONE
                            if folder == '...':
                                button = DirButton(dirpath, '(List truncated)', self.color1, self.fontcolor)
                                column = QWidget()
                                collayout = QVBoxLayout()
                                column.setLayout(collayout)
                                button.setFixedWidth(150)
                                collayout.addWidget(button)
                                #collayout.addStretch()
                                colslayout.addWidget(column)
                                colslayout.setAlignment(Qt.AlignmentFlag.AlignRight)
                                continue
                            else:
                                button = DirButton(parentdirpath, folder, self.color1, self.fontcolor)
                                button.setFixedWidth(150)
                                folderslayout.addWidget(button)

                        elif type(folder) == list:
                            
                            # subfolders
                            for i, subfolder in enumerate(folder):

                                # this will set the dirpath to the parent folder and "cache" the parent folder while iterating through the subsubfolders.
                                if type(subfolder) != list:
                                    subdirpath = os.path.join(parentdirpath, subfolder)

                                # make subfolder container widget for subsubfolder buttons
                                subfolders = QWidget()
                                subfolderslayout = QVBoxLayout()
                                subfolders.setLayout(subfolderslayout)
                                subfolderslayout.setContentsMargins(0, 0, 0, 0)
                                subfolderslayout.setAlignment(Qt.AlignmentFlag.AlignRight)

                                if subfolder == []:
                                    pass
                                elif type(subfolder) == str:
                                    # this is TIER TWO
                                    if subfolder == '...':
                                        button = DirButton(parentdirpath, subfolder, self.color1, self.fontcolor)
                                    elif subfolder == 'p...':
                                        button = DirButton(parentdirpath, '(List truncated)', self.color1, self.fontcolor)
                                    else:
                                        button = DirButton(subdirpath, subfolder, self.color2, self.fontcolor)
                                    button.setFixedWidth(140)
                                    subfolderslayout.addWidget(button)

                                else:

                                    # this is TIER THREE

                                    # subsubfolders
                                    for subsubfolder in subfolder:
                                        subsubdirpath = os.path.join(subdirpath, subsubfolder)
                                        button = DirButton(subsubdirpath, subsubfolder, self.color3, self.fontcolor)
                                        button.setFixedWidth(130)
                                        subfolderslayout.addWidget(button)

                                    # BELOW IS FOR WHENEVER YOU GET THE ACCORDION STUFF WORKING
                                    # if len(subfolder) > 6:
                                    #     # accordion
                                    #     accordion = Accordion(subdirpath, subfolder, self.color3, self.fontcolor)
                                    #     subfolderslayout.addWidget(accordion)
                                    # else:
                                    #     # subsubfolders
                                    #     for subsubfolder in subfolder:
                                    #         subsubdirpath = os.path.join(subdirpath, subsubfolder)
                                    #         button = DirButton(subsubdirpath, subsubfolder, self.color3, self.fontcolor)
                                    #         button.setFixedWidth(130)
                                    #         subfolderslayout.addWidget(button)

                                folderslayout.addWidget(subfolders)

                        collayout.addWidget(folders)

                collayout.addStretch()
                colslayout.addWidget(column)
        
        blank_widget = self.blankwidget()

        stacked_widget = QStackedWidget()
        stacked_widget.addWidget(cols)
        self.cached_size.emit(cols.sizeHint())
        stacked_widget.addWidget(blank_widget)

        return stacked_widget
    
    def fold(self, boolean, stacked_widget):
        if type(stacked_widget) != QStackedWidget:
            return
        # note: do not adjust the window size here or it will potentially fuck up button spacing in the full dirs widget(s)
        if boolean == False:
            stacked_widget.setCurrentIndex(1)
        else:
            stacked_widget.setCurrentIndex(0)

    def blankwidget(self):
        layout = QVBoxLayout()
        widget = QWidget()
        widget.setLayout(layout)
        return widget

class AboutWindow(QDialog):
    def __init__(self, parent):
        super().__init__(parent)

        layout = QVBoxLayout()

        self.setWindowTitle('About')

        title = QLabel()
        title.setText('Compass Shortcuts')
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        version = QLabel()
        version.setText(compassVersion)
        version.setAlignment(Qt.AlignmentFlag.AlignCenter)

        usage = QLabel()
        usage.setFixedWidth(300)
        usage.setWordWrap(True)
        usage.setContentsMargins(10, 10, 10, 10)
        usage.setText('To change the PARENT DIRECTORY:\n\n1. Right-click and choose Settings.\n2. Paste the FULL DIRECTORY PATH into the text box and click Submit.\n\n\nTo change colors:\n\n1. Right-click and open Settings.\n2. Paste either an HTML-compatible color name (white, black, etc.) or a hex code (#FFFFFF for white, for example) into the desired color fields.\n3. Click "Save Settings.')

        layout.addWidget(title)
        layout.addWidget(version)
        layout.addWidget(usage)

        self.setLayout(layout)

        self.show()

class HLine(QFrame):
    def __init__(self, parent):
        super().__init__(parent)
        self.setFrameShape(QFrame.Shape.HLine)
        self.setFrameShadow(QFrame.Shadow.Sunken)

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
            file.seek(0)
            json.dump(data, file)
            file.truncate()
        self.chain_dir_signal.emit()
        self.refresh_signal.emit()
        self.close()

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

class TopButtons(QWidget):

    fold_signal = Signal()
    dropdown_signal = Signal(str)

    def __init__(self, parent):
        super().__init__(parent)

        layout = QHBoxLayout()

        self.parent_dir = ''

        self.button = QPushButton("Hide")
        self.button.setGraphicsEffect(QGraphicsOpacityEffect(opacity=1.0))
        self.button.setStyleSheet('background-color: #2b2d31;')
        self.button.setFixedSize(100, 25)
        self.button.clicked.connect(self.trigger_fold)

        self.open = QPushButton("Open")
        self.open.setGraphicsEffect(QGraphicsOpacityEffect(opacity=1.0))
        self.open.setStyleSheet('background-color: #2b2d31;')
        self.open.setFixedSize(100, 25)
        self.open.clicked.connect(self.open_dir)

        self.dropdown = QComboBox()
        self.dropdown.setFixedHeight(25)
        self.dropdown.setMaximumWidth(500)
        self.dropdown.setMinimumWidth(200)
        self.dropdown.setStyleSheet('background-color: #2b2d31;')
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
        try:
            lv1 = sorted(os.listdir(self.parent_dir))
            lv1 = [d for d in lv1 if os.path.isdir(os.path.join(self.parent_dir, d)) and d[0] not in hidden_prefixes]
            for folder in lv1:
                self.dropdown.addItem(folder)
        except FileNotFoundError:
            self.dropdown.addItem('No file/directory selected.')

class ContextMenu(QMenu):

    open_settings_signal = Signal()
    movable_signal = Signal(bool)
    close_signal = Signal()
    refresh_signal_context_menu = Signal()
    
    def __init__(self, parent):
        super().__init__(parent)

        self.toggle = True

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
        AboutWindow(self.parent())

def main():
    app = QApplication([])

    window = MainWindow()
    window.show()

    sys.exit(app.exec())

if __name__ == "__main__":
    main()