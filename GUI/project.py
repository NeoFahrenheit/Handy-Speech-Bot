import wx
import wx.richtext as rt

class Project(wx.Frame):
    def __init__(self, parent: wx.Window, sanitized_name: str, path: str):
        """Creates a window that manages and interacts with a project.

        Args:
            parent (wx.Window): Parent of this window.
            sanitized_name (str): Name of the project, sanitized.
            path (str): A path for the root folder of the project.
        """        
        super().__init__(parent, title=sanitized_name, size=(900, 700))

        self.parent = parent
        self._init_ui()
        self.SetMinSize((900, 700))
        self.CenterOnScreen()

    def _init_ui(self):
        '''Initializes the UI.'''
        
        panel = wx.Panel(self)
        master_box = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)

        self.chat_rt = rt.RichTextCtrl(panel, -1, style=wx.TE_READONLY)
        self.input_tc = wx.TextCtrl(panel, -1, style=wx.TE_MULTILINE)
        self.files_lc = wx.ListCtrl(panel, -1)
        self.log_rt = rt.RichTextCtrl(panel, -1, style=wx.TE_READONLY)

        self.info_lc = wx.ListCtrl(panel, -1, size=(300, 220), style=wx.LC_REPORT)
        self.info_lc.InsertColumn(0, 'Info', wx.LIST_FORMAT_CENTRE)
        self.info_lc.InsertColumn(1, 'Value', wx.LIST_FORMAT_LEFT)
        self.info_lc.SetColumnWidth(0, 110)
        self.info_lc.SetColumnWidth(1, 200)
        self.info_lc.InsertItem(0, 'File')
        self.info_lc.InsertItem(1, 'Duration')
        self.info_lc.InsertItem(2, 'Inserted on')
        self.info_lc.InsertItem(3, 'Processing time')
        self.info_lc.InsertItem(4, 'Language')
        self.info_lc.InsertItem(5, 'Source')
        self.info_lc.InsertItem(6, 'Model')
        self.info_lc.InsertItem(7, 'LLM')
        self.info_lc.InsertItem(8, 'Database')

        chat_box = wx.BoxSizer(wx.VERTICAL)
        chat_box.Add(self.chat_rt, proportion=5, flag=wx.EXPAND)
        chat_box.Add(self.input_tc, proportion=0, flag=wx.TOP | wx.EXPAND, border=5)
        
        files_box = wx.BoxSizer(wx.VERTICAL)
        files_box.Add(self.files_lc, proportion=3, flag=wx.EXPAND)
        files_box.Add(self.info_lc, proportion=0, flag=wx.TOP | wx.EXPAND, border=10)

        top_box = wx.BoxSizer(wx.HORIZONTAL)   
        top_box.Add(chat_box, proportion=4, flag=wx.EXPAND)
        top_box.Add(files_box, proportion=1, flag=wx.LEFT | wx.EXPAND, border=5)

        vbox.Add(top_box, proportion=4, flag=wx.EXPAND)
        vbox.Add(self.log_rt, proportion=1, flag=wx.TOP | wx.EXPAND, border=5)

        master_box.Add(vbox, proportion=1, flag=wx.ALL | wx.EXPAND, border=5)
        panel.SetSizer(master_box)