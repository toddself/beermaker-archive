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

import guid

class BaseWindow():
    def __init__(self):
        pass
        
    def buildToolBar(self):
        toolbar = self.CreateToolBar()
        for button in self.toolbarData():
            toolbar.createTool(toolbar, *button)
        toolbar.Realize()
        
    def createTool(self, toolbar, tb_id, fn_icon, label, help, handler):
        if not tb_id:
            toolbar.AddSeparator()
            return
        else:
            tool = toolbar.AddSimpleTool(tb_id, fn_icon, label, help)
            self.Bind(wx.EVT_MENU, handler, tool)
    
    def buildMenuBar(self):
        menu_bar = wx.MenuBar()
        for menu_item in self.menuData():
            label = menu_item[0]
            items = menu_item[1]
            menu_bar.Append(self.createMenu(items), label)
        self.SetMenuBar(menu_bar)
    
    def createMenu(self, data):
        menu = wx.Menu
        for item in data:
            if len(item) == 2:
                label = item[0]
                sub_menu = self.createMenu(item[1])
                menu.AppendMenu(wx.NewId(), label, sub_menu)
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
        return [("&File",
                    ("&New",
                        (MENU_NEW_RECIPE, "New &Recipe", "Create a new recipe", self.newRecipe),
                        (MENU_NEW_BATCH, "New &Batch", "Create a new batch of the current recipe or batch", self.newBatch),
                    ),
                    ("","","",""),
                    (MENU_PRINT, "&Print Current", "Print currently selected recipe or batch", self.printItem),
                    (MENU_QUIT, "&Quit BeerMaker", "Quit the application", self.quitApplication),
                ),
                ("&Edit",
                    (MENU_PREFERENCES, "&Preferences", "Edit your preferences", self.viewPreferences),
                )
                ("&View",
                    (MENU_INVENTORY_EDITOR, "&Inventory", "Manage the amount of what you have on hand", self.viewInventory),
                    (MENU_MASH_EDITOR, "&Mashes", "Manage your mash profiles", self.viewMashes),
                    (MENU_EQUPIMENT_EDITOR, "&Equipment", "Manage your equipment profiles", self.viewEquipment),
                    (MENU_INGREDIENT_EDTIOR, "&Ingredients", "Manage the ingredient database", self.viewIngredients),
                    ("","","",""),
                    (MENU_CALCULATORS, "&Calculators", "View all the calculators", self.viewCalculators),
                )
                
        )]
            
    def toolbarData(self):
        return (
            (TB_NEW_RECIPE, tb_new_recipe, "New Recipe", "Create a new recipe", self.newRecipe),
            (TB_NEW_BATCH, tb_new_batch, "New Recipe", "Create a new batch of the current recipe or batch", self.newBatch),
            ("","","",""),
            (TB_INVENTORY_EDITOR, tb_inventory_editor, "Inventory Editor", "Manage the amount of what you have on hand". self.viewInventory),
            ("","","",""),
            (TB_MASH_EDITOR, tb_mash_editor, "Mash Editor", "Manage your mash profiles", self.viewMashes),
            ("","","",""),
            (TB_EQUPIMENT_EDITOR, tb_equipment_editor, "Equipment Editor", "Manage your equipment profiles", self.viewEquipment),
            ("","","",""),
            (TB_INGREDIENT_EDITOR, tb_ingredient_editor, "Ingredient Editor", "Manage the ingredient database", self.viewIngredients),
            ("","","",""),
            (TB_CALCULATORS, tb_calculators, "Calculators", "View all the calculators", self.viewCalculators),
            ("","","",""),
            (TB_PREFERENCES, tb_preferences, "Preferences", "View your preferences", self.viewPreferences),

        )