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
from models import *
from beerutils import *
from ingredient_browser import IngredientBrowser

from base import BaseWindow 

class RecipeEditor(wx.Frame, BaseWindow):
    def __init__(self, *args, **kw):        
        if kw.has_key('recipe_id'):
            recipe_id = kw.pop('recipe_id')
        else:
            recipe_id = 0
        if kw.has_key('batch'):
            batch = True
        else:
            batch = False
        wx.Frame.__init__(self, *args, **kw)
        
        # are we making a new recipe, a new batch, or editing an
        # existing recipe; if existing, populate the fields
        if recipe_id == 0:
            self.recipe = Recipe()
        else:
            if batch:
                self.recipe = cloneRecipe(Recipe(), Recipe.get(recipe_id))
                self.master_recipe = recipe_id
            else:
                self.recipe = Recipe.get(recipe_id)
        
        # set up the ui basics
        self.status_bar = self.CreateStatusBar(1,0)
        self.tools = self.buildToolbar()
        
        # set up the main view
        self.main_panel = wx.Panel(self, -1)
        self.main_panel.SetSizer(self.buildLayout(self.main_panel))
        self._setupIngredients()
        self._setupMashes()
        self._updateStyleInfo()
        self.timer_running = False
        if recipe_id != 0:
            self._gatherIngredients()        
     
    def layoutData(self):
        return ({'widget': wx.BoxSizer, 'title': 'Recipe Basics', 'flag': wx.ALL|wx.EXPAND, 'style': wx.HORIZONTAL, 'widgets':
                    (
                    {'widget': wx.StaticText, 'label': 'Name:', 'flag': self.ST_STYLE, 'proportion': 0, 'border': 3},
                    {'widget': wx.TextCtrl, 'proportion': 1, 'var': 'recipe_name', 'event': {'event_type': wx.EVT_TEXT, 'method': self.DataChanged}},
                    {'widget': wx.StaticText, 'label': 'Style:', 'flag': self.ST_STYLE},
                    {'widget': wx.Choice, 'id': guid.STYLE_SELECT, 'size': (200,-1), 'var': 'recipe_style', 'choices': self._getStyleChoices(), 'event': {'event_type': wx.EVT_CHOICE, 'method': self.DataChanged}},
                    {'widget': wx.StaticText, 'label': 'Brewer:', 'flag': self.ST_STYLE},
                    {'widget': wx.TextCtrl, 'var': 'recipe_brewer', 'event': {'event_type': wx.EVT_TEXT, 'method': self.DataChanged}},
                    {'widget': wx.StaticText, 'label': 'Brewed on:', 'display': self.recipe.is_batch, 'flag': self.ST_STYLE},
                    {'widget': wx.DatePickerCtrl, 'var': 'recipe_brewed_on', 'style': wx.DP_DEFAULT, 'display': self.recipe.is_batch, 'event': {'event_type': wx.EVT_DATE_CHANGED, 'method': self.DataChanged}},
                    {'widget': wx.StaticText, 'label': 'Type:', 'flag': self.ST_STYLE},
                    {'widget': wx.Choice, 'var': 'recipe_type', 'choices': self._getRecipeTypeChoices(), 'event': {'event_type': wx.EVT_CHOICE, 'method': self.DataChanged}},
                    )
                }, # end top row
                {'widget': wx.BoxSizer, 'flag': wx.ALL|wx.EXPAND, 'style': wx.HORIZONTAL, 'widgets':
                    (
                    {'widget': wx.StaticText, 'label': 'Boil Volume:', 'flag': self.ST_STYLE},
                    {'widget': wx.TextCtrl, 'var': 'recipe_boil_volume','event': {'event_type': wx.EVT_TEXT, 'method': self.DataChanged}},
                    {'widget': wx.StaticText, 'label': 'Batch Volume:', 'flag': self.ST_STYLE},
                    {'widget': wx.TextCtrl, 'var': 'recipe_batch_volume', 'event': {'event_type': wx.EVT_TEXT, 'method': self.DataChanged}},
                    {'widget': wx.StaticText, 'label': 'Equipment:', 'flag': self.ST_STYLE},
                    {'widget': wx.Choice, 'var': 'recipe_equipment', 'choices': self._getEquipmentChoices(), 'event': {'event_type': wx.EVT_CHOICE, 'method': self.DataChanged}},
                    {'widget': wx.CheckBox, 'var': 'recipe_boil_set_to_equipment', 'proportion': 1, 'label': 'Boil volume set to equipment', 'event': {'event_type': wx.EVT_CHECKBOX, 'method': self.DataChanged}},
                    )
                }, # end second row
                {'widget': wx.BoxSizer, 'title': 'Ingredients', 'flag': wx.ALL|wx.EXPAND, 'proportion': 1, 'style': wx.VERTICAL, 'widgets':
                    ({'widget': ObjectListView, 'var': 'ingredients_ctrl', 'style': wx.LC_REPORT, 'cellEditMode': ObjectListView.CELLEDIT_DOUBLECLICK, 'flag': wx.EXPAND|wx.ALL, 'proportion': 1},
                    {'widget': wx.BoxSizer, 'flag': wx.ALL|wx.EXPAND, 'style': wx.HORIZONTAL, 'widgets':
                        (
                        {'widget': wx.Button, 'label': '+', 'event': {'event_type': wx.EVT_BUTTON, 'method': self.InventoryAdd}},
                        {'widget': wx.Button, 'label': '-', 'event': {'event_type': wx.EVT_BUTTON, 'method': self.InventoryDelete}},
                        )},                        
                    )
                }, # end third row
                {'widget': wx.BoxSizer, 'title': 'Recipe Statistics', 'flag': wx.ALL|wx.EXPAND, 'proportion': 0, 'style': wx.HORIZONTAL, 'widgets':
                    ({'widget': wx.FlexGridSizer, 'rows': 13, 'cols': 2, 'vgap': 3, 'hgap': 3, 'widgets':
                        ({'widget': wx.StaticText, 'label': 'Style', 'font': self.GetNewFont(pointSize=13, style=wx.ITALIC), 'style': wx.ALL, 'border': 3, 'proportion': 0},
                        {'widget': wx.StaticText, 'label': 'OG:' , 'style': self.ST_STYLE},
                        {'widget': wx.TextCtrl, 'editable': False, 'var': 'style_og'},
                        {'widget': wx.StaticText, 'label': 'FG:' , 'style': self.ST_STYLE},
                        {'widget': wx.TextCtrl, 'editable': False, 'var': 'style_fg'},
                        {'widget': wx.StaticText, 'label': 'Color:' , 'style': self.ST_STYLE},
                        {'widget': wx.TextCtrl, 'editable': False, 'var': 'style_srm'},
                        {'widget': wx.StaticText, 'label': 'ABV:' , 'style': self.ST_STYLE},
                        {'widget': wx.TextCtrl, 'editable': False, 'var': 'style_abv'},
                        {'widget': wx.StaticText, 'label': 'IBU:' , 'style': self.ST_STYLE},
                        {'widget': wx.TextCtrl, 'editable': False, 'var': 'style_ibu'},                        
                        {'widget': wx.StaticText, 'label': 'Bitterness Ratio:' , 'style': self.ST_STYLE},
                        {'widget': wx.TextCtrl, 'editable': False, 'var': 'style_br'},
                        {'widget': wx.StaticText, 'label': 'Recipe', 'font': self.GetNewFont(pointSize=13, style=wx.ITALIC), 'style': wx.ALL, 'border': 3, 'proportion': 0},
                        {'widget': wx.StaticText, 'label': 'OG:' , 'style': self.ST_STYLE},
                        {'widget': wx.TextCtrl, 'var': 'recipe_og', 'event': {'event_type': wx.EVT_TEXT, 'method': self.DataChanged}},
                        {'widget': wx.StaticText, 'label': 'FG:' , 'style': self.ST_STYLE},
                        {'widget': wx.TextCtrl, 'var': 'recipe_fg', 'event': {'event_type': wx.EVT_TEXT, 'method': self.DataChanged}},
                        {'widget': wx.StaticText, 'label': 'Color:' , 'style': self.ST_STYLE},
                        {'widget': wx.TextCtrl, 'var': 'recipe_srm', 'event': {'event_type': wx.EVT_TEXT, 'method': self.DataChanged}},
                        {'widget': wx.StaticText, 'label': 'ABV:' , 'style': self.ST_STYLE},
                        {'widget': wx.TextCtrl, 'var': 'recipe_abv', 'event': {'event_type': wx.EVT_TEXT, 'method': self.DataChanged}},
                        {'widget': wx.StaticText, 'label': 'IBU:' , 'style': self.ST_STYLE},
                        {'widget': wx.TextCtrl, 'var': 'recipe_ibu', 'event': {'event_type': wx.EVT_TEXT, 'method': self.DataChanged}},                        
                        {'widget': wx.StaticText, 'label': 'Bitterness Ratio:' , 'style': self.ST_STYLE},
                        {'widget': wx.TextCtrl, 'var': 'recipe_br', 'event': {'event_type': wx.EVT_TEXT, 'method': self.DataChanged}},
                        )},
                    )
                }, # end fourth row  
                {'widget': wx.BoxSizer, 'style': wx.HORIZONTAL, 'proportion': 0, 'flag': wx.ALL|wx.EXPAND, 'widgets':
                    ({'widget': wx.BoxSizer, 'title': 'Mash', 'proportion': 1, 'flag': wx.ALL|wx.EXPAND, 'style': wx.VERTICAL, 'widgets':
                        ({'widget': wx.BoxSizer, 'style': wx.HORIZONTAL, 'proportion': 0, 'flag': wx.ALL|wx.EXPAND, 'widgets':
                            ({'widget': wx.StaticText, 'label': 'Mash Type:', 'style': self.ST_STYLE},
                            {'widget': wx.Choice, 'var': 'mash_choice', 'choices': self._getMashChoices(), 'event': {'event_type': wx.EVT_CHOICE, 'method': self.DataChanged}},)},
                        {'widget': ObjectListView, 'var': 'mash_ctrl', 'style': wx.LC_REPORT|wx.EXPAND, 'cellEditMode': ObjectListView.CELLEDIT_DOUBLECLICK, 'flag': wx.EXPAND|wx.ALL, 'proportion': 1},
                        {'widget': wx.BoxSizer, 'style': wx.HORIZONTAL, 'widgets':
                            ({'widget': wx.Button, 'id': wx.ID_ADD, 'event': {'event_type': wx.EVT_BUTTON, 'method': self.MashAdd}},
                            {'widget': wx.Button, 'id': wx.ID_DELETE, 'event': {'event_type': wx.EVT_BUTTON, 'method': self.MashDelete}},
                            {'widget': wx.Button, 'id': wx.ID_UP, 'event': {'event_type': wx.EVT_BUTTON, 'method': self.MashUp}},
                            {'widget': wx.Button, 'id': wx.ID_DOWN, 'event': {'event_type': wx.EVT_BUTTON, 'method': self.MashDown}})},)},
                    {'widget': wx.BoxSizer, 'style': wx.VERTICAL, 'title': 'Fermentation', 'border': 3, 'flag': wx.ALL, 'widgets':
                        ({'widget': wx.BoxSizer, 'style': wx.HORIZONTAL, 'flag': wx.ALIGN_CENTER, 'widgets':
                        ({'widget': wx.StaticText, 'label': 'Stages:', 'style': self.ST_STYLE},
                        {'widget': wx.Choice, 'var': 'fermentation_type', 'choices': self._getFermentationStageChoices(), 'event': {'event_type': wx.EVT_CHOICE, 'method': self.DataChanged}},)},
                        {'widget': wx.FlexGridSizer, 'vgap': 3, 'hgap': 3, 'rows': 4, 'cols': 4, 'widgets':
                            ({'widget': wx.StaticText, 'label': 'Primary:', 'style': self.ST_STYLE},
                            {'widget': wx.TextCtrl, 'var': 'primary_length', 'event': {'event_type': wx.EVT_TEXT, 'method': self.DataChanged}},
                            {'widget': wx.StaticText, 'label': 'Temperature:', 'style': self.ST_STYLE},
                            {'widget': wx.TextCtrl, 'var': 'primary_temp', 'event': {'event_type': wx.EVT_TEXT, 'method': self.DataChanged}},
                            {'widget': wx.StaticText, 'label': 'Secondard:', 'style': self.ST_STYLE},
                            {'widget': wx.TextCtrl, 'var': 'secondary_length', 'event': {'event_type': wx.EVT_TEXT, 'method': self.DataChanged}},
                            {'widget': wx.StaticText, 'label': 'Temperature:', 'style': self.ST_STYLE},
                            {'widget': wx.TextCtrl, 'var': 'secondary_temp', 'event': {'event_type': wx.EVT_TEXT, 'method': self.DataChanged}},
                            {'widget': wx.StaticText, 'label': 'Tertiary:', 'style': self.ST_STYLE},
                            {'widget': wx.TextCtrl, 'var': 'tertiary_length', 'event': {'event_type': wx.EVT_TEXT, 'method': self.DataChanged}},
                            {'widget': wx.StaticText, 'label': 'Temperature:', 'style': self.ST_STYLE},
                            {'widget': wx.TextCtrl, 'var': 'teritary_temp', 'event': {'event_type': wx.EVT_TEXT, 'method': self.DataChanged}},)},)},
                    {'widget': wx.BoxSizer, 'style': wx.VERTICAL, 'title': 'Carbonation', 'border': 3, 'flag': wx.ALL|wx.EXPAND, 'widgets':
                        ({'widget': wx.FlexGridSizer, 'vgap': 3, 'hgap': 3, 'rows': 2, 'cols': 4, 'widgets':
                            ({'widget': wx.StaticText, 'label': 'Type:', 'style': self.ST_STYLE},
                            {'widget': wx.Choice, 'var': 'carbonation_type', 'choices': self._getCarbonationTypeChoices(), 'event': {'event_type': wx.EVT_CHOICE, 'method': self.DataChanged}},
                            {'widget': wx.StaticText, 'label': 'Style:', 'style': self.ST_STYLE},
                            {'widget': wx.TextCtrl, 'var': 'carbonation_style', 'editable': False, 'event': {'event_type': wx.EVT_TEXT, 'method': self.DataChanged}},
                            {'widget': wx.StaticText, 'label': 'Volumes:', 'style': self.ST_STYLE},
                            {'widget': wx.TextCtrl, 'var': 'carbonation_volumes', 'editable': False, 'event': {'event_type': wx.EVT_TEXT, 'method': self.DataChanged}},
                            {'widget': wx.StaticText, 'label': 'Amount Used:', 'style': self.ST_STYLE},
                            {'widget': wx.TextCtrl, 'var': 'carbonation_used', 'event': {'event_type': wx.EVT_TEXT, 'method': self.DataChanged}},
                            )},
                        )
                    }
                            
                    )                
                }, # end fifth row              
                )
                
    def InventoryAdd(self, event):
        inventory = IngredientBrowser(self, -1, "Ingredient Browser", pos=(50,50), size=(800,600))
        if inventory.ShowModal() == wx.ID_OK:
            ingredient = inventory.ingredients_ctrl.GetSelectedObject()
            ingredient_type = inventory.inventory_types[inventory.ing_choices.GetCurrentSelection()]
            amount = Measure(inventory.amount_ctrl.GetValue())
            time_used = Measure(inventory.time_used_ctrl.GetValue())
            use_in = inventory.use_choices.GetCurrentSelection()
            
            ing = RecipeIngredient(recipe=self.recipe.id, ingredient_id=ingredient, amount=amount, use_in=use_in, time_used=time_used)
            self.recipe.add_to_total_weight(amount.convert('oz'), ingredient_type.lower())
            self.ingredients_ctrl.AddObject(ing)
            self.updateRecipePercentage()
            self.ingredients_ctrl.AutoSizeColumns()
            
            self.updateRecipeStats()
            
        inventory.Destroy()
        event.Skip()

    def updateRecipePercentage(self):
        for ingredient in self.ingredients_ctrl.GetObjects():
            ingredient.percentage = self._getPercentOfTotalBill(ingredient.amount_m, ingredient_type)
            self.ingredients_ctrl.RefreshObject(ingredient)

    def _getPercentOfTotalBill(self, new_amount, ingredient_type):
        total_ingredient = getattr(self.recipe, '%s_total_weight' % ingredient_type.lower())
        return (new_amount.convert('oz') / total_ingredient) * Decimal('100.0')

    def InventoryDelete(self, event):
        ingredient = self.ingredients_ctrl.GetSelectedObject()
        self.recipe.remove_from_total_weigt(ingredient.amount.convert('oz'), ingredient.ingredient_type.lower())
        self.ingredients_ctrl.RemoveObject(ingredient)
        self.updateRecipePercentage()
        event.Skip()
        
    def updateRecipeStats(self):
        pass
        
    def _updateStyleInfo(self):
        (style_id, style_name) = self.style_choices[self.recipe_style.GetCurrentSelection()].split(":")
        style = BJCPStyle.select(BJCPStyle.q.name==style_name.strip()).getOne()
        self.style_og.SetValue(style.og_range)
        self.style_fg.SetValue(style.fg_range)
        self.style_srm.SetValue(style.srm_range)
        self.style_abv.SetValue(style.abv_range)
        self.style_ibu.SetValue(style.ibu_range)
        br_high = calculateBitternessRatio(style.og_high, style.ibu_high)
        br_low = calculateBitternessRatio(style.og_low, style.ibu_low)
        self.style_br.SetValue("%s - %s" % (br_high, br_low))

    def MashAdd(self, event):
        """docstring for MashAdd"""
        pass
    
    def MashDelete(self, event):
        """docstring for MashDelete"""
        pass
        
    def MashUp(self, event):
        """docstring for MashUp"""
        pass
        
    def MashDown(self, event):
        pass
        
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
        namec = ColumnDefn('Ingredient', 'left', 200, 'name', minimumWidth=200, isSpaceFilling=True)
        typec= ColumnDefn('Type', 'left', 100, 'ingredient_type')
        use_inc = ColumnDefn('Use', 'left', 100, 'use_in', stringConverter=getUseIn)
        percentc = ColumnDefn('%', 'left', 100, 'percentage', stringConverter="%.2f")
        timec = ColumnDefn('Time', 'left', 100, 'time_used_m', stringConverter="%s")
        amountc = ColumnDefn('Amount', 'left', 100, 'amount_m', stringConverter="%s")
        
        namec.freeSpaceProportion = 2
        
        self.ingredients_ctrl.oddRowsBackColor = wx.WHITE        
        self.ingredients_ctrl.SetColumns([namec, typec, amountc, use_inc, percentc, timec])

    def _setupMashes(self):
        namec = ColumnDefn('Name', 'left', -1, 'name', isSpaceFilling=True)
        startc = ColumnDefn('Start Temp', 'left', 80, 'start_temp')
        endc = ColumnDefn('End Temp', 'left', 80, 'end_temp')
        timec = ColumnDefn('Time', 'left', 80, 'time')
        
        self.mash_ctrl.oddRowsBackColor = wx.WHITE
        self.mash_ctrl.SetColumns([namec, startc, endc, timec])
                    
    def _getStyleChoices(self):
        self.style_choices =  ["%s: %s" % (st.combined_category_id, st.name) for st in list(BJCPStyle.select())]
        return self.style_choices
  
    def _getRecipeTypeChoices(self):
        return Recipe.recipe_types
            
    def _getEquipmentChoices(self):
        if EquipmentSet.select().count() == 0:
            return ['Equipment Not Set',]
        else:
            return ['%s' % e.name for e in list(EquipmentSet.select())]

    def BoilSetToEquipment(self, event):
        pass

    def DataChanged(self, event):
        if self.timer_running:
            self.save_timer.Restart()
        else:
            self.save_timer = wx.FutureCall(1500, self.SaveRecipe)
            self.timer_running = True
            
        if event.GetId() == guid.STYLE_SELECT:
            self._updateStyleInfo()
        
        event.Skip()
  
    def SaveRecipe(self):
        self.recipe.name = self.recipe_name.GetValue()
        

  
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