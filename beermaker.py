#!/usr/bin/env python

# BeerMaker - beer recipe creation and inventory management software
# Copyright (C) 2010 Todd Kennedy <todd.kennedy@gmail.com>
# 
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import wx
from ObjectListView import ObjectListView, ColumnDefn

# we're importing these for now so we have better separation of data and ui elements
# these will eventually move into a skinning system
import guid
import iconsrc

# import data objects
from db import DataStore
from models import Recipe

# import gui elements
from base import BaseWindow
from recipe_editor import RecipeEditor

class RecipeData():
    def __init__(self, name, category, number, ibu, srm, abv, og, fg, brewed_on):
        self.name = name
        self.category = category
        self.number = number
        self.ibu = ibu
        self.srm = srm
        self.abv = abv
        self.og = og
        self.fg = fg
        self.brewed_on = brewed_on
        
class MainFrame(wx.Frame, BaseWindow):
    def __init__(self, *args, **kw):
        kw['style'] = wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kw)
        
        # ui basics...
        self.status_bar = self.CreateStatusBar(1,0)
        self.menus = self.buildMenuBar()
        self.tools = self.buildToolbar()
        
        # new layout engine
        self.main_panel = wx.Panel(self, -1)
        self.main_panel.SetSizer(self.buildLayout(self.main_panel))
        
        self._setupRecipeList()


    def layoutData(self):
        return ({'widget': wx.BoxSizer, 'style:': wx.VERTICAL, 'proportion': 1, 'flag': wx.EXPAND|wx.ALL, 'border': 3, 'widgets':
            ({'widget': ObjectListView, 'var': 'recipes_ctrl', 'style': wx.LC_REPORT, 'cellEditMode': ObjectListView.CELLEDIT_DOUBLECLICK, 'flag': wx.EXPAND|wx.ALL, 'proportion': 1},)
        },)

    def _setupRecipeList(self):
        namec = ColumnDefn('Name', 'left', -1, 'name', isSpaceFilling=True)
        catc = ColumnDefn('Category', 'left', 80, 'start_temp')
        numberc = ColumnDefn('Number', 'left', 80, 'end_temp')
        ibuc = ColumnDefn('IBU', 'left', 80, 'time')
        srmc = ColumnDefn('SRM', 'left', 80, 'time')
        abvc = ColumnDefn('ABV', 'left', 80, 'time')
        ogc = ColumnDefn('OG', 'left', 80, 'time')
        fgc = ColumnDefn('FG', 'left', 80, 'time')
        boc = ColumnDefn('Brewed On', 'left', 80, 'time')


        self.recipes_ctrl.SetColumns([namec, catc, numberc, ibuc, srmc, abvc, ogc, fgc, boc])
        
    def newRecipe(self, event):
        recipe_editor = RecipeEditor(self, -1, "", size=(1024,768), pos=(10,50))
        recipe_editor.Show()
    
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
    
    def visitWebsite(self):
        """docstring for visitWebsite"""
        pass
        
    def undo(self):
        """docstring for undo"""
        pass

    def redo(self):
        """docstring for redo"""
        pass

    def copy(self):
        """docstring for copy"""
        pass

    def paste(self):
        """docstring for paste"""
        pass

    def cut(self):
        """docstring for cut"""
        pass

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
            ({'name': '&Undo',
            'help': 'Undo last command',
            'id': guid.MENU_EDIT_UNDO,
            'method': self.undo},
            
            {'name': '&Redo',
            'help': 'Redo last command',
            'id': guid.MENU_EDIT_REDO,
            'method': self.redo},

            {'name': 'separator',
            'id': 'separator',
            'help': 'separator',
            'method': 'separator'},   
            
            {'name': '&Copy',
            'help': '',
            'id': guid.MENU_EDIT_COPY,
            'method': self.copy},
            
            {'name': 'C&ut',
            'help': '',
            'id': guid.MENU_EDIT_CUT,
            'method': self.cut},
            
            {'name': '&Paste',
            'help': '',
            'id': guid.MENU_EDIT_PASTE,
            'method': self.paste},
      
            {'name': 'separator',
            'id': 'separator',
            'help': 'separator',
            'method': 'separator'},
            
            {'name': 'Pr&eferences',
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
            
        help_menu = {'name': '&Help',
        'items':
            ({'name': 'Visit Website',
            'id': guid.MENU_HELP_WEBSITE,
            'help': 'Visit the website',
            'method': self.visitWebsite},)}

        menu = (file_menu, edit_menu, view_menu, help_menu)

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
    

class BeerMaker(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        ds = DataStore()
        BeerMaker = MainFrame(None, -1, "BeerMaker", size=(800,600))
        self.SetTopWindow(BeerMaker)
        BeerMaker.Show()
        return 1

# end of class BeerMaker

if __name__ == "__main__":
    BeerMaker = BeerMaker(0)
    BeerMaker.MainLoop()