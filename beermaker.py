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

from db import DataStore
from models import Recipe, Batch

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
        for menu in self.menuData():
            label = menu['name']
            items = menu['items']
            menu_bar.Append(self.createMenu(items), label)
        self.SetMenuBar(menu_bar)
    
    def createMenu(self, items):
        menu = wx.Menu()
        for item in items:
            if item.has_key('items'):
                menu_id = wx.NewId()
                label = item['name']
                sub_menu = self.createMenu(item['items'])
                menu.AppendMenu(menu_id, label, sub_menu)
            else:
                self.createMenuItem(menu, item['id'], item['name'], item['help'], item['method'])
        return menu
        
    def createMenuItem(self, menu, menu_id, name, help, method, kind=wx.ITEM_NORMAL):
        if menu_id == 'separator':
            menu.AppendSeparator()
            return
        menu_item = menu.Append(menu_id, name, help, kind)
        self.Bind(wx.EVT_MENU, method, menu_item)
        
            
    def menuData(self):
        file_menu = {'name': "&File",
        'items': 
            ({'name': '&New',
            'items': 
                ({'name': "New &Recipe",
                'id': guid.MENU_NEW_RECIPE,
                'help': 'Create a new recipe',
                'method': self.newRecipe},
    
                {'name': "New &Batch",
                'id': guid.MENU_NEW_BATCH,
                'help': 'Create a new batch of the current recipe or batch',
                'method': self.newBatch})            
            },

            {'name': 'separator',
            'id': 'separator',
            'help': 'separator',
            'method': 'separator'},    

            {'name': "&Print Current",
            'id': guid.MENU_PRINT,
            'help': 'Print currently selected recipe or batch',
            'method': self.printItem},

            {'name': "&Quit BeerMaker",
            'help': 'Terminate BeerMaker',
            'id': guid.MENU_QUIT,
            'method': self.quitApplication},)}

        edit_menu = {'name': '&Edit',
        'items':
            ({'name': '&Preferences',
            'help': 'Edit Preferences',
            'id': guid.MENU_PREFERENCES,
            'method': self.viewPreferences},)}

        view_menu = {'name': '&View',
        'items':
            ({'name': '&Inventory',
            'id': guid.MENU_INVENTORY_EDITOR,
            'help': 'Manage the inventory of items you have on hand',
            'method': self.viewInventory},

            {'name': '&Mashes',
            'id': guid.MENU_MASH_EDITOR,
            'help': 'Manage your mash profiles',
            'method': self.viewMashes},

            {'name': '&Equipment',
            'id': guid.MENU_EQUIPMENT_EDITOR,
            'help': 'Manage your equipment profiles',
            'method': self.viewEquipment},

            {'name': '&Ingredients',
            'id': guid.MENU_INGREDIENT_EDTIOR,
            'help': 'Manage the ingredient database',
            'method': self.viewIngredients},

            {'name': 'separator',
            'id': 'separator',
            'help': 'separator',
            'method': 'separator'},    

            {'name': '&Calculators',
            'id': guid.MENU_CALCULATORS,
            'help': 'View all the calculators',
            'method': self.viewCalculators},)}

        menu = (file_menu, edit_menu, view_menu)

        return menu    

    def toolbarData(self):
         return (
             (guid.TB_NEW_RECIPE, iconsrc.tb_new_recipe, "New Recipe", "Create a new recipe", self.newRecipe),
             (guid.TB_NEW_BATCH, iconsrc.tb_new_batch, "New Batch", "Create a new batch of the current recipe or batch", self.newBatch),
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
        self.menus = self.buildMenuBar()
        
        # make some toolbars
        self.tools = self.buildToolbar()
        
        
        # start the layout
        self.SetTitle("BeerMaker")
        self.SetSize((1024, 768))       
        self.panel = wx.Panel(self,-1)

        # generate the list control
        self.recipe_list = wx.ListCtrl(self.panel, -1, style=wx.LC_REPORT|wx.SUNKEN_BORDER)

        # set the sizers
        self.main_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.main_sizer.Add(self.recipe_list, 1, wx.ALL|wx.EXPAND, 3)
        self.panel.SetSizer(self.main_sizer)
        
        # load data
        self.populateList()
    
    def populateList(self):
        self.recipe_list.InsertColumn(guid.RL_NAME, 'Name')
        self.recipe_list.InsertColumn(guid.RL_CATEGORY, 'Category')
        self.recipe_list.InsertColumn(guid.RL_NUMBER, 'Number')
        self.recipe_list.InsertColumn(guid.RL_IBU, 'IBU')
        self.recipe_list.InsertColumn(guid.RL_SRM, 'SRM')
        self.recipe_list.InsertColumn(guid.RL_ABV, 'ABV')
        self.recipe_list.InsertColumn(guid.RL_OG, 'OG')
        self.recipe_list.InsertColumn(guid.RL_FG, 'FG')
        self.recipe_list.InsertColumn(guid.RL_BREWED_ON, 'Brewed On')
        
        for batch in list(Batch.select(distinct=True)):
            recipe = Recipe.get(batch.master_id)
            index = self.recipe_list.InsertStringItem(wx.NewId(), recipe.name)
            self.recipe_list.SetStringItem(index, guid.RL_CATEGORY, recipe.style.name)
            self.recipe_list.SetStringItem(index, guid.RL_NUMBER, recipe.style.combined_category_id)
            self.recipe_list.SetStringItem(index, guid.RL_IBU, recipe.ibu)
            self.recipe_list.SetStringItem(index, guid.RL.SRM, recipe.srm)
            self.recipe_list.SetStringItem(index, guid.RL_ABV, recipe.abv)
            self.recipe_list.SetStringItem(index, guid.RL_OG, recipe.og)
            self.recipe_list.SetStringItem(index, guid.RL_FG, recipe.fg)
            self.recipe_list.SetStringItem(index, guid.RL_BREWED_ON, recipe.brewed_on)        
        
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
        ds = DataStore()
        BeerMaker = MainFrame(None, -1, "")
        self.SetTopWindow(BeerMaker)
        BeerMaker.Show()
        return 1

# end of class BeerMaker

if __name__ == "__main__":
    BeerMaker = BeerMaker(0)
    BeerMaker.MainLoop()