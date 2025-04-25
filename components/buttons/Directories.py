from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QHBoxLayout, QStackedWidget
from PySide6.QtCore import Signal, QSize, Qt
import os, json
from components.buttons.DirButton import DirButton

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
        
    def generate(self, dirpath, toobig):

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
        opsys = os.name
        if opsys == 'posix':
            delim = '/'
        else:
            delim = '\\'
        if dirpath[-1] != delim:
            dirpath += delim

        # big vars
        # columns = 9
        # rows = 7
        # maxrows = 15
        # maxsize = 100

        dirs = self.get_directories(dirpath, 9, 7, 15, 100)

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
                                button.setFixedWidth(175)
                                collayout.addWidget(button)
                                #collayout.addStretch()
                                colslayout.addWidget(column)
                                colslayout.setAlignment(Qt.AlignmentFlag.AlignRight)
                                continue
                            else:
                                button = DirButton(parentdirpath, folder, self.color1, self.fontcolor)
                                button.setFixedWidth(175)
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
                                    button.setFixedWidth(155)
                                    subfolderslayout.addWidget(button)

                                else:

                                    # this is TIER THREE

                                    # subsubfolders
                                    for subsubfolder in subfolder:
                                        subsubdirpath = os.path.join(subdirpath, subsubfolder)
                                        button = DirButton(subsubdirpath, subsubfolder, self.color3, self.fontcolor)
                                        button.setFixedWidth(140)
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

    def nested_len(self, arr):
        if type(arr) == list:
            return sum(self.nested_len(entry) for entry in arr)
        else:
            return 1

    def get_directories(self, source, columns, rows, maxrows, maxsize):

        toobig = False

        hidden_prefixes = ['.', '$']

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

                    if self.nested_len(subfolders) > maxrows:
                        subfolders = subfolders[0:maxrows]
                        subfolders.append('p...')
                        toobig = True
                        break
                
                # append to wrapper array
                subarray.append(subfolders)
                
                if self.nested_len(subarray) > maxsize:
                    toobig = True
                    break

                # append to parent array
                folderslist.append(subarray)
        except FileNotFoundError:
            folderslist = 'filenotfound'

        except PermissionError:
            folderslist = 'permerror'

        return [toobig, folderslist]
