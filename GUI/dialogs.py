import wx

def show_modal_dialog(parent: wx.Window, message: str, title: str, style: int) -> None:
    """Creates a `wx.MessageDialog` and displays it, blocking the UI and app flow.

    Args:
        parent (wx.Window): Window that onws this Dialog.
        message (str): Message for the body.
        title (str): Title for the Dialog.
        style (int): Style for Dialog, like wx.OK | wx.ICON_INFORMATION
    """    
    
    dialog = wx.MessageDialog(parent, message, title, style)
    dialog.ShowModal()