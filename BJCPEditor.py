#!/usr/bin/env python
import os
import sys

import wx
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin, ColumnSorterMixin

from db import DataStore
from models import BJCPStyle, BJCPCategory

os.environ['VERSIONER_PYTHON_PREFER_32_BIT'] = 'yes'

# box sizer 1 - horizontal
# +------------------------------------------------------+
# |   style |                                            |
# |   list  |     editor                                 |
# |         |                                            |
# |         |                                            |
# +------------------------------------------------------+
# |         |                                            |
# | beer    |                                            |
# | list    |   editor                                   |
# |         |                                            |
# |         |                                            |
# |         |                                            |
# |         |                                            |
# |         |                                            |
# +------------------------------------------------------+

ID_BUTTON_SAVE = 100
ID_BUTTON_LOAD = 110

class SortedAutoWidthListCtrl(wx.ListCtrl, ListCtrlAutoWidthMixin, ColumnSorterMixin):
    def __init__(self, parent, dataset):
        wx.ListCtrl.__init__(self, parent, -1, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        ListCtrlAutoWidthMixin.__init__(self)
        ColumnSorterMixin.__init__(self, 2)
        self.itemDataMap = dataset
        
    def GetListCtrl(self):
        return self

class MainWindow(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size=(850,600))
        
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        vbox1 = wx.BoxSizer(wx.VERTICAL)
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        vbox3 = wx.BoxSizer(wx.VERTICAL)
        
        pnl1 = wx.Panel(self, -1, style=wx.SIMPLE_BORDER)
        
        dataset = self.getDataSet()
        self.lc = SortedAutoWidthListCtrl(self, dataset)
        self.lc.InsertColumn(0, 'Number')
        self.lc.InsertColumn(1, 'Name')

        vbox1.Add(self.lc, 1, wx.EXPAND| wx.ALL, 3)
        vbox2.Add(pnl1, 1, wx.EXPAND | wx.ALL, 3)
        
        self.tc1 = wx.TextCtrl(pnl1, -1, style=wx.EXPAND)
        self.tc2 = wx.TextCtrl(pnl1, -1, style=wx.TE_MULTILINE | wx.EXPAND, size=(200,300))
        
        vbox3.AddMany([ (wx.StaticText(pnl1, -1, 'Name'), 0, wx.ALIGN_LEFT),
                        (self.tc1, 0, wx.ALIGN_LEFT | wx.ALIGN_CENTER_VERTICAL),
                        (wx.StaticText(pnl1, -1, 'Notes'), 0, wx.ALIGN_LEFT),
                        (self.tc2, 0)])
                        
        pnl1.SetSizer(vbox3)
        
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnSelect, self.lc)
        
        
        hbox.Add(vbox1, 1, wx.EXPAND)
        hbox.Add(vbox2, 1, wx.EXPAND)
        self.populateList(dataset)
        self.SetSizer(hbox)
        self.Show(True)
        
    def getDataSet(self):
        data = DataStore()
        dataset = {}
        index = 1
        for category in list(BJCPCategory.select()):
            dataset[index] = ("%i" % category.category_id, category.name)
            index = index + 1
        
        return dataset
        
    def populateList(self, dataset):
        items = dataset.items()
        for key, data in items:
            index = self.lc.InsertStringItem(sys.maxint, data[0])
            self.lc.SetStringItem(index, 1, data[1])
            self.lc.SetItemData(index, key)
        
    def OnSelect(self, event):
        category_id = event.GetItem().GetData()
        cat = BJCPCategory.select(BJCPCategory.q.category_id==category_id)[0]
        self.tc1.ChangeValue(cat.name)
        if cat.notes:
            self.tc2.ChangeValue(cat.notes)
        else:
            self.tc2.ChangeValue("")
        
app = wx.PySimpleApp()
frame = MainWindow(None, -1, 'BJCP Editor')
app.MainLoop()