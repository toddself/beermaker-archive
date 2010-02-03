#!/usr/bin/env python

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

import wx

# we're importing these for now so we have better separation of data and ui elements
# these will eventually move into a skinning system
import guid
import iconsrc

class BaseWindow():
    def __init__(self):
        pass
        
    def buildToolbar(self):
        toolbar = wx.ToolBar(self, -1, style=wx.TB_TEXT)
        self.SetToolBar(toolbar)
        for button in self.toolbarData():
            self.createTool(toolbar, *button)
        toolbar.Realize()
        
    def createTool(self, toolbar, tb_id, fn_icon, label, help, handler):
        if not tb_id:
            toolbar.AddSeparator()
            return
        else:
            icon = wx.Bitmap(fn_icon, wx.BITMAP_TYPE_ANY)
            tool = toolbar.AddLabelTool(tb_id, label, icon, icon, wx.ITEM_NORMAL, label, help)
            self.Bind(wx.EVT_MENU, handler, tool)
    
    def buildMenuBar(self):
        menu_bar = wx.MenuBar()
        for menu_item in self.menuData():
            label = menu_item[1]
            items = menu_item[2]
            menu_bar.Append(self.createMenu(items), label)
        self.SetMenuBar(menu_bar)
    
    def createMenu(self, data):
        menu = wx.Menu()
        for item in data:
            if type(item) == type(()):
                menu_id = item[0]
                label = item[1]
                sub_menu = self.createMenu(item[2])
                menu.AppendMenu(menu_id, label, sub_menu)
            else:
                self.createMenuItem(menu, *item)
        return menu
        
    def createMenuItem(self, menu, menu_id, label, status, handler, kind=wx.ITEM_NORMAL):
        if not menu_id:
            menu.AppendSeperator()
            return
        menu_item = menu.Append(menu_id, label, status, kind)
        self.Bind(wx.EVT_MENU, handler, menu_item)
        
            
    def menuData(self):
        return [(guid.MENU_FILE, "&File",
                (
                    guid.MENU_NEW, "&New",
                        (
                            (guid.MENU_NEW_RECIPE, "New &Recipe", "Create a new recipe", self.newRecipe),
                            (guid.MENU_NEW_BATCH, "New &Batch", "Create a new batch of the current recipe or batch", self.newBatch)
                        ),
                    ("","","",""),
                    (guid.MENU_PRINT, "&Print Current", "Print currently selected recipe or batch", self.printItem),
                    (guid.MENU_QUIT, "&Quit BeerMaker", "Quit the application", self.quitApplication),
                ),
                (guid.MENU_EDIT, "&Edit",
                    (guid.MENU_PREFERENCES, "&Preferences", "Edit your preferences", self.viewPreferences),
                ),
                (guid.MENU_VIEW, "&View",
                    (guid.MENU_INVENTORY_EDITOR, "&Inventory", "Manage the amount of what you have on hand", self.viewInventory),
                    (guid.MENU_MASH_EDITOR, "&Mashes", "Manage your mash profiles", self.viewMashes),
                    (guid.MENU_EQUPIMENT_EDITOR, "&Equipment", "Manage your equipment profiles", self.viewEquipment),
                    (guid.MENU_INGREDIENT_EDTIOR, "&Ingredients", "Manage the ingredient database", self.viewIngredients),
                    ("","","",""),
                    (guid.MENU_CALCULATORS, "&Calculators", "View all the calculators", self.viewCalculators),
                ))]
            
    def toolbarData(self):
        return (
            (guid.TB_NEW_RECIPE, iconsrc.tb_new_recipe, "New Recipe", "Create a new recipe", self.newRecipe),
            (guid.TB_NEW_BATCH, iconsrc.tb_new_batch, "New Recipe", "Create a new batch of the current recipe or batch", self.newBatch),
            ("","","","",""),
            (guid.TB_INVENTORY_EDITOR, iconsrc.tb_inventory_editor, "Inventory Editor", "Manage the amount of what you have on hand", self.viewInventory),
            ("","","","",""),
            (guid.TB_MASH_EDITOR, iconsrc.tb_mash_editor, "Mash Editor", "Manage your mash profiles", self.viewMashes),
            ("","","","",""),
            (guid.TB_EQUPIMENT_EDITOR, iconsrc.tb_equipment_editor, "Equipment Editor", "Manage your equipment profiles", self.viewEquipment),
            ("","","","",""),
            (guid.TB_INGREDIENT_EDITOR, iconsrc.tb_ingredient_editor, "Ingredient Editor", "Manage the ingredient database", self.viewIngredients),
            ("","","","",""),
            (guid.TB_CALCULATORS, iconsrc.tb_calculators, "Calculators", "View all the calculators", self.viewCalculators),
            ("","","","",""),
            (guid.TB_PREFERENCES, iconsrc.tb_preferences, "Preferences", "View your preferences", self.viewPreferences),

        )

class MainFrame(wx.Frame, BaseWindow):
    def __init__(self, *args, **kw):
        kw['style'] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kw)
        
        # make a status bar
        self.status_bar = self.CreateStatusBar(1,0)
        
        # make some menus
        # self.menus = self.buildMenuBar()
        
        # make some toolbars
        self.tools = self.buildToolbar()
        
        self.SetTitle("BeerMaker")
        self.SetSize((1024, 768))       
        
    def newRecipe(self):
        pass
    
    def newBatch(self):
        pass
        
    def viewInventory(self):
        """docstring for viewIventory"""
        pass
        
    def viewMashes(self):
        """docstring for viewMashes"""
        pass 
    
    def viewEquipment(self):
        """docstring for viewEquipment"""
        pass

    def viewIngredients(self):
        """docstring for viewIngredients"""
        pass

    def viewCalculators(self):
        """docstring for viewCalculators"""
        pass
        
    def viewPreferences(self):
        """docstring for viewPreferences"""
        pass
        
    def printItem(self):
        """docstring for printItem"""
        pass
    
    def quitApplication(self):
        """docstring for quitApplication"""
        pass

class BeerMaker(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        BeerMaker = MainFrame(None, -1, "")
        self.SetTopWindow(BeerMaker)
        BeerMaker.Show()
        return 1

# end of class BeerMaker

if __name__ == "__main__":
    BeerMaker = BeerMaker(0)
    BeerMaker.MainLoop()