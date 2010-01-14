import wx
import os

ID_EXIT = 101

class MainWindow(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, wx.DefaultPosition, wx.Size(450,350))
        
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox = wx.BoxSizer(wx.VERTICAL)
        panel1 = wx.Panel(self, -1)
        panel2 = wx.Panel(self, -1)
        self.create_menus()
    
        self.tree = wx.TreeCtrl(panel1, 1,wx.DefaultPosition, (-1,-1), wx.TR_HIDE_ROOT|wx.TR_HAS_BUTTONS)
        root = self.tree.AddRoot('Ingredients')
        hops = self.tree.AppendItem(root, 'Hops')
        grains = self.tree.AppendItem(root,'Grains')
        yeasts = self.tree.AppendItem(root, 'Yeasts')
        self.tree.AppendItem(hops, 'Galena')
        self.tree.AppendItem(hops, 'Columbus')
        self.tree.AppendItem(hops, 'Cascade')
        self.tree.AppendItem(grains, '2 Row')
        self.tree.AppendItem(yeasts, 'Safeale US-05')
        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.OnSelChanged, id=1)
        self.display = wx.StaticText(panel2, -1, '', (10,10), style=wx.ALIGN_CENTRE)
        vbox.Add(self.tree, 1, wx.EXPAND)
        hbox.Add(panel1, 1, wx.EXPAND)
        hbox.Add(panel2, 1, wx.EXPAND)
        panel1.SetSizer(vbox)
        self.SetSizer(hbox)
        self.Centre()

    def OnSelChanged(self, e):
        item = e.GetItem()
        self.display.SetLabel(self.tree.GetItemText(item))
        
    def create_menus(self):
        filemenu = wx.Menu()
        filemenu.Append(ID_EXIT, '&Quit', ' Quit')
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")
        self.SetMenuBar(menuBar)
        wx.EVT_MENU(self, ID_EXIT, self.OnExit)
    
    def OnExit(self, e):
        self.Close(True)
        

class IngredientListSelector(wx.Panel):
    
    def __init__(self):
        self.panel = wx.Panel(self, wx.ID_ANY)
        
        self.tree = wx.TreeCtrl(self)
        root = self.tree.AddRoot("Example")
        
        items = ['test1','test2','test3']
        
        self.AddTreeNodes(root,items)
    
    def AddTreeNodes(self, parentItem, items):
        for item in items:
            if type(item) == str:
                self.tree.AppendItem(parentItem, item)
            else:
                newItem = self.tree.AppendItem(parentItem, item[0])
                self.AddTreeNodes(newItem,item[0])
        
class MyApp(wx.App):
    def OnInit(self):
        frame = MainWindow(None, -1, 'test')
        frame.Show(True)
        self.SetTopWindow(frame)
        return True
        
if __name__ == '__main__':
    app = MyApp(0)
    app.MainLoop()