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
from models import Recipe, Batch, BJCPStyle, BJCPCategory, Measures, EquipmentSet, MashProfile

from base import BaseWindow

class Ingredient():
    """
    Convience class for the ingredients_ctrl ObjectListView.  These are genered by RecipeEditor._gatherIngredients from models.RecipeIngredient
    """

    def __init__(self, name, ingredient_type, amount, use_in, time_used, percentage, amount_units, use_in_units):
        self.name = name
        self.ingredient_type = ingredient_type
        self.amount = amount
        self.use_in = use_in
        self.use_in_units = use_in_units
        self.time_used = time_used
        self.percentage = percentage
        self.amount_units = amount_units

class Mash():
    
    def __init__(self, name, start_temp, end_temp, time, temp_units):
        self.name = name
        self.start_temp = start_temp
        self.end_temp = end_temp
        self.time = time
        self.temp_units = temp_units


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
        self._setupMashes()

        if self.is_batch:
            self._gatherIngredients()
     
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
                    # {'widget': wx.Choice, 'choices': self._getLiquidVolumeChoices(), 'size': (-1,-1)},
                    {'widget': wx.StaticText, 'label': 'Batch Volume:', 'flag': self.ST_STYLE},
                    {'widget': wx.TextCtrl, 'event': {'event_type': wx.EVT_TEXT, 'method': self.onTextEvent}},
                    # {'widget': wx.Choice, 'choices': self._getLiquidVolumeChoices(), 'size': (-1,-1)},
                    {'widget': wx.StaticText, 'label': 'Equipment:', 'flag': self.ST_STYLE},
                    {'widget': wx.Choice, 'choices': self._getEquipmentChoices()},
                    {'widget': wx.CheckBox, 'proportion': 1, 'label': 'Boil volume set to equipment'},
                    )
                }, # end second row
                {'widget': wx.BoxSizer, 'title': 'Ingredients', 'flag': wx.ALL|wx.EXPAND, 'proportion': 1, 'style': wx.HORIZONTAL, 'widgets':
                    ({'widget': ObjectListView, 'var': 'ingredients_ctrl', 'style': wx.LC_REPORT, 'cellEditMode': ObjectListView.CELLEDIT_DOUBLECLICK, 'flag': wx.EXPAND|wx.ALL, 'proportion': 1},
                    {'widget': wx.BoxSizer, 'flag': wx.ALL|wx.EXPAND, 'style': wx.VERTICAL, 'widgets':
                        ({'widget': wx.Button, 'id': wx.ID_ADD},
                        {'widget': wx.Button, 'id': wx.ID_DELETE},
                        {'widget': wx.Button, 'id': wx.ID_UP},
                        {'widget': wx.Button, 'id': wx.ID_DOWN},
                        )},                        
                    )
                }, # end third row
                {'widget': wx.BoxSizer, 'title': 'Recipe Statistics', 'flag': wx.ALL|wx.EXPAND, 'proportion': 0, 'style': wx.HORIZONTAL, 'widgets':
                    ({'widget': wx.FlexGridSizer, 'rows': 11, 'cols': 2, 'vgap': 3, 'hgap': 3, 'widgets':
                        ({'widget': wx.StaticText, 'label': 'Style', 'style': wx.ALL, 'border': 3, 'proportion': 0},
                        {'widget': wx.StaticText, 'label': 'OG:' , 'style': self.ST_STYLE},
                        {'widget': wx.TextCtrl, 'event': {'event_type': wx.EVT_TEXT, 'method': self.onTextEvent}},
                        {'widget': wx.StaticText, 'label': 'FG:' , 'style': self.ST_STYLE},
                        {'widget': wx.TextCtrl, 'event': {'event_type': wx.EVT_TEXT, 'method': self.onTextEvent}},
                        {'widget': wx.StaticText, 'label': 'Color:' , 'style': self.ST_STYLE},
                        {'widget': wx.TextCtrl, 'event': {'event_type': wx.EVT_TEXT, 'method': self.onTextEvent}},
                        {'widget': wx.StaticText, 'label': 'ABV:' , 'style': self.ST_STYLE},
                        {'widget': wx.TextCtrl, 'event': {'event_type': wx.EVT_TEXT, 'method': self.onTextEvent}},
                        {'widget': wx.StaticText, 'label': 'Bitterness Ratio:' , 'style': self.ST_STYLE},
                        {'widget': wx.TextCtrl, 'event': {'event_type': wx.EVT_TEXT, 'method': self.onTextEvent}},
                        {'widget': wx.StaticText, 'label': 'Recipe', 'style': wx.ALL, 'border': 3, 'proportion': 0},
                        {'widget': wx.StaticText, 'label': 'OG:' , 'style': self.ST_STYLE},
                        {'widget': wx.TextCtrl, 'event': {'event_type': wx.EVT_TEXT, 'method': self.onTextEvent}},
                        {'widget': wx.StaticText, 'label': 'FG:' , 'style': self.ST_STYLE},
                        {'widget': wx.TextCtrl, 'event': {'event_type': wx.EVT_TEXT, 'method': self.onTextEvent}},
                        {'widget': wx.StaticText, 'label': 'Color:' , 'style': self.ST_STYLE},
                        {'widget': wx.TextCtrl, 'event': {'event_type': wx.EVT_TEXT, 'method': self.onTextEvent}},
                        {'widget': wx.StaticText, 'label': 'ABV:' , 'style': self.ST_STYLE},
                        {'widget': wx.TextCtrl, 'event': {'event_type': wx.EVT_TEXT, 'method': self.onTextEvent}},
                        {'widget': wx.StaticText, 'label': 'Bitterness Ratio:' , 'style': self.ST_STYLE},
                        {'widget': wx.TextCtrl, 'event': {'event_type': wx.EVT_TEXT, 'method': self.onTextEvent}},
                        )},
                    )
                }, # end fourth row  
                {'widget': wx.BoxSizer, 'style': wx.HORIZONTAL, 'proportion': 0, 'flag': wx.ALL|wx.EXPAND, 'widgets':
                    ({'widget': wx.BoxSizer, 'title': 'Mash', 'proportion': 1, 'flag': wx.ALL|wx.EXPAND, 'style': wx.VERTICAL, 'widgets':
                        ({'widget': wx.BoxSizer, 'style': wx.HORIZONTAL, 'proportion': 0, 'flag': wx.ALL|wx.EXPAND, 'widgets':
                            ({'widget': wx.StaticText, 'label': 'Mash Type:', 'style': self.ST_STYLE},
                            {'widget': wx.Choice, 'choices': self._getMashChoices()},)},
                        {'widget': ObjectListView, 'size': (500, -1), 'var': 'mash_ctrl', 'style': wx.LC_REPORT|wx.EXPAND, 'cellEditMode': ObjectListView.CELLEDIT_DOUBLECLICK, 'flag': wx.EXPAND|wx.ALL, 'proportion': 1},
                        {'widget': wx.BoxSizer, 'style': wx.HORIZONTAL, 'widgets':
                            ({'widget': wx.Button, 'id': wx.ID_ADD},
                            {'widget': wx.Button, 'id': wx.ID_DELETE},
                            {'widget': wx.Button, 'id': wx.ID_UP},
                            {'widget': wx.Button, 'id': wx.ID_DOWN})},)},
                    {'widget': wx.BoxSizer, 'style': wx.VERTICAL, 'title': 'Fermentation', 'border': 3, 'flag': wx.ALL|wx.EXPAND, 'widgets':
                        ({'widget': wx.FlexGridSizer, 'vgap': 3, 'hgap': 3, 'rows': 2, 'cols': 4, 'widgets':
                            ({'widget': wx.StaticText, 'label': 'Stages:', 'style': self.ST_STYLE},
                            {'widget': wx.Choice, 'choices': self._getFermentationStageChoices()},
                            {'widget': wx.StaticText, 'label': 'Primary:', 'style': self.ST_STYLE},
                            {'widget': wx.TextCtrl, 'event': {'event_type': wx.EVT_TEXT, 'method': self.onTextEvent}},
                            {'widget': wx.StaticText, 'label': 'Secondary:', 'style': self.ST_STYLE},
                            {'widget': wx.TextCtrl, 'event': {'event_type': wx.EVT_TEXT, 'method': self.onTextEvent}},
                            {'widget': wx.StaticText, 'label': 'Teritary:', 'style': self.ST_STYLE},
                            {'widget': wx.TextCtrl, 'event': {'event_type': wx.EVT_TEXT, 'method': self.onTextEvent}},)},)},
                    {'widget': wx.BoxSizer, 'style': wx.VERTICAL, 'title': 'Carbonation', 'border': 3, 'flag': wx.ALL|wx.EXPAND, 'widgets':
                        ({'widget': wx.FlexGridSizer, 'vgap': 3, 'hgap': 3, 'rows': 2, 'cols': 4, 'widgets':
                            ({'widget': wx.StaticText, 'label': 'Type:', 'style': self.ST_STYLE},
                            {'widget': wx.Choice, 'choices': self._getCarbonationTypeChoices()},
                            {'widget': wx.StaticText, 'label': 'Volumes:', 'style': self.ST_STYLE},
                            {'widget': wx.TextCtrl, 'event': {'event_type': wx.EVT_TEXT, 'method': self.onTextEvent}},
                            {'widget': wx.StaticText, 'label': 'Style:', 'style': self.ST_STYLE},
                            {'widget': wx.TextCtrl, 'event': {'event_type': wx.EVT_TEXT, 'method': self.onTextEvent}},
                            {'widget': wx.StaticText, 'label': 'Amount:', 'style': self.ST_STYLE},
                            {'widget': wx.TextCtrl, 'event': {'event_type': wx.EVT_TEXT, 'method': self.onTextEvent}},
                            
                            )},
                        )
                    }
                            
                    )                
                }, # end fifth row              
                )
    def _getCarbonationTypeChoices(self):
        return Recipe.carbonation_types

    def _getFermentationStageChoices(self):
        return Recipe.fermentation_types

    def _getMashChoices(self):
        if MashProfile.select().count() == 0:
            return ['No Mashes Defined',]
        else:
            return ['%s' % m.name for m in list(MashProfile.select())]
                
    def _gatherIngredients(self):
        ing1 = Ingredient("Test", "Hop", 10, "Boil", 60, 0, 'oz', 'min')
        self.ingredient_list = [ing1, ]
        self.ingredients_ctrl.SetObjects(self.ingredient_list)

    def _setupIngredients(self):
        namec = ColumnDefn('Ingredient', 'left', -1, 'name', isSpaceFilling=True)
        typec= ColumnDefn('Type', 'left', 120, 'ingredient_type')
        use_inc = ColumnDefn('Use', 'left', 120, 'use_in')
        percentc = ColumnDefn('%', 'left', 120, 'percentage', stringConverter="%.2f")
        timec = ColumnDefn('Time', 'left', 120, 'time_used')
        amountc = ColumnDefn('Amount', 'left', 120, 'amount')
        
        self.ingredients_ctrl.SetColumns([namec, typec, amountc, use_inc, percentc, timec])

    def _setupMashes(self):
        namec = ColumnDefn('Name', 'left', -1, 'name', isSpaceFilling=True)
        startc = ColumnDefn('Start Temp', 'left', 80, 'start_temp')
        endc = ColumnDefn('End Temp', 'left', 80, 'end_temp')
        timec = ColumnDefn('Time', 'left', 80, 'time')
        
        self.mash_ctrl.SetColumns([namec, startc, endc, timec])

                    
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