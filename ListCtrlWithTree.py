import wx

class ListCtrlWithTree(wx.ListCtrl):
    """Used for creating a list ctrl with a tree"""
    
    childIndent = "     "
    
    def __init__(self, ctrlColumn=0, *args, **kw):
        wx.ListCtrl.__init__(self, *args, **kw)
        self.ctrlColumn = ctrlColumn

    def AddChild(self, child, parent):
        pass
    
    def RemoveChild(self, child):
        pass