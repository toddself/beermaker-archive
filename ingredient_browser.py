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

from db import DataStore
from models import *

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
                    {'widget': wx.BoxSizer, 'flag': wx.ALIGN_RIGHT|wx.TOP|wx.BOTTOM, 'style': wx.HORIZONTAL, 'widgets':
                        ({'widget': wx.Button, 'id': wx.ID_CANCEL, 'style': wx.ALIGN_RIGHT, 'flag': wx.ALL|wx.ALIGN_RIGHT},
                        {'widget': wx.Button, 'id': wx.ID_OK, 'style': wx.ALIGN_RIGHT, 'flag': wx.ALL|wx.ALIGN_RIGHT},)
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