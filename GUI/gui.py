import json
import os
import wx
import wx.lib.scrolledpanel as scrolled
from Cocoa import NSApp, NSApplication
from DataManager import storage_manager
from GUI.create_project import CreateProject
from GUI.dialogs import show_modal_dialog

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
        self.scrolled = scrolled.ScrolledPanel(self.panel)
        self.scrolled_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.scrolled.SetSizer(self.scrolled_sizer)
        right_box = wx.BoxSizer(wx.VERTICAL)
        
        self._create_project_info_sizer(right_box)
        self.load_project_buttons()

        base_box.Add(self.scrolled, proportion=1, flag=wx.ALL | wx.EXPAND, border=15)
        base_box.Add(right_box, proportion=2, flag=wx.ALL | wx.EXPAND, border=15)

        self.panel.SetSizer(base_box)
        self._init_menu()

    def _create_project_info_sizer(self, sizer: wx.BoxSizer) -> None:
        """Creates the info panel for the current selected project.

        Args:
            sizer (wx.BoxSizer): The Sizer to be added to.
        """        

        font = wx.Font(25, wx.MODERN, wx.NORMAL, wx.FONTWEIGHT_BOLD, False, u'Consolas')
        self.project_st = wx.StaticText(self.panel, -1, 'Project name')
        self.project_st.SetFont(font)

        self.description_st = wx.StaticText(self.panel, -1, 'Project description')
        self.files_st = wx.StaticText(self.panel, -1, 'Files: ')
        self.files_number_st = wx.StaticText(self.panel, -1, '0')
        self.model_st = wx.StaticText(self.panel, -1, 'Model: ')
        self.model_name_st = wx.StaticText(self.panel, -1, 'large-v3')
        self.date_st = wx.StaticText(self.panel, -1, 'Created at: ')
        self.date_value_st = wx.StaticText(self.panel, -1, '1900-01-01')

        files_sizer = wx.BoxSizer(wx.HORIZONTAL)
        files_sizer.Add(self.files_st)
        files_sizer.Add(self.files_number_st, flag=wx.LEFT, border=5)

        models_sizer = wx.BoxSizer(wx.HORIZONTAL)
        models_sizer.Add(self.model_st)
        models_sizer.Add(self.model_name_st, flag=wx.LEFT, border=5)
        
        date_sizer = wx.BoxSizer(wx.HORIZONTAL)
        date_sizer.Add(self.date_st)
        date_sizer.Add(self.date_value_st, flag=wx.LEFT, border=5)

        buttons_sizer = wx.BoxSizer(wx.HORIZONTAL)
        open_btn = wx.Button(self.panel, -1, 'Open project')
        open_btn.Bind(wx.EVT_BUTTON, self._open_project)
        buttons_sizer.Add(open_btn)

        delete_btn = wx.Button(self.panel, -1, 'Delete project')
        delete_btn.Bind(wx.EVT_BUTTON, self._delete_project)
        buttons_sizer.Add(delete_btn, flag=wx.LEFT, border= 50)


        sizer.Add(self.project_st)
        sizer.Add(self.description_st, flag=wx.TOP, border=15)
        sizer.Add(files_sizer, flag=wx.TOP, border=15)
        sizer.Add(models_sizer, flag=wx.TOP, border=15)
        sizer.Add(date_sizer, flag=wx.TOP, border=15)
        sizer.Add(buttons_sizer, flag=wx.TOP | wx.ALIGN_CENTER, border=25)


    def _init_menu(self) -> None:
        self.menu = wx.MenuBar()
        self.projects_menu = wx.Menu()
        media = wx.Menu()
        file = wx.Menu()
        help = wx.Menu()
        
        # -- File menu -- #
        open = file.Append(-1, 'Open a file', 'Opens a file from your computer')

        # -- Media menu -- #
        add_offline_media = media.Append(-1, 'Add audio file', 'Add an audio file from your computer.')
        add_online_media = media.Append(-1, 'Add internet video', 'Add a video link from the internet, like YouTube or Twitch.')
        add_live_recording = media.Append(-1, 'Record audio', 'Record an audio stream from your system or microphone.')
        
        self.menu.Append(file, 'File')
        self.menu.Append(self.projects_menu, 'Projects')
        self.menu.Append(media, 'Media')
        self.menu.Append(help, 'Help')

        self.load_projects_menu()
        self.SetMenuBar(self.menu)

    def update_projects_entry(self) -> None:
        '''Updates the projects that appears in the app. It updates the MenuBar and the button on the main screen.'''
        
        self.project_names = self.sm.get_projects()
        self.load_projects_menu()
        self.load_project_buttons()

    def load_projects_menu(self) -> None:
        self.menu.Remove(1)

        projects_menu = wx.Menu()
        create = projects_menu.Append(-1, 'Create project', 'Create a new project')
        projects_menu.Append(-1, 'Delete project', 'Deletes an existing project')
        projects_menu.AppendSeparator()

        self.Bind(wx.EVT_MENU, self.on_create_project, create)

        for name in self.project_names:
            projects_menu.Append(-1, name)

        self.menu.Insert(1, projects_menu, 'Projects')

    def load_project_buttons(self):
        self.scrolled_sizer.Clear(True)
        vbox = wx.BoxSizer(wx.VERTICAL)

        create_btn = wx.Button(self.scrolled, -1, 'Create new project')
        vbox.Add(create_btn, flag=wx.EXPAND)
        create_btn.Bind(wx.EVT_BUTTON, self.on_create_project)

        i = 0
        for project in self.project_names:
            border = 30 if i == 0 else 10
            btn = wx.Button(self.scrolled, -1, project)
            btn.Bind(wx.EVT_BUTTON, self._on_button_clicked)
            vbox.Add(btn, flag=wx.TOP | wx.EXPAND, border=border)
            i += 1

        self.scrolled_sizer.Add(vbox)
        self.scrolled_sizer.Add(wx.Size(5, 1))
        self.scrolled.SetupScrolling(scroll_x=False)
        self.Layout()

    def _on_button_clicked(self, event) -> None:
        name = event.GetEventObject().GetLabel()
        path = os.path.join(self.sm.projects_path, name, 'project_settings.json')
        data = {}
        if os.path.isfile(path):
            with open(path, "r", encoding="utf-8") as f:
                text = f.read()
                data = json.loads(text)
        else:
            show_modal_dialog(self, 'Error loading project data. File project_settings.json not found.', 'File not found', wx.OK | wx.ICON_ERROR)
            return
        
        self.project_st.SetLabel(data['name'])
        self.description_st.SetLabel(data['description'])
        self.files_number_st.SetLabel(str(data['number_files']))
        self.model_name_st.SetLabel(data['model'])
        self.date_value_st.SetLabel(data['created_at'])


    def on_create_project(self, event) -> None:
        create_window = CreateProject(self, [model for model in self.sm.app_data['models'].keys()])
        create_window.ShowModal()
        print('aaaaaaaa')
        
    def _open_project(self, event) -> None:
        pass
    
    def _delete_project(self, event) -> None:
        pass

    def go_foreground(self):
        NSApplication.sharedApplication()
        NSApp().activateIgnoringOtherApps_(True)
