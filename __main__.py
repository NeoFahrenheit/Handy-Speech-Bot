import wx
from GUI.gui import MainFrame

if __name__ == '__main__':
    gui = wx.App()
    frame = MainFrame(None)
    frame.Show()
    gui.MainLoop()