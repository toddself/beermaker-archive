import wx
from base import BaseWindow

class Test(wx.Frame, BaseWindow):

	def __init__(self, *args, **kw):
		wx.Frame.__init__(self, *args, **kw)
		
		panel = wx.Panel(self, -1)
		panel.SetSizer(self.buildLayout(panel))
		
	def layoutData(self):
	    return  ({'widget': wx.BoxSizer, 'flag': wx.ALL|wx.EXPAND, 'proportion': 1, 'style': wx.HORIZONTAL, 'widgets':(
	        {'widget': wx.StaticText, 'label': 'Hello World', 'flag': wx.ALL|wx.EXPAND, 'proportion': 0, 'border': 3},
	        {'widget': wx.Button, 'id': wx.ID_OK, 'event': {'event_type': wx.EVT_BUTTON, 'method': self.OnButton}},)},)
	
	def OnButton(self, event):
	    self.Close(True)

class TestApp(wx.App):
	def OnInit(self):
		test = Test(None, -1, "", size=(400,400))
		test.Show()
		return 1
	
if __name__ == '__main__':
    t = TestApp(0)
    t.MainLoop()