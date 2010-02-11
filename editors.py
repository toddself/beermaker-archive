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
        self.f = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
        self.f.SetPointSize(self.f.GetPointSize()-1)   
        
        # set up if this is a batch or a master recipe
        self.is_batch = False   
    
        
        # set up the main view
        self.main_panel = wx.Panel(self, -1)
        # self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        
        # self.main_sizer.Add(self._basicInfo(), 0, wx.EXPAND|wx.ALL, 3)
        self.main_panel.SetSizer(self.buildLayout(self.main_panel))
        # self.main_panel.SetSizer(self.main_sizer)
                                   
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
                {'widget': wx.BoxSizer, 'flag': wx.ALL|wx.EXPAND, 'proportion': 1, 'style': wx.HORIZONTAL, 'widgets':
                    ({'widget': wx.BoxSizer, 'title': 'Ingredients', 'proportion': 1, 'flag': wx.ALL|wx.EXPAND, 'style': wx.HORIZONTAL, 'widgets':
                        ({'widget': wx.ListCtrl, 'style': wx.LC_REPORT, 'border': 60, 'flag': wx.EXPAND|wx.ALL, 'proportion': 1},)},
                    {'widget': wx.BoxSizer, 'title': 'Details', 'flag': wx.ALL|wx.EXPAND, 'style': wx.HORIZONTAL, 'widgets':
                        ({'widget': wx.ListCtrl, 'style': wx.LC_REPORT},)},                        
                    )
                }, # end third row
                )
                    
    def onTextEvent(self, event):
        pass

    def _basicInfo(self):

          # bottom row sizer: boil volume, batch volume, equipment setup
          bottom_row_ctrls = wx.BoxSizer(wx.HORIZONTAL)
          self.boil_vol_txt = wx.StaticText(self.main_panel, -1, "Boil Volume:")
          self.boil_vol_ctrl = wx.TextCtrl(self.main_panel, -1, "")
          self.boil_vol_units_ctrl = wx.Choice(self.main_panel, -1, size=(-1,-1), choices=self._getLiquidVolumeChoices())
          self.batch_vol_txt = wx.StaticText(self.main_panel, -1, "Batch Volume:")
          self.batch_vol_ctrl = wx.TextCtrl(self.main_panel, -1, "")
          self.batch_vol_units_ctrl = wx.Choice(self.main_panel, -1, choices=self._getLiquidVolumeChoices())
          self.equipment_txt = wx.StaticText(self.main_panel, -1, "Equipment:")
          self.equipment_ctrl = wx.Choice(self.main_panel, -1, choices=self._getEquipmentChoices())
          self.base_boil_volume_ctrl = wx.CheckBox(self.main_panel, -1, "Boil set to equipment")
          
          bottom_row_ctrls.Add(self.boil_vol_txt, 0, self.ST_STYLE, 3)
          bottom_row_ctrls.Add(self.boil_vol_ctrl, 0, self.TC_STYLE, 3)
          bottom_row_ctrls.Add(self.boil_vol_units_ctrl, 0, self.TC_STYLE, 3)
          bottom_row_ctrls.Add(self.batch_vol_txt, 0, self.ST_STYLE, 3)
          bottom_row_ctrls.Add(self.batch_vol_ctrl, 0, self.TC_STYLE, 3)
          bottom_row_ctrls.Add(self.batch_vol_units_ctrl, 0, self.TC_STYLE, 3)
          bottom_row_ctrls.Add(self.equipment_txt, 0, self.ST_STYLE, 3)
          bottom_row_ctrls.Add(self.equipment_ctrl, 0, self.TC_STYLE, 3)
          bottom_row_ctrls.Add(self.base_boil_volume_ctrl, 2, self.ST_STYLE|wx.EXPAND|wx.FIXED_MINSIZE, 3)
          
          basic_info = wx.BoxSizer(wx.VERTICAL)
          basic_info.Add(self._createSectionHeader("Recipe Basics"), 0, wx.ALL|wx.EXPAND|wx.FIXED_MINSIZE, 3)
          basic_info.Add(top_row_ctrls, 0, wx.ALL|wx.EXPAND, 3)
          basic_info.Add(bottom_row_ctrls, 0, wx.ALL|wx.EXPAND, 3)
          
          return basic_info



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
    
    # # top row sizer: name, style, brewed on and brewer name
    # top_row_ctrls = wx.BoxSizer(wx.HORIZONTAL)
    # self.name_txt = wx.StaticText(self.main_panel, -1, "Name:")
    # self.name_txt.SetFont(self.f)
    # self.name_ctrl = wx.TextCtrl(self.main_panel, -1, "")
    # self.name_ctrl.SetFont(self.f)
    # self.style_txt = wx.StaticText(self.main_panel, -1, "Style:")
    # self.style_txt.SetFont(self.f)
    # self.style_ctrl = wx.Choice(self.main_panel, -1, choices=self._getStyleChoices())
    # self.style_ctrl.SetFont(self.f)
    # self.brewer_txt = wx.StaticText(self.main_panel, -1, "Brewer:")
    # self.brewer_txt.SetFont(self.f)
    # self.brewer_ctrl = wx.TextCtrl(self.main_panel, -1, "")
    # self.brewer_ctrl.SetFont(self.f)
    # self.recipe_type_txt = wx.StaticText(self.main_panel, -1, "Type:")
    # self.recipe_type_txt.SetFont(self.f)
    # self.recipe_type_ctrl = wx.Choice(self.main_panel, -1, choices=self._getRecipeTypeChoices())
    # self.recipe_type_ctrl.SetFont(self.f)
    # 
    # top_row_ctrls.Add(self.name_txt, 0, self.ST_STYLE, 3)
    # top_row_ctrls.Add(self.name_ctrl, 1, self.TC_STYLE, 3)
    # top_row_ctrls.Add(self.style_txt, 0, self.ST_STYLE, 3)
    # top_row_ctrls.Add(self.style_ctrl, 1, self.TC_STYLE, 3)
    # if self.is_batch:
    #     self.brewed_on_txt = wx.StaticText(self.main_panel, -1, "Brewed On:")
    #     self.brewed_on_ctrl = wx.DatePickerCtrl(self.main_panel, -1, style=wx.DP_DEFAULT)
    #     top_row_ctrls.Add(self.brewed_on_txt, 0, self.ST_STYLE, 3)
    #     top_row_ctrls.Add(self.brewed_on_ctrl, 0, self.TC_STYLE, 3)
    # top_row_ctrls.Add(self.brewer_txt, 0, self.ST_STYLE, 3)
    # top_row_ctrls.Add(self.brewer_ctrl, 1, self.TC_STYLE, 3)
    # top_row_ctrls.Add(self.recipe_type_txt, 0, self.ST_STYLE, 3)
    # top_row_ctrls.Add(self.recipe_type_ctrl, 1, self.TC_STYLE, 3)
    #    