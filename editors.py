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
import wx.cal as cal

import guid
import iconsrc

from db import DataStore
from models import Recipe, Batch, BJCPStyle, BJCPCategory

from base import BaseWindow

class RecipeEditor(wx.Frame, BaseWindow):
    def __init__(self, parent, fid, title, pos=wx.DefaultPosition, size=wx.DefaultSize, style=wx.DEFAULT_FRAME_STYLE):
        wx.Frame.__init__(self, parent, fid, title, pos, size, style)
        
        self.status_bar = self.CreateStatusBar(1,0)
        
        self.tools = self.buildToolbar()
        self.SetSize((1024,800))
        
        self.main_panel = wx.Panel(self, -1)
        self.main_sizer = wx.BoxSizer(wx.VERTICAL)
        self._doLayout(self.main_sizer)
        self.main_panel.SetSizer(self.main_sizer)
        
        # top row elements: name, style, brewed on, brewed by
        self.name_txt = wx.StaticText(self.main_panel, -1, "Name:")
        self.name_ctrl = wx.TextCtrl(self.main_panel, -1, "")
        self.style_txt = wx.StaticText(self.main_panel, -1, "Name:")
        self.style_ctrl = wx.Choice(self.main_panel, -1, choices=self._getStyleChoices())
        self.brewed_on_txt = wx.StaticText(self.main_panel, -1, "Brewed On:")
        self.brewed_on_ctrl = wx.TextCtrl(self.main_panel, -1, "")
        
        top_row = wx.BoxSizer(wx.HORIZONTAL)
        

    def _getStyleChoices(self):
        styles = []
        for style in list(BJCPStyle.select()):
            styles.append("%s: %s" % style.get_combined_category_id, style.name)
        
        return styles
        
    def _showCalendar(self, event):
        # do we have a date?
        if self.brewed_on_ctrl.GetValue != "":
            
        
        # make a new panel for the calendar to live on and generate the calendar widget
        self.calendar_panel = wx.Panel(self.main_panel)
        calendar = cal.CalendarCtrl(calendar_panel, -1. wx.DateTime_Now(), style=CAL_SUNDAY_FIRST|CAL_SHOW_SURROUNDING_WEEKS|CAL_SEQUENTIAL_MONTH_SELECTION)
        self.Bind(wx.EVT_CALENDAR, self._selectDate, id=calendar.GetId())
        
        # make the sizer, add the calendar and set the sizer to the panel
        calendar_sizer = wx.BoxSizer(wx.VERTICAL)
        calendar_sizer.Add(calendar, 0, wx.ALL, 3)
        self.calendar_panel.SetSizer(calendar_panel)
        
        # position and show the calendar
        self.calendar_panel.Raise()
        self.calendar_panel.SetPosition((0,0))
        self.calendar_panel.Show()
    
    def _selectDate(self, event):
        # we've got the date selected, so we'll hide the calendar
        self.calendar_panel.Hide()
        date = event.GetDate()
        dt = str(date).split(' ')
        s = ' '.join(str(s) for s in dt)
        self.brewed_on_ctrl.SetValue(s)
  
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
        reditor = RecipeEditor(None, -1, "")
        self.SetTopWindow(reditor)
        reditor.Show()
        return 1

if __name__ == "__main__":
    R = RE(0)
    R.MainLoop()        
    
    
    # def _setLayout(self):
    #     """
    #     _setLayout returns a tuple containing multiple dictionaries.  these dictionaries are then used
    #     to generate the layout for the window
    #     """
    # 
    #     window = ({
    #     'element': 'sizer',
    #     'format': wx.HORIZONTAL,
    #     'type': 'box',
    #     'elements': (
    #         {'element': 'txt',
    #         'type': 'static',
    #         'value': 'Name:',
    #         'greed': 0,
    #         'padding': 3,
    #         'style': wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL|wx.ADJUST_MINSIZE},
    #         {'element': 'txt',
    #         'type': 'ctrl',
    #         'greed': 1,
    #         'padding': 3,
    #         'style': wx.ALL|wx.EXPAND|wx.ADJUST_MINSIZE|wx.ALIGN_CENTER_VERTICAL
    #         'bind': ((wx.EVT_TEXT, self.textChanged),)},
    #         )
    #     },)
    # 
    # def _doLayout(self, top_sizer):
    #     for widget in self._setLayout():
    #         top_sizer.Add(*self._createLayoutElement(widget))
    # 
    # def _createLayoutElement(self, widget_dict):
    #     for widget in widget_dict:
    #         if widget['element'] == 'sizer':
    #             if widget['type'] == 'box':
    #                 newSizer = wx.BoxSizer(widget['format'])
    #                 newSizer.Add(*self._createLayoutElement(widget))
    #         elif widget['element'] == 'txt':
    #             if widget['type']