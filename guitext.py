import wx
import os

ID_ABOUT = 101
ID_EXIT = 200
ID_OPEN = 120
ID_SAVE = 300
ID_BUTTON1 = 200

class MainWindow(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(200,100))
        self.control = wx.TextCtrl(self, 1, style=wx.TE_MULTILINE)
        self.CreateStatusBar()
        filemenu = wx.Menu()
        filemenu.Append(ID_ABOUT, "&About", " Information about this program")
        filemenu.AppendSeparator()
        filemenu.Append(ID_OPEN, "&Open", " Open a file")
        filemenu.Append(ID_SAVE, "&Save", " Save a file")
        filemenu.AppendSeparator()
        filemenu.Append(ID_EXIT, "E&xit", " Terminate the program")
        menuBar = wx.MenuBar()
        menuBar.Append(filemenu, "&File")
        self.SetMenuBar(menuBar)
        wx.EVT_MENU(self, ID_ABOUT, self.OnAbout)
        wx.EVT_MENU(self, ID_OPEN, self.OnOpen)
        wx.EVT_MENU(self, ID_EXIT, self.OnExit)
        wx.EVT_MENU(self, ID_SAVE, self.OnSave)
        self.sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.buttons = []
        for i in range(0,6):
            self.buttons.append(wx.Button(self, ID_BUTTON1+i, "Button &"+`i`))
            self.sizer2.Add(self.buttons[i], 1, wx.EXPAND)

        self.sizer = wx.BoxSizer(wx.VERTICAL)
        self.sizer.Add(self.sizer2, 0, wx.SHAPED)
        self.sizer.Add(self.control, 1, wx.EXPAND)

        
        self.SetSizer(self.sizer)
        self.SetAutoLayout(1)
        self.sizer.Fit(self)
        
        self.Show(1)
    
    def OnAbout(self, e):
        d = wx.MessageDialog(self, " A sample editor \n in wxPython", "About Sample Editor", wx.OK)
        d.ShowModal()
        d.Destroy()

    def OnExit(self, e):
        self.Close(True)
    
    def OnOpen(self, e):
        self.dirname = ''
        dlg = wx.FileDialog(self, "Choose a file", self.dirname, "", "*.*", wx.OPEN)
        if dlg.ShowModal() == wx.ID_OK:
            self.filename = dlg.GetFilename()
            self.dirname = dlg.GetDirectory()
            f = open(os.path.join(self.dirname,self.filename), 'r')
            self.control.SetValue(f.read())
            f.close()
        dlg.Destroy()
    
    def OnSave(self, e):
        f = open(os.path.join(self.dirname,self.filename),'w')
        f.write(self.control.GetValue())
        f.close()

app = wx.PySimpleApp()
frame = MainWindow(None, -1, 'Small Editor')
app.MainLoop()