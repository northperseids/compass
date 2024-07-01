import wx
import os
import webbrowser
import textwrap
import wx.lib
import wx.lib.scrolledpanel
import json

toobig = False

greenscheme = ['#b8fac2', '#14c443', '#137724', '#000000', '#d5e0d7']
bluescheme = ['#95b2fb', '#3f61f2', '#212ed4', '#000000', '#dce4fd']
redscheme = ['#ffa39b', '#ff4131', '#c2180a', '#000000', '#ffe1df']
colorblindscheme = ['#5da899', '#94cbec', '#c26a77', '#000000', '#dddddd']

about_text = "Compass v.0.1\n\nFile-mapping software.\n\nhttps://github.com/\nnorthperseids/compass\n\n©Elijah North\nMIT License"

show_warning = True

hidden_prefixes = ['.', '$']

columns = 50
rows = 50

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

        for i, entry in enumerate(lv1):
            # prevent too many folders
            if i > columns:
                toobig = True
                break

            # make wrapper array for individual lv1 folders
            subarray = []

            # add header folders
            subarray.append(entry)

            # get level 2 dirs
            folder2 = sorted(os.listdir(os.path.join(source, entry)))
            folder2 = [d for d in folder2 if os.path.isdir(os.path.join(source, entry, d)) and d[0] not in hidden_prefixes]
            
            # make another wrapper array for lv2 folders
            subfolders = []

            for i, subentry in enumerate(folder2):
                # prevent too many folders again
                if i > columns:
                    toobig = True
                    break

                # add lv2 header folders
                subfolders.append(subentry)

                # get level 3 dirs
                folder3 = sorted(os.listdir(os.path.join(source, entry, subentry)))
                folder3 = [d for d in folder3 if os.path.isdir(os.path.join(source, entry, subentry, d)) and d[0] not in hidden_prefixes]

                # append to wrapper array
                subfolders.append(folder3)
            
            # append to wrapper array
            subarray.append(subfolders)
            
            if nested_len(subarray) > rows:
                toobig = True

            # append to parent array
            folderslist.append(subarray)
    except FileNotFoundError:
        folderslist = 'filenotfound'

    except PermissionError:
        folderslist = 'permerror'

    return [toobig, folderslist]

class TooBigDialog(wx.Dialog):
    def __init__(self, parent):
        super().__init__(parent, title='ERROR', size=(250,200))
        panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)

        self.checkbox = wx.CheckBox(panel, label='Do not show this again')
        self.checkbox.Bind(wx.EVT_CHECKBOX, self.on_check)

        self.btn = wx.Button(panel, wx.ID_OK, label='Okay', size=(50,30))

        self.text = wx.StaticText(panel, label='Error: Too many folders in\nspecified directory. A truncated\nlist will be shown.')

        self.sizer.AddSpacer(10)
        self.sizer.Add(self.text, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.sizer.AddSpacer(20)
        self.sizer.Add(self.checkbox, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.sizer.AddSpacer(20)
        self.sizer.Add(self.btn, 0, wx.ALIGN_CENTER_HORIZONTAL)
        panel.SetSizer(self.sizer)

    def on_check(self, e):
        global show_warning
        if self.checkbox.GetValue() == True:
            show_warning = False
        else:
            show_warning = True

class PopupDialog(wx.Dialog):
    def __init__(self, parent, title, label, x, y):
        super().__init__(parent, title=title, size=(x,y))
        panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.btn = wx.Button(panel, wx.ID_OK, label='Okay', size=(50,30))
        self.text = wx.StaticText(panel, label=label)
        self.sizer.AddSpacer(20)
        self.sizer.Add(self.text, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.sizer.AddSpacer(20)
        self.sizer.Add(self.btn, 0, wx.ALIGN_CENTER_HORIZONTAL)
        panel.SetSizer(self.sizer)

class SettingsDialog(wx.Dialog):
    def __init__(self, parent, title):
        super().__init__(parent, title=title, size=(300,300))
        panel = wx.Panel(self)
        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.btn = wx.Button(panel, wx.ID_OK, label='Back', size=(50,30))
        self.text = wx.StaticText(panel, label='Color theme: ')
        
        with open('./settings.json', 'r+') as f:
            config = json.load(f)
            theme = config['theme']
        self.selected_color = theme

        self.color_dropdown = wx.ComboBox(panel, size=wx.DefaultSize)
        colors = ['Green', 'Blue', 'Red', 'Colorblind']
        for color in colors:
            self.color_dropdown.Append(color)
        self.color_dropdown.Bind(wx.EVT_COMBOBOX, self.on_select)

        self.color_dropdown.SetStringSelection(f'{self.selected_color}')

        self.sizer.AddSpacer(20)
        self.sizer.Add(self.text, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.sizer.AddSpacer(20)
        self.sizer.Add(self.color_dropdown, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.sizer.AddSpacer(20)
        self.sizer.Add(self.btn, 0, wx.ALIGN_CENTER_HORIZONTAL)
        panel.SetSizer(self.sizer)

    def on_select(self, e):
        self.selected_color = self.color_dropdown.GetStringSelection()
        with open('./settings.json', 'r+') as f:
            config = json.load(f)
            dirpath = config['dirpath']
            newconfig = {"dirpath":f"{dirpath}","theme":f"{self.selected_color}"}
            f.seek(0)
            json.dump(newconfig, f)
            f.truncate()
        frame.reconstruct(dirpath)

class PopMenu(wx.Menu):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.dirpath = ''

        set_as_dir = wx.MenuItem(self, wx.ID_ANY, 'Set as Directory')
        self.Append(set_as_dir)

class MyFrame(wx.Frame):    
    def __init__(self):
        super().__init__(parent=None, title='Compass', size=(1300,930))

        self.Bind(wx.EVT_CLOSE, self.save_dir)

        self.panel = wx.lib.scrolledpanel.ScrolledPanel(self, -1, size=(1300, 930))
        self.panel.SetupScrolling(scroll_x=False)

        with open('settings.json', 'r') as f:
            config = json.load(f)
            start_dir = config['dirpath']
            self.theme = config['theme']

        if self.theme == 'Green':
            scheme = greenscheme
        elif self.theme == 'Blue':
            scheme = bluescheme
        elif self.theme == 'Red':
            scheme = redscheme
        elif self.theme == 'Colorblind':
            scheme = colorblindscheme

        bgcolor = scheme[4]

        self.panel.SetBackgroundColour(bgcolor)

        top_menu = wx.MenuBar()
        menu = wx.Menu()
        menu_settings = menu.Append(wx.ID_ANY, 'Settings')
        menu_about = menu.Append(wx.ID_ANY, 'About')
        top_menu.Append(menu,'File')
        self.SetMenuBar(top_menu)

        self.Bind(wx.EVT_MENU, self.show_settings, menu_settings)
        self.Bind(wx.EVT_MENU, self.show_about, menu_about)

        self.wrapper = wx.GridBagSizer(4, 4)

        self.dirlabel = wx.TextCtrl(self.panel, size=(550,30))
        self.dirlabel.SetValue(start_dir)

        dirbutton = wx.Button(self.panel, size=(150,30))
        dirbutton.SetLabel('Update Directory')
        dirbutton.Bind(wx.EVT_BUTTON, self.on_press_dir_button)

        upbutton = wx.Button(self.panel, size=(75,30))
        upbutton.SetLabel('⬆')
        upbutton.Bind(wx.EVT_BUTTON, self.on_press_up_button)

        self.header = wx.GridBagSizer(1,3)
        self.header.Add(self.dirlabel, pos=(1,2))
        self.header.Add(dirbutton, pos=(1,3))
        self.header.Add(upbutton, pos=(1,1))

        self.wrapper.Add(self.header, pos=(1,2))

        self.stuff = self.create_buttons(start_dir, self.panel)

        if self.stuff[0] == True and show_warning == True:
            TooBigDialog(self).ShowModal()

        self.newsizer = self.stuff[1]
        
        self.wrapper.Add(self.newsizer, pos=(2,2))

        self.panel.SetSizer(self.wrapper)

        self.Show()

    def show_settings(self, e):
        SettingsDialog(self, 'Settings').Show()

    def show_about(self, e):
        PopupDialog(self, 'ABOUT', about_text, 275, 300).ShowModal()

    def save_dir(self, e):
        dirpath = self.dirlabel.GetValue()
        with open('settings.json', 'r+') as f:
            currentsettings = json.load(f)
            theme = currentsettings['theme']
            config = {"dirpath":f"{dirpath}","theme":f"{theme}"}
            f.seek(0)
            json.dump(config, f)
            f.truncate()
        if type(e) == wx.CloseEvent:
            self.Destroy()

    def on_right_down(self, e):
        coords = self.panel.ScreenToClient(wx.GetMousePosition())
        menu = PopMenu(self)
        menu.dirpath = e.GetEventObject().dirpath
        menu.Bind(wx.EVT_MENU, self.right_click_dir)
        self.PopupMenu(menu, coords)
        menu.Destroy()

    def reconstruct(self, directory):

        self.wrapper.Clear(delete_windows=True)
        self.dirlabel = wx.TextCtrl(self.panel, size=(550,30))
        self.dirlabel.SetValue(directory)

        dirbutton = wx.Button(self.panel, size=(150,30))
        dirbutton.SetLabel('Update Directory')
        dirbutton.Bind(wx.EVT_BUTTON, self.on_press_dir_button)

        upbutton = wx.Button(self.panel, size=(75,30))
        upbutton.SetLabel('⬆')
        upbutton.Bind(wx.EVT_BUTTON, self.on_press_up_button)
        
        self.header = wx.GridBagSizer(1,2)
        self.header.Add(self.dirlabel, pos=(1,2))
        self.header.Add(dirbutton, pos=(1,3))
        self.header.Add(upbutton, pos=(1,1))

        self.wrapper.Add(self.header, pos=(1,2))

        self.stuff = self.create_buttons(directory, self.panel)
        if self.stuff == None:
            PopupDialog(self, 'ERROR', 'ERROR: File not found.', 250, 150).ShowModal()
            self.newsizer = wx.FlexGridSizer(0, 0, 0)
        else:
            self.newsizer = self.stuff[1]
            if self.stuff[0] == True and show_warning == True:
                TooBigDialog(self).ShowModal()
        self.newsizer.Layout()
        self.wrapper.Add(self.newsizer, pos=(2,2))
        # self.panel.FitInside() is necessary to make sure the WHOLE list is scrollable and not cut off at the bottom.
        self.panel.FitInside()
        self.wrapper.Layout()

    def right_click_dir(self, e):
        newdir = e.GetEventObject().dirpath
        self.reconstruct(newdir)

    def on_press_dir_button(self, e):
        newdir = self.dirlabel.GetValue()
        self.save_dir(None)
        self.reconstruct(newdir)

    def on_press_up_button(self, e):
        currentdir = self.dirlabel.GetValue()
        newdir = os.path.dirname(currentdir)
        self.reconstruct(newdir)

    def on_press(self, e):
        webbrowser.open(e.GetEventObject().dirpath)

    def create_buttons(self, directory, panel):

        with open('settings.json', 'r') as f:
            config = json.load(f)
            self.theme = config['theme']

        if self.theme == 'Green':
            scheme = greenscheme
        elif self.theme == 'Blue':
            scheme = bluescheme
        elif self.theme == 'Red':
            scheme = redscheme
        elif self.theme == 'Colorblind':
            scheme = colorblindscheme

        lv1color = scheme[0]
        lv2color = scheme[1]
        lv3color = scheme[2]
        lv4color = scheme[2]
        textcolor = scheme[3]
        bgcolor = scheme[4]

        self.panel.SetBackgroundColour(bgcolor)

        wrap_sizer_1 = wx.GridSizer(3, 1, 0, 0)

        dirs = get_directories(directory)

        toobig = dirs[0]
        array = dirs[1]

        if dirs[1] == 'filenotfound':
            PopupDialog(self, 'ERROR', 'ERROR: File not found.', 250, 150).ShowModal()
            label = wx.StaticText(panel, label='Please enter a directory.')
            label.SetForegroundColour('#000000')
            wrap_sizer_1.Add(label)
            return [toobig, wrap_sizer_1]
        elif dirs[1] == 'permerror':
            PopupDialog(self, 'ERROR', 'ERROR: Access denied.', 250, 150).ShowModal()
            label = wx.StaticText(panel, label='Please enter a directory.')
            label.SetForegroundColour('#000000')
            wrap_sizer_1.Add(label)
            return [toobig, wrap_sizer_1]
        else:

            arr1 = array[0:14]
            arr2 = array[15:29]
            arr3 = array[30:44]
            parent_arr = [arr1, arr2, arr3]

            for arr in parent_arr:
                
                wrap_sizer = wx.FlexGridSizer(8, 1, 20)

                for entry in arr:
                    subsizer = wx.GridSizer(15, 1, 5, 0)
                    parentpath = ''
                    for level1 in entry:
                        childcount = len(subsizer.GetChildren())
                        if childcount > 13:
                            toobig = True
                            button = wx.Button(panel, size=(70, 45))
                            button.SetLabel('...')
                            button.dirpath = os.path.dirname(os.path.join(directory, level1))
                            button.Bind(wx.EVT_BUTTON, self.on_press)
                            button.Bind(wx.EVT_RIGHT_DOWN, self.on_right_down)
                            button.SetBackgroundColour(lv4color)
                            button.SetForegroundColour(textcolor)
                            subsizer.Add(button)
                            parentpath = os.path.join(directory, level1)
                            break
                        elif type(level1) == bool:
                            pass
                        elif type(level1) != list:
                            button = wx.Button(panel, size=(130, 45))
                            textlabel = "\n".join(textwrap.wrap(level1, width=14))
                            if len(textlabel) > 28:
                                textlabel = textwrap.shorten(textlabel, width=26, placeholder='...')
                            button.SetLabel(textlabel)
                            button.dirpath = os.path.join(directory, level1)
                            button.Bind(wx.EVT_BUTTON, self.on_press)
                            button.Bind(wx.EVT_RIGHT_DOWN, self.on_right_down)
                            button.SetBackgroundColour(lv1color)
                            button.SetForegroundColour(textcolor)
                            subsizer.Add(button)
                            parentpath = os.path.join(directory, level1)
                        else:
                            for level2 in level1:
                                childcount = len(subsizer.GetChildren())
                                if childcount > 14:
                                    break
                                elif childcount > 13:
                                    toobig = True
                                    button = wx.Button(panel, size=(70, 45))
                                    button.SetLabel('...')
                                    button.dirpath = os.path.join(directory, parentpath)
                                    button.Bind(wx.EVT_BUTTON, self.on_press)
                                    button.Bind(wx.EVT_RIGHT_DOWN, self.on_right_down)
                                    button.SetBackgroundColour(lv4color)
                                    button.SetForegroundColour(textcolor)
                                    subsizer.Add(button)
                                    parentpath2 = parentpath
                                    break
                                elif type(level2) != list:
                                    button = wx.Button(panel, size=(110, 45))
                                    textlabel = "-\n".join(textwrap.wrap(level2, width=12))
                                    if len(textlabel) > 24:
                                        textlabel = textwrap.shorten(textlabel, width=23, placeholder='...')
                                    button.SetLabel(textlabel)
                                    button.dirpath = os.path.join(directory, parentpath, level2)
                                    button.Bind(wx.EVT_BUTTON, self.on_press)
                                    button.Bind(wx.EVT_RIGHT_DOWN, self.on_right_down)
                                    button.SetBackgroundColour(lv2color)
                                    button.SetForegroundColour(textcolor)
                                    subsizer.Add(button)
                                    parentpath2 = os.path.join(directory, parentpath, level2)
                                else:
                                    for level3 in level2:
                                        childcount = len(subsizer.GetChildren())
                                        if childcount > 14:
                                            break
                                        if childcount > 13:
                                            toobig = True
                                            button = wx.Button(panel, size=(70, 45))
                                            button.SetLabel('...')
                                            button.dirpath = os.path.join(directory, parentpath2)
                                            button.Bind(wx.EVT_BUTTON, self.on_press)
                                            button.Bind(wx.EVT_RIGHT_DOWN, self.on_right_down)
                                            button.SetBackgroundColour(lv4color)
                                            button.SetForegroundColour(textcolor)
                                            subsizer.Add(button)
                                            break
                                        elif type(level3) != list:
                                            button = wx.Button(panel, size=(90, 45))
                                            textlabel = "-\n".join(textwrap.wrap(level3, width=8))
                                            if len(textlabel) > 16:
                                                textlabel = textwrap.shorten(textlabel, width=15, placeholder='...')
                                            button.SetLabel(textlabel)
                                            button.dirpath = os.path.join(directory, parentpath2, level3)
                                            button.Bind(wx.EVT_BUTTON, self.on_press)
                                            button.Bind(wx.EVT_RIGHT_DOWN, self.on_right_down)
                                            button.SetBackgroundColour(lv3color)
                                            button.SetForegroundColour(textcolor)
                                            subsizer.Add(button)
                                        else:
                                            pass
                    
                    wrap_sizer.Add(subsizer, flag=wx.BOTTOM, border=20)

                wrap_sizer_1.Add(wrap_sizer)
            
            return [toobig, wrap_sizer_1]

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame()
    app.MainLoop()
