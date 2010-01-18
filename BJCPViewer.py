#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Sun Jan 17 19:25:55 2010
import sys

import wx
from wx.lib.mixins.listctrl import ListCtrlAutoWidthMixin

from models import BJCPCategory, BJCPStyle
from db import DataStore

# begin wxGlade: extracode
# end wxGlade



class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.BJCP_Style_ctrl = wx.ListCtrl(self, -1, style=wx.LC_REPORT|wx.LC_SINGLE_SEL|wx.SUNKEN_BORDER)
        self.BJCP_Name_txt = wx.StaticText(self, -1, "Name:", style=wx.ALIGN_RIGHT)
        self.BJCP_Name_ctrl = wx.TextCtrl(self, -1, "", style=wx.TE_READONLY)
        self.BJCP_Category_txt = wx.StaticText(self, -1, "Category:", style=wx.ALIGN_RIGHT)
        self.BJCP_Category_ctrl = wx.TextCtrl(self, -1, "", style=wx.TE_READONLY)
        self.BJCP_Type_txt = wx.StaticText(self, -1, "Type:", style=wx.ALIGN_RIGHT)
        self.BJCP_Type_ctrl = wx.TextCtrl(self, -1, "", style=wx.TE_READONLY)
        self.BJCP_Aroma_txt = wx.StaticText(self, -1, "Aroma")
        self.BJCP_Aroma_ctrl = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.BJCP_Appearance_txt = wx.StaticText(self, -1, "Appearance")
        self.BJCP_Appearance_ctrl = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.BJCP_Flavor_txt = wx.StaticText(self, -1, "Flavor")
        self.BJCP_Flavor_ctrl = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.BJCP_Mouthfeel_txt = wx.StaticText(self, -1, "Mouthfeel")
        self.BJCP_Mouthfeel_ctrl = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.BJCP_Impression_txt = wx.StaticText(self, -1, "Impression")
        self.BJCP_Impression_ctrl = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.BJCP_Examples_txt = wx.StaticText(self, -1, "Examples")
        self.BJCP_Examples_ctrl = wx.TextCtrl(self, -1, "", style=wx.TE_MULTILINE|wx.TE_READONLY)
        self.BJCP_IBUs_txt = wx.StaticText(self, -1, "IBUs:", style=wx.ALIGN_RIGHT)
        self.BJCP_IBUs_ctrl = wx.TextCtrl(self, -1, "", style=wx.TE_READONLY)
        self.BJCP_SRM_txt = wx.StaticText(self, -1, "SRM:", style=wx.ALIGN_RIGHT)
        self.BJCP_SRM_ctrl = wx.TextCtrl(self, -1, "", style=wx.TE_READONLY)
        self.BJCP_ABV_txt = wx.StaticText(self, -1, "ABV:", style=wx.ALIGN_RIGHT)
        self.BJCP_ABV_ctrl = wx.TextCtrl(self, -1, "", style=wx.TE_READONLY)
        self.BJCP_OG_txt = wx.StaticText(self, -1, "OG:", style=wx.ALIGN_RIGHT)
        self.BJCP_OG_ctrl = wx.TextCtrl(self, -1, "", style=wx.TE_READONLY)
        self.BJCP_FG_txt = wx.StaticText(self, -1, "FG:", style=wx.ALIGN_RIGHT)
        self.BJCP_FG_ctrl = wx.TextCtrl(self, -1, "", style=wx.TE_READONLY)
        
        # Menu Bar
        self.BJCP_Category_ctrl_menubar = wx.MenuBar()
        wxglade_tmp_menu = wx.Menu()
        wxglade_tmp_menu.Append(101, "Quit", "Quit the Viewer", wx.ITEM_NORMAL)
        self.BJCP_Category_ctrl_menubar.Append(wxglade_tmp_menu, "File")
        self.SetMenuBar(self.BJCP_Category_ctrl_menubar)
        # Menu Bar end
        self.BJCP_Category_ctrl_statusbar = self.CreateStatusBar(1, 0)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.OnStyleSelect, self.BJCP_Style_ctrl)
        self.Bind(wx.EVT_MENU, self.OnQuit, id=101)
        # end wxGlade
        
        self.getBJCPData()
        self.populateList()
        self.resizeColumns()

    def __set_properties(self):
        # begin wxGlade: MyFrame.__set_properties
        self.SetTitle("BJCP Style Viewer")
        self.SetSize((1106, 860))
        self.BJCP_Category_ctrl_statusbar.SetStatusWidths([-1])
        # statusbar fields
        BJCP_Category_ctrl_statusbar_fields = ["BJCP_Category_ctrl_statusbar"]
        for i in range(len(BJCP_Category_ctrl_statusbar_fields)):
            self.BJCP_Category_ctrl_statusbar.SetStatusText(BJCP_Category_ctrl_statusbar_fields[i], i)
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MyFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_8 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_4 = wx.BoxSizer(wx.HORIZONTAL)
        grid_sizer_2 = wx.GridSizer(3, 1, 0, 0)
        sizer_5_copy_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_5_copy_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_5_copy = wx.BoxSizer(wx.VERTICAL)
        grid_sizer_1 = wx.GridSizer(3, 1, 0, 0)
        sizer_7 = wx.BoxSizer(wx.VERTICAL)
        sizer_6 = wx.BoxSizer(wx.VERTICAL)
        sizer_5 = wx.BoxSizer(wx.VERTICAL)
        sizer_3 = wx.BoxSizer(wx.HORIZONTAL)
        sizer_1.Add(self.BJCP_Style_ctrl, 1, wx.ALL|wx.EXPAND, 5)
        sizer_3.Add(self.BJCP_Name_txt, 0, wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_3.Add(self.BJCP_Name_ctrl, 1, wx.ALL, 1)
        sizer_3.Add(self.BJCP_Category_txt, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_3.Add(self.BJCP_Category_ctrl, 1, wx.ALL, 1)
        sizer_3.Add(self.BJCP_Type_txt, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 5)
        sizer_3.Add(self.BJCP_Type_ctrl, 1, wx.ALL, 1)
        sizer_2.Add(sizer_3, 0, wx.EXPAND, 0)
        sizer_5.Add(self.BJCP_Aroma_txt, 0, wx.ALL, 5)
        sizer_5.Add(self.BJCP_Aroma_ctrl, 1, wx.ALL|wx.EXPAND, 5)
        grid_sizer_1.Add(sizer_5, 1, wx.EXPAND, 0)
        sizer_6.Add(self.BJCP_Appearance_txt, 0, wx.ALL, 5)
        sizer_6.Add(self.BJCP_Appearance_ctrl, 1, wx.ALL|wx.EXPAND, 5)
        grid_sizer_1.Add(sizer_6, 1, wx.EXPAND, 0)
        sizer_7.Add(self.BJCP_Flavor_txt, 0, wx.ALL, 5)
        sizer_7.Add(self.BJCP_Flavor_ctrl, 1, wx.ALL|wx.EXPAND, 5)
        grid_sizer_1.Add(sizer_7, 1, wx.EXPAND, 0)
        sizer_4.Add(grid_sizer_1, 1, wx.EXPAND, 0)
        sizer_5_copy.Add(self.BJCP_Mouthfeel_txt, 0, wx.ALL, 5)
        sizer_5_copy.Add(self.BJCP_Mouthfeel_ctrl, 1, wx.ALL|wx.EXPAND, 5)
        grid_sizer_2.Add(sizer_5_copy, 1, wx.EXPAND, 0)
        sizer_5_copy_1.Add(self.BJCP_Impression_txt, 0, wx.ALL, 5)
        sizer_5_copy_1.Add(self.BJCP_Impression_ctrl, 1, wx.ALL|wx.EXPAND, 5)
        grid_sizer_2.Add(sizer_5_copy_1, 1, wx.EXPAND, 0)
        sizer_5_copy_2.Add(self.BJCP_Examples_txt, 0, wx.ALL, 5)
        sizer_5_copy_2.Add(self.BJCP_Examples_ctrl, 1, wx.ALL|wx.EXPAND, 5)
        grid_sizer_2.Add(sizer_5_copy_2, 1, wx.EXPAND, 0)
        sizer_4.Add(grid_sizer_2, 1, wx.EXPAND, 0)
        sizer_2.Add(sizer_4, 1, wx.EXPAND, 0)
        sizer_8.Add(self.BJCP_IBUs_txt, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_8.Add(self.BJCP_IBUs_ctrl, 1, wx.ALL|wx.EXPAND, 1)
        sizer_8.Add(self.BJCP_SRM_txt, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_8.Add(self.BJCP_SRM_ctrl, 1, wx.ALL|wx.EXPAND, 1)
        sizer_8.Add(self.BJCP_ABV_txt, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_8.Add(self.BJCP_ABV_ctrl, 1, wx.ALL|wx.EXPAND, 1)
        sizer_8.Add(self.BJCP_OG_txt, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_8.Add(self.BJCP_OG_ctrl, 1, wx.ALL|wx.EXPAND, 1)
        sizer_8.Add(self.BJCP_FG_txt, 0, wx.ALL|wx.ALIGN_CENTER_HORIZONTAL|wx.ALIGN_CENTER_VERTICAL, 0)
        sizer_8.Add(self.BJCP_FG_ctrl, 1, wx.ALL|wx.EXPAND, 1)
        sizer_2.Add(sizer_8, 0, wx.EXPAND, 0)
        sizer_1.Add(sizer_2, 2, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade

    def OnQuit(self):
        self.Close(True)

    def getBJCPData(self):
        data = DataStore()
        self.bjcp_styles = list(BJCPStyle.select())
        
    def populateList(self):
        self.BJCP_Style_ctrl.InsertColumn(0, 'Name')
        self.BJCP_Style_ctrl.InsertColumn(1, 'Category')
        self.BJCP_Style_ctrl.InsertColumn(2, 'Type')
        self.BJCP_Style_ctrl.InsertColumn(3, 'IBU')
        self.BJCP_Style_ctrl.InsertColumn(4, 'SRM')
        self.BJCP_Style_ctrl.InsertColumn(5, 'ABV')
        self.BJCP_Style_ctrl.InsertColumn(6, 'OG')
        self.BJCP_Style_ctrl.InsertColumn(7, 'FG')
        
        for style in self.bjcp_styles:
            index = self.BJCP_Style_ctrl.InsertStringItem(sys.maxint, style.name)
            cat = "%i%s: %s" % (style.category.category_id, style.subcategory, style.category.name)
            self.BJCP_Style_ctrl.SetStringItem(index, 1, cat)
            self.BJCP_Style_ctrl.SetStringItem(index, 2, style.beer_type.capitalize())
            ibus = "%i- %i" % (style.ibu_low, style.ibu_high)
            self.BJCP_Style_ctrl.SetStringItem(index, 3, ibus)
            srm = "%.1f - %.1f" % (style.srm_low, style.srm_high)
            self.BJCP_Style_ctrl.SetStringItem(index, 4, srm)
            abv = "%.1f - %.1f" % (style.abv_low, style.abv_high)
            self.BJCP_Style_ctrl.SetStringItem(index, 5, abv)
            og = "%.3f - %.3f" % (style.og_low, style.og_high)
            self.BJCP_Style_ctrl.SetStringItem(index, 6, og)
            fg = "%.3f - %.3f" % (style.fg_low, style.fg_high)
            self.BJCP_Style_ctrl.SetStringItem(index, 7, fg)
            

    def resizeColumns(self):
        #print self.BJCP_Style_ctrl.GetColumnCount()
        for column in range(0,self.BJCP_Style_ctrl.GetColumnCount()):
            self.BJCP_Style_ctrl.SetColumnWidth(column, wx.LIST_AUTOSIZE)

    def OnStyleSelect(self, event): # wxGlade: MyFrame.<event_handler>
        selected = self.BJCP_Style_ctrl.GetItem(event.Index,0).GetText()
        style = BJCPStyle.select(BJCPStyle.q.name==selected)[0]
        self.BJCP_Name_ctrl.ChangeValue(style.name)
        category = "%i%s: %s" % (style.category.category_id, style.subcategory, style.category.name)
        self.BJCP_Category_ctrl.ChangeValue(category)
        self.BJCP_Type_ctrl.ChangeValue(style.beer_type.capitalize())
        self.BJCP_Aroma_ctrl.ChangeValue(style.aroma)
        self.BJCP_Mouthfeel_ctrl.ChangeValue(style.mouthfeel)
        self.BJCP_Appearance_ctrl.ChangeValue(style.appearance)
        self.BJCP_Examples_ctrl.ChangeValue(style.examples)
        self.BJCP_Impression_ctrl.ChangeValue(style.impression)
        self.BJCP_Flavor_ctrl.ChangeValue(style.flavor)
        ibus = "%i- %i" % (style.ibu_low, style.ibu_high)
        srm = "%.1f - %.1f" % (style.srm_low, style.srm_high)
        abv = "%.1f - %.1f" % (style.abv_low, style.abv_high)
        og = "%.3f - %.3f" % (style.og_low, style.og_high)
        fg = "%.3f - %.3f" % (style.fg_low, style.fg_high)
        self.BJCP_IBUs_ctrl.ChangeValue(ibus)
        self.BJCP_SRM_ctrl.ChangeValue(srm)
        self.BJCP_ABV_ctrl.ChangeValue(abv)
        self.BJCP_OG_ctrl.ChangeValue(og)
        self.BJCP_FG_ctrl.ChangeValue(fg)
        

    def OnQuit(self, event): # wxGlade: MyFrame.<event_handler>
        print "Event handler `OnQuit' not implemented"
        event.Skip()

# end of class MyFrame


if __name__ == "__main__":
    app = wx.PySimpleApp(0)
    wx.InitAllImageHandlers()
    frame_1 = MyFrame(None, -1, "")
    app.SetTopWindow(frame_1)
    frame_1.Show()
    app.MainLoop()
