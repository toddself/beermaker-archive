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
import wx.calendar as cal

from ObjectListView import ObjectListView, ColumnDefn

import guid
import iconsrc

from db import DataStore
from models import Recipe, Batch, BJCPStyle, BJCPCategory, Measures, EquipmentSet

from base import BaseWindow

class RecipeEditor(wx.Frame, BaseWindow):
    def __init__(self, parent, fid, title, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE):
        wx.Frame.__init__(self, parent, fid, title, pos, size, style)
        
        # set up the ui basics
        self.status_bar = self.CreateStatusBar(1,0)
        self.tools = self.buildToolbar()
        
        # set up if this is a batch or a master recipe
        # by default we're never editing a batch
        self.is_batch = False   
        
        # set up the main view
        self.main_panel = wx.Panel(self, -1)
        self.main_panel.SetSizer(self.buildLayout(self.main_panel))
        
        self._setupIngredients()
                                          
    def layoutData(self):
        return ({'widget': wx.BoxSizer, 'title': 'Recipe Basics', 'flag': wx.ALL|wx.EXPAND, 'style': wx.HORIZONTAL, 'widgets':
                    (
                    {'widget': wx.StaticText, 'label': 'Name:', 'flag': self.ST_STYLE, 'proportion': 0, 'border': 3},
                    {'widget': wx.TextCtrl, 'proportion': 1, 'event': {'event_type': wx.EVT_TEXT, 'method': self.onTextEvent}},
                    {'widget': wx.StaticText, 'label': 'Style:', 'flag': self.ST_STYLE},
                    {'widget': wx.Choice, 'size': (200,-1), 'choices': self._getStyleChoices()},
                    {'widget': wx.StaticText, 'label': 'Brewer:', 'flag': self.ST_STYLE},
                    {'widget': wx.TextCtrl, 'event': {'event_type': wx.EVT_TEXT, 'method': self.onTextEvent}},
                    {'widget': wx.StaticText, 'label': 'Brewed on:', 'display': self.is_batch, 'flag': self.ST_STYLE},
                    {'widget': wx.DatePickerCtrl, 'style': wx.DP_DEFAULT, 'display': self.is_batch},
                    {'widget': wx.StaticText, 'label': 'Type:', 'flag': self.ST_STYLE},
                    {'widget': wx.Choice, 'choices': self._getRecipeTypeChoices()},
                    )
                }, # end top row
                {'widget': wx.BoxSizer, 'flag': wx.ALL|wx.EXPAND, 'style': wx.HORIZONTAL, 'widgets':
                    (
                    {'widget': wx.StaticText, 'label': 'Boil Volume:', 'flag': self.ST_STYLE},
                    {'widget': wx.TextCtrl, 'event': {'event_type': wx.EVT_TEXT, 'method': self.onTextEvent}},
                    {'widget': wx.Choice, 'choices': self._getLiquidVolumeChoices(), 'size': (-1,-1)},
                    {'widget': wx.StaticText, 'label': 'Batch Volume:', 'flag': self.ST_STYLE},
                    {'widget': wx.TextCtrl, 'event': {'event_type': wx.EVT_TEXT, 'method': self.onTextEvent}},
                    {'widget': wx.Choice, 'choices': self._getLiquidVolumeChoices(), 'size': (-1,-1)},
                    {'widget': wx.StaticText, 'label': 'Equipment:', 'flag': self.ST_STYLE},
                    {'widget': wx.Choice, 'choices': self._getEquipmentChoices()},
                    {'widget': wx.CheckBox, 'proportion': 1, 'label': 'Boil set to equipment'},
                    )
                }, # end second row
                {'widget': wx.BoxSizer, 'title': 'Ingredients', 'flag': wx.ALL|wx.EXPAND, 'proportion': 1, 'style': wx.HORIZONTAL, 'widgets':
                    ({'widget': ObjectListView, 'var': 'ingredients_ctrl', 'cellEditMode': ObjectListView.CELLEDIT_DOUBLECLICK, 'flag': wx.EXPAND|wx.ALL, 'proportion': 1},
                    {'widget': wx.BoxSizer, 'title': 'Details', 'flag': wx.ALL|wx.EXPAND, 'style': wx.VERTICAL, 'widgets':
                        ({'widget': wx.Button, 'id': wx.ID_ADD},
                        {'widget': wx.Button, 'id': wx.ID_DELETE},
                        {'widget': wx.Button, 'id': wx.ID_UP},
                        {'widget': wx.Button, 'id': wx.ID_DOWN},
                        )},                        
                    )
                }, # end third row
                )

    def _setupIngredients(self):
        ingredient_name_column = ColumnDefn('Ingredient', 'left', 120, 'name')
        
        pass
                    
    def onTextEvent(self, event):
        pass

    def _getStyleChoices(self):
        return ["%s: %s" % (st.combined_category_id, st.name) for st in list(BJCPStyle.select())]
  
    def _getRecipeTypeChoices(self):
        return Recipe.recipe_types
    
    def _getLiquidVolumeChoices(self):
        lm = []
        for m in Measures.liquid_measures:
            lm.append(Measures.measures[m])
        return lm
        
    def _getEquipmentChoices(self):
        if EquipmentSet.select().count() == 0:
            return ['Equipment Not Set',]
        else:
            return ['%s' % e.name for e in list(EquipmentSet.select())]
  
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
    
    def checkIngredients(self):
        """docstring for checkIngredients"""
        pass
        
    def removeIngredients(self):
        """docstring for removeIngredients"""
        pass
    
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
            (guid.TB_INGREDIENT_CHECK, iconsrc.tb_ingredient_check, "Check Ingredients", "Verify you have the ingredients on hand for this batch", self.checkIngredients),
            (guid.TB_INGREDIENT_REMOVE, iconsrc.tb_ingredient_remove, "Remove Ingredients", "Remove the ingredients for this batch from your inventory", self.removeIngredients),
            ("","","","",""),
            (guid.TB_CALCULATORS, iconsrc.tb_calculators, "Calculators", "View all the calculators", self.viewCalculators),
            
        )
        
class RE(wx.App):
    def OnInit(self):
        wx.InitAllImageHandlers()
        ds = DataStore()
        reditor = RecipeEditor(None, -1, "", size=(1024,768))
        self.SetTopWindow(reditor)
        reditor.Show()
        return 1

if __name__ == "__main__":
    R = RE(0)
    R.MainLoop()