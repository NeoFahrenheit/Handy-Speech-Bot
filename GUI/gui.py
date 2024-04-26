import wx
from Cocoa import NSApp, NSApplication
from DataManager import storage_manager

class MainFrame(wx.Frame):
    '''Create the main frame for the GUI version of the application.'''
    def __init__(self, parent):
        super().__init__(parent, title='Handy Speech Bot', size=(600, 400))

        self.CenterOnScreen()
        self.sm = storage_manager.StorageManager()
        
        self.project_names = self.sm.get_projects()
        self._init_gui()
        self.CreateStatusBar()
        self.go_foreground()
    

    def _init_gui(self) -> None:
        self.panel = wx.Panel(self)
        base_box = wx.BoxSizer(wx.HORIZONTAL)
        self.left_box = wx.BoxSizer(wx.VERTICAL)
        right_box = wx.BoxSizer(wx.VERTICAL)

        self.load_project_buttons()
        right_box.Add(wx.TextCtrl(self.panel, -1), proportion=1, flag=wx.EXPAND)

        base_box.Add(self.left_box, proportion=1, flag=wx.ALL | wx.EXPAND, border=15)
        base_box.Add(right_box, proportion=2, flag=wx.ALL | wx.EXPAND, border=15)

        self.panel.SetSizer(base_box)
        self._init_menu()


    def _init_menu(self) -> None:
        menu = wx.MenuBar()
        projects_menu = self.load_projects_menu()
        media = wx.Menu()
        file = wx.Menu()
        help = wx.Menu()
        
        # -- File menu -- #
        open = file.Append(-1, 'Open a file', 'Opens a file from your computer')

        # -- Media menu -- #
        add_offline_media = media.Append(-1, 'Add audio file', 'Add an audio file from your computer.')
        add_online_media = media.Append(-1, 'Add internet video', 'Add a video link from the internet, like YouTube or Twitch.')
        add_live_recording = media.Append(-1, 'Record audio', 'Record an audio stream from your system or microphone.')
        
        menu.Append(file, 'File')
        menu.Append(projects_menu, 'Projects')
        menu.Append(media, 'Media')
        menu.Append(help, 'Help')

        self.SetMenuBar(menu)

    def load_projects_menu(self) -> wx.Menu:
        menu = wx.Menu()
        menu.Append(-1, 'Create project', 'Create a new project')
        menu.Append(-1, 'Delete project', 'Deletes an existing project')
        menu.AppendSeparator()

        for name in self.project_names:
            menu.Append(-1, name)

        return menu

    def load_project_buttons(self):
        #self.left_box.Clear()
        self.left_box.Add(wx.Button(self.panel, -1, 'Create new project'), flag=wx.EXPAND)

        i = 0
        for project in self.project_names:
            border = 30 if i == 0 else 10
            self.left_box.Add(wx.Button(self.panel, -1, project), flag=wx.TOP | wx.EXPAND, border=border)
            i += 1      

    def go_foreground(self):
        NSApplication.sharedApplication()
        NSApp().activateIgnoringOtherApps_(True)
