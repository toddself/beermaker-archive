#!/usr/bin/env python

# TODO:
# MAKE TEXT FIELDS NON-EDITABLE WHERE APPROPRIATE
# FINISH INGREDIENTS DIALOG



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
from algorithms import convertToOz

from base import BaseWindow 

class IngredientBrowser(wx.Dialog, BaseWindow):
    inventory_types = ['Grain', 'Extract', 'Hop', 'Yeast', 'Misc']
    
    def __init__(self, *args, **kw):
        wx.Dialog.__init__(self, *args, **kw)
        
        self.main_panel = wx.Panel(self, -1)
        sizer = self.buildLayout(self.main_panel)
        self.main_panel.SetSizer(sizer)
        
        self._setupIngredientsCtrl()
        self._populateIngredients()

    def layoutData(self):
        return ({'widget': wx.BoxSizer, 'flag': wx.ALL|wx.EXPAND, 'proportion': 1, 'style': wx.VERTICAL, 'widgets':
                    ({'widget': wx.BoxSizer, 'flag': wx.ALIGN_CENTER|wx.ALL, 'style': wx.HORIZONTAL, 'widgets':
                        ({'widget': wx.StaticText, 'style': self.ST_STYLE, 'label': 'Type:'},
                        {'widget': wx.Choice, 'var': 'ing_choices', 'choices': self._getIngredientTypeChoices(), 'event': {'event_type': wx.EVT_CHOICE, 'method': self.OnIngredientSelect}})
                    },
                    {'widget': ObjectListView, 'style': wx.LC_REPORT, 'var': 'ingredients_ctrl', 'useAlternateBackColors': True, 'cellEditMode': ObjectListView.CELLEDIT_NONE, 'flag': wx.EXPAND|wx.ALL, 'proportion': 1},
                    {'widget': wx.BoxSizer, 'flag': wx.ALL|wx.EXPAND, 'style': wx.HORIZONTAL, 'widgets':
                        ({'widget': wx.StaticText, 'label': 'Amount:', 'flag': self.ST_STYLE},
                        {'widget': wx.TextCtrl, 'var': 'amount_ctrl'},
                        {'widget': wx.StaticText, 'label': 'Use in:', 'flag': self.ST_STYLE},
                        {'widget': wx.Choice, 'var': 'use_choices', 'choices': Misc.misc_use_ins},
                        {'widget': wx.StaticText, 'label': 'Time:', 'flag': self.ST_STYLE},
                        {'widget': wx.TextCtrl, 'var': 'time_used_ctrl'}
                        )
                    },
                    {'widget': wx.BoxSizer, 'flag': wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, 'style': wx.HORIZONTAL, 'widgets':
                        ({'widget': wx.Button, 'id': wx.ID_CANCEL, 'flag': wx.ALL|wx.ALIGN_RIGHT},
                        {'widget': wx.Button, 'id': wx.ID_OK, 'flag': wx.ALL|wx.ALIGN_RIGHT},)
                    },)
                },)

    def OnIngredientSelect(self, event):
        self._populateIngredients(self.inventory_types[event.GetSelection()])
        event.Skip()
        
    def _getIngredientTypeChoices(self):
        return self.inventory_types
    
    def _setupIngredientsCtrl(self, ing_type='Grain'):
        columns = []
        if ing_type == 'Grain':
            columns.append(ColumnDefn('Name', 'left', -1, 'name', isSpaceFilling=True))
            columns.append(ColumnDefn('Origin', 'left', 120, 'origin'))
            columns.append(ColumnDefn('SRM', 'left', 120, 'srm'))
            columns.append(ColumnDefn('Potential', 'left', 120, 'potential', stringConverter='%.3f'))
            columns.append(ColumnDefn('Inventory', 'left', 120, 'inventory'))
        elif ing_type == 'Hop':
            columns.append(ColumnDefn('Name', 'left', -1, 'name', isSpaceFilling=True))
            columns.append(ColumnDefn('Origin', 'left', 120, 'origin'))
            columns.append(ColumnDefn('Type', 'left', 120, 'hop_type', stringConverter=getHopType))
            columns.append(ColumnDefn('Alpha', 'left', 120, 'alpha'))
            columns.append(ColumnDefn('Inventory', 'left', 120, 'inventory'))
        elif ing_type == 'Extract':
            columns.append(ColumnDefn('Name', 'left', -1, 'name', isSpaceFilling=True))
            columns.append(ColumnDefn('Origin', 'left', 120, 'origin'))
            columns.append(ColumnDefn('SRM', 'left', 120, 'srm'))
            columns.append(ColumnDefn('Potential', 'left', 120, 'potential', stringConverter='%.3f'))
            columns.append(ColumnDefn('Inventory', 'left', 120, 'inventory'))
        elif ing_type == 'Yeast':
            columns.append(ColumnDefn('Name', 'left', -1, 'name', isSpaceFilling=True))
            columns.append(ColumnDefn('Lab', 'left', 120, 'lab'))
            columns.append(ColumnDefn('ID', 'left', 80, 'yeast_id'))
            columns.append(ColumnDefn('Type', 'left', 80, 'yeast_type', stringConverter=getYeastType))
            columns.append(ColumnDefn('Form', 'left', 80, 'yeast_form', stringConverter=getYeastForm))
            columns.append(ColumnDefn('Flocc.', 'left', 80, 'flocc', stringConverter=getYeastFlocc))
            columns.append(ColumnDefn('Atten.', 'left', 80, 'avg_attenuation', stringConverter=getYeastAtten))
        elif ing_type == 'Misc':
            pass
            
        
        self.ingredients_ctrl.oddRowsBackColor = wx.WHITE
        self.ingredients_ctrl.SetColumns(columns)
        
    def _populateIngredients(self, ing_type='Grain'):
        try:
            inventory = list(eval(ing_type).select())
        except:
            self.ingredients_ctrl.SetEmptyListMsg("No ingredients match your selection")
            

        self._setupIngredientsCtrl(ing_type)
        self.ingredients_ctrl.SetObjects(inventory)
        self.ingredients_ctrl.AutoSizeColumns()


class RecipeEditor(wx.Frame, BaseWindow):
    def __init__(self, parent, fid, title, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE, recipe_id=0):
        wx.Frame.__init__(self, parent, fid, title, pos, size, style)
        
        # set up the ui basics
        self.status_bar = self.CreateStatusBar(1,0)
        self.tools = self.buildToolbar()
        
        # set up if this is a batch or a master recipe
        # by default we're never editing a batch
        if recipe_id == 0:
            self.is_batch = False
            self.recipe_id = 0
        
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
                    {'widget': wx.TextCtrl, 'proportion': 1, 'var': 'recipe_name', 'event': {'event_type': wx.EVT_TEXT, 'method': self.onTextEvent}},
                    {'widget': wx.StaticText, 'label': 'Style:', 'flag': self.ST_STYLE},
                    {'widget': wx.Choice, 'size': (200,-1), 'var': 'recipe_style', 'choices': self._getStyleChoices()},
                    {'widget': wx.StaticText, 'label': 'Brewer:', 'flag': self.ST_STYLE},
                    {'widget': wx.TextCtrl, 'var': 'recipe_brewer', 'event': {'event_type': wx.EVT_TEXT, 'method': self.onTextEvent}},
                    {'widget': wx.StaticText, 'label': 'Brewed on:', 'display': self.is_batch, 'flag': self.ST_STYLE},
                    {'widget': wx.DatePickerCtrl, 'var': 'recipe_brewed_on', 'style': wx.DP_DEFAULT, 'display': self.is_batch},
                    {'widget': wx.StaticText, 'label': 'Type:', 'flag': self.ST_STYLE},
                    {'widget': wx.Choice, 'var': 'recipe_type', 'choices': self._getRecipeTypeChoices()},
                    )
                }, # end top row
                {'widget': wx.BoxSizer, 'flag': wx.ALL|wx.EXPAND, 'style': wx.HORIZONTAL, 'widgets':
                    (
                    {'widget': wx.StaticText, 'label': 'Boil Volume:', 'flag': self.ST_STYLE},
                    {'widget': wx.TextCtrl, 'var': 'recipe_boil_volume','event': {'event_type': wx.EVT_TEXT, 'method': self.onTextEvent}},
                    {'widget': wx.StaticText, 'label': 'Batch Volume:', 'flag': self.ST_STYLE},
                    {'widget': wx.TextCtrl, 'var': 'recipe_batch_volume', 'event': {'event_type': wx.EVT_TEXT, 'method': self.onTextEvent}},
                    {'widget': wx.StaticText, 'label': 'Equipment:', 'flag': self.ST_STYLE},
                    {'widget': wx.Choice, 'var': 'recipe_equipment', 'choices': self._getEquipmentChoices()},
                    {'widget': wx.CheckBox, 'var': 'recipe_boil_set_to_equipment', 'proportion': 1, 'label': 'Boil volume set to equipment', 'event': {'event_type': wx.EVT_CHECKBOX, 'method': self.BoilSetToEquipment}},
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
                    ({'widget': wx.FlexGridSizer, 'rows': 11, 'cols': 2, 'vgap': 3, 'hgap': 3, 'widgets':
                        ({'widget': wx.StaticText, 'label': 'Style', 'font': self.GetNewFont(pointSize=13, style=wx.ITALIC), 'style': wx.ALL, 'border': 3, 'proportion': 0},
                        {'widget': wx.StaticText, 'label': 'OG:' , 'style': self.ST_STYLE},
                        {'widget': wx.TextCtrl, 'editable': False, 'var': 'style_og', 'event': {'event_type': wx.EVT_TEXT, 'method': self.onTextEvent}},
                        {'widget': wx.StaticText, 'label': 'FG:' , 'style': self.ST_STYLE},
                        {'widget': wx.TextCtrl, 'editable': False, 'var': 'style_fg', 'event': {'event_type': wx.EVT_TEXT, 'method': self.onTextEvent}},
                        {'widget': wx.StaticText, 'label': 'Color:' , 'style': self.ST_STYLE},
                        {'widget': wx.TextCtrl, 'editable': False, 'var': 'style_srm', 'event': {'event_type': wx.EVT_TEXT, 'method': self.onTextEvent}},
                        {'widget': wx.StaticText, 'label': 'ABV:' , 'style': self.ST_STYLE},
                        {'widget': wx.TextCtrl, 'editable': False, 'var': 'style_abv', 'event': {'event_type': wx.EVT_TEXT, 'method': self.onTextEvent}},
                        {'widget': wx.StaticText, 'label': 'Bitterness Ratio:' , 'style': self.ST_STYLE},
                        {'widget': wx.TextCtrl, 'editable': False, 'var': 'style_br', 'event': {'event_type': wx.EVT_TEXT, 'method': self.onTextEvent}},
                        {'widget': wx.StaticText, 'label': 'Recipe', 'font': self.GetNewFont(pointSize=13, style=wx.ITALIC), 'style': wx.ALL, 'border': 3, 'proportion': 0},
                        {'widget': wx.StaticText, 'label': 'OG:' , 'style': self.ST_STYLE},
                        {'widget': wx.TextCtrl, 'var': 'recipe_og', 'event': {'event_type': wx.EVT_TEXT, 'method': self.onTextEvent}},
                        {'widget': wx.StaticText, 'label': 'FG:' , 'style': self.ST_STYLE},
                        {'widget': wx.TextCtrl, 'var': 'recipe_fg', 'event': {'event_type': wx.EVT_TEXT, 'method': self.onTextEvent}},
                        {'widget': wx.StaticText, 'label': 'Color:' , 'style': self.ST_STYLE},
                        {'widget': wx.TextCtrl, 'var': 'recipe_srm', 'event': {'event_type': wx.EVT_TEXT, 'method': self.onTextEvent}},
                        {'widget': wx.StaticText, 'label': 'ABV:' , 'style': self.ST_STYLE},
                        {'widget': wx.TextCtrl, 'var': 'recipe_abv', 'event': {'event_type': wx.EVT_TEXT, 'method': self.onTextEvent}},
                        {'widget': wx.StaticText, 'label': 'Bitterness Ratio:' , 'style': self.ST_STYLE},
                        {'widget': wx.TextCtrl, 'var': 'recipe_br', 'event': {'event_type': wx.EVT_TEXT, 'method': self.onTextEvent}},
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
                            ({'widget': wx.Button, 'id': wx.ID_ADD, 'event': {'event_type': wx.EVT_BUTTON, 'method': self.MashAdd}},
                            {'widget': wx.Button, 'id': wx.ID_DELETE, 'event': {'event_type': wx.EVT_BUTTON, 'method': self.MashDelete}},
                            {'widget': wx.Button, 'id': wx.ID_UP, 'event': {'event_type': wx.EVT_BUTTON, 'method': self.MashUp}},
                            {'widget': wx.Button, 'id': wx.ID_DOWN, 'event': {'event_type': wx.EVT_BUTTON, 'method': self.MashDown}})},)},
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
                
    def InventoryAdd(self, event):
        inventory = IngredientBrowser(self, -1, "Ingredient Browser", pos=(50,50), size=(800,600))
        if inventory.ShowModal() == wx.ID_OK:
            ingredient = inventory.ingredients_ctrl.GetSelectedObject()
            ingredient_type = inventory.inventory_types[inventory.ing_choices.GetCurrentSelection()]
            amount = inventory.amount_ctrl.GetValue()
            use_in = inventory.use_choices.GetCurrentSelection()
            time_used = inventory.time_used_ctrl.GetValue()
            if ingredient_type == 'Hop' or ingredient_type == 'Grain':
                percentage = self._getPercentOfTotalBill(amount, ingredient_type)
            else:
                percentage = ''
            
            ing = RecipeIngredient(recipe=self.recipe_id, ingredient_id=ingredient, amount=amount, use_in=use_in, time_used=time_used, percentage=percentage)
            
            for ingredient in self.ingredients_ctrl.GetObjects():
                ingredient.percentage = self._getPercentOfTotalBill(amount, ingredient_type)
                self.ingredients_ctrl.RefreshObject(ingredient)
                
            self.ingredients_ctrl.AddObject(ing)
            self.ingredients_ctrl.AutoSizeColumns()
            
        inventory.Destroy()

    def _getPercentOfTotalBill(self, amount, ingredient_type):
        (new_ing_amount, unit) = getAmountFromString(amount)
        new_ing_amount = convertToOz(new_ing_amount, unit)
        
        # we haven't actually added the new ingredient to the list, so we'll seed with the new ingredient amount
        total_ingredient = new_ing_amount
                
        for ingredient in self.ingredients_ctrl.GetObjects():
            if ingredient.ingredient_type == ingredient_type:
                if ingredient.amount_units != Measure.OZ:
                     amt = convertToOz(ingredient.amount, unit)
                total_ingredient = total_ingredient + amt
                
        if new_ing_amount > total_ingredient:
            return ((float(total_ingredient) / float(new_ing_amount)) * 100.0)
        else:
            return ((float(new_ing_amount) / float(total_ingredient)) * 100.0)
                
        
    def InventoryDelete(self, event):
        pass
        
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
        timec = ColumnDefn('Time', 'left', 100, 'time_used')
        amountc = ColumnDefn('Amount', 'left', 100, 'amount_string')
        
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
        return ["%s: %s" % (st.combined_category_id, st.name) for st in list(BJCPStyle.select())]
  
    def _getRecipeTypeChoices(self):
        return Recipe.recipe_types
            
    def _getEquipmentChoices(self):
        if EquipmentSet.select().count() == 0:
            return ['Equipment Not Set',]
        else:
            return ['%s' % e.name for e in list(EquipmentSet.select())]

    def BoilSetToEquipment(self, event):
        pass

    def onTextEvent(self, event):
        pass
  
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