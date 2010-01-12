import wx

class Form1(wx.Panel):
    def __init__(self, parent, id):
        wx.Panel.__init__(self, parent, id)
        self.quote = wx.StaticText(self, -1, "Your quote:", wx.Point(20,30), wx.Size(200, -1))
        self.logger = wx.TextCtrl(self, 5, "", wx.Point(300,200), wx.Size(200,300), wx.TE_MULTILINE | wx.TE_READONLY)
        
        self.button = wx.Button(self, 10, "Save", wx.Point(200,325))    
        wx.EVT_BUTTON(self, 10, self.ClickIt)
        self.lblname = wx.StaticText(self, -1, "Your name :", wx.Point(20,60))
        self.editname = wx.TextCtrl(self, 20, "Enter here your name", wx.Point(150, 60), wx.Size(140,-1))
        wx.EVT_TEXT(self, 20, self.EvtText)
        wx.EVT_CHAR(self.editname, self.EvtChar)
        self.sampleList = ['friends','advertising','web search', 'Yellow Pages',]
        self.lblhear = wx.StaticText(self,-1,"How did you hear from us ?",wx.Point(20,90))
        self.edithear = wx.ComboBox(self, 30, "", wx.Point(150, 90), wx.Size(95, -1), self.sampleList, wx.CB_DROPDOWN)
        wx.EVT_COMBOBOX(self, 30, self.EvtComboBox)
        wx.EVT_TEXT(self, 30, self.EvtText)
        self.insure = wx.CheckBox(self, 40, "Do you want Insured Shipment ?", wx.Point(20,180))
        wx.EVT_CHECKBOX(self, 40, self.EvtCheckBox)
        self.radioList = ['blue','red','yellow','orange','green','purple','navy blue','black','gray']
        rb = wx.RadioBox(self, 50, "What color would you like ?", wx.Point(20, 210), wx.DefaultSize, self.radioList, 3, wx.RA_SPECIFY_COLS)
        wx.EVT_RADIOBOX(self, 50, self.EvtRadioBox)
        
    def EvtRadioBox(self, event):
        self.logger.AppendText('EvtRadioBox: %d\n' % event.GetInt())
    
    def EvtComboBox(self, event):
        self.logger.AppendText('EvtComboBox: %s\n' % event.GetString())
    
    def ClickIt(self, event):
        self.logger.AppendText(" Click on object with ID %d\n" % event.GetId())
    
    def EvtText(self, event):
        self.logger.AppendText('EvtText: %s\n' % event.GetString())
        
    def EvtChar(self, event):
        self.logger.AppendText('EvtChar: %d\b' % event.GetKeyCode())
        event.Skip()
    
    def EvtCheckBox(self, event):
        self.logger.AppendText('EvtCheckBox %d\n' % event.Checked())

app = wx.PySimpleApp()
frame = wx.Frame(None, -1, " Our first control")
Form1(frame, -1)
frame.Show(1)
app.MainLoop()