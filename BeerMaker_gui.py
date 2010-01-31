#!/usr/bin/env python
# -*- coding: utf-8 -*-
# generated by wxGlade 0.6.3 on Mon Jan 18 22:13:01 2010

# Copyright (C) 2010 Todd Kennedy <todd.kennedy@gmail.com>
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import os

import wx

# begin wxGlade: extracode
# end wxGlade

icon = os.path.abspath('img/icon.gif')

class MainFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MainFrame.__init__
        kwds["style"] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        
        # Menu Bar
        self.BeerMakerMenu = wx.MenuBar()
        wxglade_tmp_menu = wx.Menu()
        wxglade_tmp_menu.Append(101, "Quit", "Terminate the program", wx.ITEM_NORMAL)
        self.BeerMakerMenu.Append(wxglade_tmp_menu, "File")
        self.SetMenuBar(self.BeerMakerMenu)
        # Menu Bar end
        self.BeerMakerStatus = self.CreateStatusBar(1, 0)
        
        # Tool Bar
        self.BeerMakerToolbars = wx.ToolBar(self, -1, style=wx.TB_HORIZONTAL|wx.TB_TEXT)
        self.SetToolBar(self.BeerMakerToolbars)
        self.BeerMakerToolbars.AddLabelTool(200, "New Recipe", wx.Bitmap(icon,wx.BITMAP_TYPE_ANY), wx.Bitmap(icon,wx.BITMAP_TYPE_ANY), wx.ITEM_NORMAL, "New Recipe", "Create a new recipe")
        self.BeerMakerToolbars.AddLabelTool(201, "New Batch", wx.Bitmap(icon,wx.BITMAP_TYPE_ANY), wx.Bitmap(icon,wx.BITMAP_TYPE_ANY), wx.ITEM_NORMAL, "New Batch", "Create a new batch of an existing recipe")
        self.BeerMakerToolbars.AddLabelTool(202, "Edit Recipe/Batch", wx.Bitmap(icon,wx.BITMAP_TYPE_ANY), wx.Bitmap(icon,wx.BITMAP_TYPE_ANY), wx.ITEM_NORMAL, "Edit current item", "Edit the current recipe or batch")
        # Tool Bar end
        self.RecipeList = wx.ListCtrl(self, -1, style=wx.LC_REPORT|wx.LC_SINGLE_SEL|wx.LC_SORT_ASCENDING|wx.SUNKEN_BORDER)

        self.__set_properties()
        self.__do_layout()

        self.Bind(wx.EVT_MENU, self.OnQuit, id=101)
        self.Bind(wx.EVT_TOOL, self.launchRecipeEditor, id=200)
        self.Bind(wx.EVT_TOOL, self.createBatchFromRecipe, id=201)
        self.Bind(wx.EVT_LIST_ITEM_ACTIVATED, self.showRecipeEditor, self.RecipeList)
        self.Bind(wx.EVT_LIST_ITEM_RIGHT_CLICK, self.showContextMenu, self.RecipeList)
        # end wxGlade
        
        self.populateList()

    def __set_properties(self):
        # begin wxGlade: MainFrame.__set_properties
        self.SetTitle("BeerMaker")
        self.SetSize((1024, 768))
        self.BeerMakerStatus.SetStatusWidths([-1])
        # statusbar fields
        BeerMakerStatus_fields = [""]
        for i in range(len(BeerMakerStatus_fields)):
            self.BeerMakerStatus.SetStatusText(BeerMakerStatus_fields[i], i)
        self.BeerMakerToolbars.Realize()
        # end wxGlade

    def __do_layout(self):
        # begin wxGlade: MainFrame.__do_layout
        sizer_1 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(self.RecipeList, 1, wx.EXPAND, 0)
        self.SetSizer(sizer_1)
        self.Layout()
        # end wxGlade

    def populateList(self):
        self.RecipeList.InsertColumn(0, 'Name')
        self.RecipeList.InsertColumn(1, 'Style')
        self.RecipeList.InsertColumn(2, 'IBU')
        self.RecipeList.InsertColumn(3, 'ABV')
        self.RecipeList.InsertColumn(4, 'OG')
        self.RecipeList.InsertColumn(6, 'FG')
        self.RecipeList.InsertColumn(7, 'Brewed On')
        for column in range(0,self.RecipeList.GetColumnCount()):
            self.RecipeList.SetColumnWidth(column, 100)
            
        
    

    def OnQuit(self, event): # wxGlade: MainFrame.<event_handler>
        self.Close(True)

    def launchRecipeEditor(self, event): # wxGlade: MainFrame.<event_handler>
        print "Event handler `launchRecipeEditor' not implemented!"
        event.Skip()

    def createBatchFromRecipe(self, event): # wxGlade: MainFrame.<event_handler>
        print "Event handler `createBatchFromRecipe' not implemented!"
        event.Skip()

    def showRecipeEditor(self, event): # wxGlade: MainFrame.<event_handler>
        print "Event handler `showRecipeEditor' not implemented"
        event.Skip()

    def showContextMenu(self, event): # wxGlade: MainFrame.<event_handler>
        print "Event handler `showContextMenu' not implemented"
        event.Skip()

# end of class MainFrame


class BeerMaker(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        frame_1 = MainFrame(None, -1, "")
        self.SetTopWindow(frame_1)
        frame_1.Show()
        return 1

# end of class BeerMaker

if __name__ == "__main__":
    BeerMaker = BeerMaker(0)
    BeerMaker.MainLoop()
