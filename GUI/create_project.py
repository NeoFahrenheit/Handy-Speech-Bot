import wx
from DataManager.storage_manager import StorageManager
from GUI.dialogs import show_modal_dialog

class CreateProject(wx.Dialog):
    '''Window presented to the user when he wants to create a new project.'''

    def __init__(self, parent: wx.Window, model_names: list[str]):
        super().__init__(parent, title='Create new project')

        self.parent = parent
        self.model_names = model_names

        self._init_ui()
        self.SetSize((400, 330))
        self.CenterOnParent()

    def _init_ui(self) -> None:
        '''Initializes the UI.'''

        vbox = wx.BoxSizer(wx.VERTICAL)
        padding = wx.BoxSizer(wx.VERTICAL)
        panel = wx.Panel(self)

        # -- Static Text -- #
        name_st = wx.StaticText(panel, -1, 'Project name:')
        description_st = wx.StaticText(panel, -1, 'Description (optional):')
        models_st = wx.StaticText(panel, -1, 'Model:')

        name_st.SetToolTip(wx.ToolTip('Name of the project. It should not contain special characters. If any is found, it will be removed.'))
        description_st.SetToolTip(wx.ToolTip('Project description. Opcional.'))
        models_st.SetToolTip(wx.ToolTip('Model size to be used for this project. Models ended with ".en" can only recognize english. The smaller the sizer, it will be faster but less accurate.'))

        # -- Text Ctrls -- #
        self.name_tc = wx.TextCtrl(panel)
        self.description_tc = wx.TextCtrl(panel, style=wx.TE_MULTILINE)

        # -- Combo Boxes -- #
        self.models_cb = wx.ComboBox(panel, -1, self.model_names[0], choices=self.model_names, style=wx.CB_READONLY)

        # -- Button -- #
        create_btn = wx.Button(panel, -1, 'Create project')
        create_btn.Bind(wx.EVT_BUTTON, self._create_project)

        # -- Sizer Setup -- #
        padding.Add(name_st)
        padding.Add(self.name_tc, flag=wx.TOP | wx.EXPAND, border=5)
        
        padding.Add(description_st, flag=wx.TOP, border=15)
        padding.Add(self.description_tc, flag=wx.TOP | wx.EXPAND, border=5)
        
        padding.Add(models_st, flag=wx.TOP, border=15)
        padding.Add(self.models_cb, flag=wx.TOP | wx.EXPAND, border=5)
        
        padding.Add(create_btn, flag=wx.TOP | wx.ALIGN_CENTER, border=30)

        vbox.Add(padding, flag=wx.ALL | wx.EXPAND, border=10)
        panel.SetSizerAndFit(vbox)

    def _create_project(self, event) -> None:
        '''Create a new project.'''

        name = self.name_tc.GetValue()
        description = self.description_tc.GetValue()
        model = self.models_cb.GetValue()

        if len(name) > 50:
            show_modal_dialog(self, 'Name cannot be more than 50 characters', 'Length error', wx.OK | wx.ICON_ERROR)
            return
        
        if len(description) > 500:
            show_modal_dialog(self, 'Description cannot be more than 500 characters', 'Length error', wx.OK | wx.ICON_ERROR)
            return
        
        sm = StorageManager()
        sanitized_name = sm.sanitize_folder_filename(name)
        if sm.does_project_exists(sanitized_name):
            show_modal_dialog(self, 'A project with this name already exists. Please, choose another one.', 'Project already exists', wx.OK | wx.ICON_ERROR)
            return

        status = sm.create_project_files(sanitized_name, description, model)
        if status:
            self.parent.update_projects_entry()
            show_modal_dialog(self, 'Project created successfully', 'Success', wx.OK | wx.ICON_INFORMATION)
        else:
            show_modal_dialog(self, 'Error creating the project', 'Error', wx.OK | wx.ICON_ERROR)
            pass
        
        self.Close()