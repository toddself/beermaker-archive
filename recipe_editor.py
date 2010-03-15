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

import logging

import wx
from ObjectListView import ObjectListView, ColumnDefn, GroupListView
from sqlobject import SQLObjectNotFound

import guid
import iconsrc
from db import DataStore
from models import *
from beerutils import *
from ingredient_browser import IngredientBrowser
from base import BaseWindow 

class RecipeEditor(wx.Frame, BaseWindow):
    def __init__(self, *args, **kw):   
        
        # lets pull out some stuff we need for the recipe   
        if kw.has_key('recipe_id'):
            recipe_id = kw.pop('recipe_id')
            logging.debug('editing existing recipe: %s' % recipe_id)        
        else:
            recipe_id = 0
        if kw.has_key('batch'):
            batch = True
            logging.debug('this is a batch')
        else:
            batch = False
            logging.debug('this is not a batch')
            
        # since i'm still not so good at this layout shit
        # we're gonna prevent resizing the recipe editor
        if kw.has_key('style'):
            kw['style'] = kw['style'] ^ wx.RESIZE_BORDER
        else:
            kw['style'] = wx.DEFAULT_FRAME_STYLE ^ wx.RESIZE_BORDER
        wx.Frame.__init__(self, *args, **kw)
        self.Centre()
        
        # are we making a new recipe, a new batch, or editing an
        # existing recipe; if existing, populate the fields
        if recipe_id == 0:
            self.recipe = Recipe()
            logging.debug('New recipe')
        else:
            try:
                if batch:
                    self.recipe = cloneRecipe(Recipe(), Recipe.get(recipe_id))
                    self.master_recipe = recipe_id
                    logging.debug('cloning existing recipe %s' % recipe_id)
                else:
                    self.recipe = Recipe.get(recipe_id)
                    logging.debug('editing pre-existing recipe: %s' % recipe_id)
            except SQLObjectNotFound:
                self.recipe= Recipe()
                logging.debug("Thought this was a existing recipe, but it wasn't")
        
        # set up the ui basics
        self.status_bar = self.CreateStatusBar(1,0)
        self.tools = self.buildToolbar()
        
        # set up the main view
        self.main_panel = wx.Panel(self, -1)
        self.main_panel.SetSizer(self.buildLayout(self.main_panel))
        self.setupIngredients()
        self.setupMashes()
        self.updateStyleInfo()
        
        # set up save information
        self.timer_running = False
        self.dirty_data = []
        
        # populate the current recipe if necessary
        # if recipe_id != 0:
        #     self.gatherIngredients() 
        self.setRecipeType()       
        self.setFermentationType()
     
    def layoutData(self):
        return ({'widget': wx.BoxSizer, 'title': 'Recipe Basics', 'flag': wx.ALL|wx.EXPAND, 'style': wx.HORIZONTAL, 'widgets':
                    (
                    {'widget': wx.StaticText, 'label': 'Name:', 'flag': self.ST_STYLE, 'proportion': 0, 'border': 3},
                    {'widget': wx.TextCtrl, 'proportion': 1, 'var': 'recipe_name', 'event': {'event_type': wx.EVT_TEXT, 'method': self.dataChanged}},
                    {'widget': wx.StaticText, 'label': 'Style:', 'flag': self.ST_STYLE},
                    {'widget': wx.Choice, 'size': (200,-1), 'var': 'recipe_style', 'choices': self.getStyleChoices(), 'event': ({'event_type': wx.EVT_CHOICE, 'method': self.dataChanged}, {'event_type': wx.EVT_CHOICE, 'method': self.updateStyleInfo})},
                    {'widget': wx.StaticText, 'label': 'Brewer:', 'flag': self.ST_STYLE},
                    {'widget': wx.TextCtrl, 'var': 'recipe_brewer', 'event': {'event_type': wx.EVT_TEXT, 'method': self.dataChanged}},
                    {'widget': wx.StaticText, 'label': 'Brewed on:', 'display': self.recipe.is_batch, 'flag': self.ST_STYLE},
                    {'widget': wx.DatePickerCtrl, 'var': 'recipe_brewed_on', 'style': wx.DP_DEFAULT, 'display': self.recipe.is_batch, 'event': {'event_type': wx.EVT_DATE_CHANGED, 'method': self.dataChanged}},
                    {'widget': wx.StaticText, 'label': 'Type:', 'flag': self.ST_STYLE},
                    {'widget': wx.Choice, 'var': 'recipe_type', 'choices': self.getRecipeTypeChoices(), 'event': ({'event_type': wx.EVT_CHOICE, 'method': self.dataChanged}, {'event_type': wx.EVT_CHOICE, 'method': self.setRecipeType})},
                    )
                }, # end top row
                {'widget': wx.BoxSizer, 'flag': wx.ALL|wx.EXPAND, 'style': wx.HORIZONTAL, 'widgets':
                    (
                    {'widget': wx.StaticText, 'label': 'Boil Volume:', 'flag': self.ST_STYLE},
                    {'widget': wx.TextCtrl, 'var': 'recipe_boil_volume','event': {'event_type': wx.EVT_TEXT, 'method': self.dataChanged}},
                    {'widget': wx.StaticText, 'label': 'Batch Volume:', 'flag': self.ST_STYLE},
                    {'widget': wx.TextCtrl, 'value': '5 gal', 'var': 'recipe_batch_volume', 'event': {'event_type': wx.EVT_TEXT, 'method': self.dataChanged}},
                    {'widget': wx.StaticText, 'label': 'Equipment:', 'flag': self.ST_STYLE},
                    {'widget': wx.Choice, 'var': 'recipe_equipment', 'choices': self.getEquipmentChoices(), 'event': {'event_type': wx.EVT_CHOICE, 'method': self.dataChanged}},
                    {'widget': wx.CheckBox, 'var': 'recipe_boil_set_to_equipment', 'proportion': 1, 'label': 'Boil volume set to equipment', 'event': {'event_type': wx.EVT_CHECKBOX, 'method': self.dataChanged}},
                    {'widget': wx.Button, 'label': 'Efficiency:', 'event': {'event_type': wx.EVT_BUTTON, 'method': self.viewEfficiency}},
                    {'widget': wx.TextCtrl, 'size': (50, -1), 'var': 'recipe_efficiency', 'value': '75', 'event':({'event_type': wx.EVT_TEXT, 'method': self.dataChanged}, {'event_type': wx.EVT_TEXT, 'method': self.updateRecipeStats})},
                    {'widget': wx.StaticText, 'label': '%', 'flag': wx.ALL}
                    )
                }, # end second row
                {'widget': wx.BoxSizer, 'title': 'Ingredients', 'flag': wx.ALL|wx.EXPAND, 'proportion': 1, 'style': wx.VERTICAL, 'widgets':
                    ({'widget': ObjectListView, 'var': 'ingredients_ctrl', 'style': wx.LC_REPORT, 'cellEditMode': ObjectListView.CELLEDIT_DOUBLECLICK, 'flag': wx.EXPAND|wx.ALL, 'proportion': 1, 'event': ({'event_type': wx.EVT_LIST_INSERT_ITEM, 'method': self.updateRecipeStats}, {'event_type': wx.EVT_LIST_DELETE_ITEM, 'method': self.updateRecipeStats})},
                    {'widget': wx.BoxSizer, 'flag': wx.ALL|wx.EXPAND, 'style': wx.HORIZONTAL, 'widgets':
                        (
                        {'widget': wx.Button, 'label': 'Add Grain', 'event': {'event_type': wx.EVT_BUTTON, 'method': self.grainAdd}},
                        {'widget': wx.Button, 'label': 'Add Hops', 'event': {'event_type': wx.EVT_BUTTON, 'method': self.hopsAdd}},
                        {'widget': wx.Button, 'label': 'Add Yeast', 'event': {'event_type': wx.EVT_BUTTON, 'method': self.yeastAdd}},
                        {'widget': wx.Button, 'label': 'Add Misc', 'event': {'event_type': wx.EVT_BUTTON, 'method': self.miscAdd}}, 
                        {'widget': wx.Button, 'label': 'Delete Item', 'event': {'event_type': wx.EVT_BUTTON, 'method': self.inventoryDelete}},                 
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
                        {'widget': wx.TextCtrl, 'var': 'recipe_og', 'editable': False},
                        {'widget': wx.StaticText, 'label': 'FG:' , 'style': self.ST_STYLE},
                        {'widget': wx.TextCtrl, 'var': 'recipe_fg',  'editable': False},
                        {'widget': wx.StaticText, 'label': 'Color:' , 'style': self.ST_STYLE},
                        {'widget': wx.TextCtrl, 'var': 'recipe_srm',  'editable': False},
                        {'widget': wx.StaticText, 'label': 'ABV:' , 'style': self.ST_STYLE},
                        {'widget': wx.TextCtrl, 'var': 'recipe_abv', 'editable': False},
                        {'widget': wx.StaticText, 'label': 'IBU:' , 'style': self.ST_STYLE},
                        {'widget': wx.TextCtrl, 'var': 'recipe_ibu',  'editable': False},                        
                        {'widget': wx.StaticText, 'label': 'Bitterness Ratio:' , 'style': self.ST_STYLE},
                        {'widget': wx.TextCtrl, 'var': 'recipe_br',  'editable': False},
                        )},
                    )
                }, # end fourth row  
                {'widget': wx.BoxSizer, 'style': wx.HORIZONTAL, 'proportion': 0, 'flag': wx.ALL|wx.EXPAND, 'widgets':
                    ({'widget': wx.BoxSizer, 'title': 'Mash', 'proportion': 1, 'flag': wx.ALL|wx.EXPAND, 'style': wx.VERTICAL, 'widgets':
                        ({'widget': wx.BoxSizer, 'style': wx.HORIZONTAL, 'proportion': 0, 'flag': wx.ALL|wx.EXPAND, 'widgets':
                            ({'widget': wx.StaticText, 'label': 'Mash Type:', 'style': self.ST_STYLE},
                            {'widget': wx.Choice, 'var': 'mash_choice', 'choices': self.getMashChoices(), 'event': {'event_type': wx.EVT_CHOICE, 'method': self.dataChanged}},)},
                        {'widget': ObjectListView, 'var': 'mash_ctrl', 'style': wx.LC_REPORT|wx.EXPAND, 'cellEditMode': ObjectListView.CELLEDIT_DOUBLECLICK, 'flag': wx.EXPAND|wx.ALL, 'proportion': 1},
                        {'widget': wx.BoxSizer, 'style': wx.HORIZONTAL, 'widgets':
                            ({'widget': wx.Button, 'var': 'mash_add', 'id': wx.ID_ADD, 'event': {'event_type': wx.EVT_BUTTON, 'method': self.mashAdd}},
                            {'widget': wx.Button, 'var': 'mash_delete', 'id': wx.ID_DELETE, 'event': {'event_type': wx.EVT_BUTTON, 'method': self.mashDelete}},
                            {'widget': wx.Button, 'var': 'mash_up', 'id': wx.ID_UP, 'event': {'event_type': wx.EVT_BUTTON, 'method': self.mashUp}},
                            {'widget': wx.Button, 'var': 'mash_down', 'id': wx.ID_DOWN, 'event': {'event_type': wx.EVT_BUTTON, 'method': self.mashDown}})},)},
                    {'widget': wx.BoxSizer, 'style': wx.VERTICAL, 'title': 'Fermentation', 'border': 3, 'flag': wx.ALL, 'widgets':
                        ({'widget': wx.BoxSizer, 'style': wx.HORIZONTAL, 'flag': wx.ALIGN_CENTER, 'widgets':
                        ({'widget': wx.StaticText, 'label': 'Stages:', 'style': self.ST_STYLE},
                        {'widget': wx.Choice, 'var': 'fermentation_type', 'choices': self.getFermentationStageChoices(), 'event': ({'event_type': wx.EVT_CHOICE, 'method': self.dataChanged}, {'event_type': wx.EVT_CHOICE, 'method': self.setFermentationType})},)},
                        {'widget': wx.FlexGridSizer, 'vgap': 3, 'hgap': 3, 'rows': 4, 'cols': 4, 'widgets':
                            ({'widget': wx.StaticText, 'label': 'Primary:', 'style': self.ST_STYLE},
                            {'widget': wx.TextCtrl, 'var': 'primary_length', 'event': {'event_type': wx.EVT_TEXT, 'method': self.dataChanged}},
                            {'widget': wx.StaticText, 'label': 'Temperature:', 'style': self.ST_STYLE},
                            {'widget': wx.TextCtrl, 'var': 'primary_temp', 'event': {'event_type': wx.EVT_TEXT, 'method': self.dataChanged}},
                            {'widget': wx.StaticText, 'label': 'Secondard:', 'style': self.ST_STYLE},
                            {'widget': wx.TextCtrl, 'var': 'secondary_length', 'event': {'event_type': wx.EVT_TEXT, 'method': self.dataChanged}},
                            {'widget': wx.StaticText, 'label': 'Temperature:', 'style': self.ST_STYLE},
                            {'widget': wx.TextCtrl, 'var': 'secondary_temp', 'event': {'event_type': wx.EVT_TEXT, 'method': self.dataChanged}},
                            {'widget': wx.StaticText, 'label': 'Tertiary:', 'style': self.ST_STYLE},
                            {'widget': wx.TextCtrl, 'var': 'tertiary_length', 'event': {'event_type': wx.EVT_TEXT, 'method': self.dataChanged}},
                            {'widget': wx.StaticText, 'label': 'Temperature:', 'style': self.ST_STYLE},
                            {'widget': wx.TextCtrl, 'var': 'tertiary_temp', 'event': {'event_type': wx.EVT_TEXT, 'method': self.dataChanged}},)},)},
                    {'widget': wx.BoxSizer, 'style': wx.VERTICAL, 'title': 'Carbonation', 'border': 3, 'flag': wx.ALL|wx.EXPAND, 'widgets':
                        ({'widget': wx.FlexGridSizer, 'vgap': 3, 'hgap': 3, 'rows': 2, 'cols': 4, 'widgets':
                            ({'widget': wx.StaticText, 'label': 'Type:', 'style': self.ST_STYLE},
                            {'widget': wx.Choice, 'var': 'carbonation_type', 'choices': self.getCarbonationTypeChoices(), 'event': {'event_type': wx.EVT_CHOICE, 'method': self.dataChanged}},
                            {'widget': wx.StaticText, 'label': 'Style:', 'style': self.ST_STYLE},
                            {'widget': wx.TextCtrl, 'var': 'carbonation_style', 'editable': False, 'event': {'event_type': wx.EVT_TEXT, 'method': self.dataChanged}},
                            {'widget': wx.StaticText, 'label': 'Volumes:', 'style': self.ST_STYLE},
                            {'widget': wx.TextCtrl, 'var': 'carbonation_volumes', 'editable': False, 'event': {'event_type': wx.EVT_TEXT, 'method': self.dataChanged}},
                            {'widget': wx.StaticText, 'label': 'Amount Needed:', 'style': self.ST_STYLE},
                            {'widget': wx.TextCtrl, 'var': 'carbonation_needed', 'editable': False, 'event': {'event_type': wx.EVT_TEXT, 'method': self.dataChanged}},                            
                            {'widget': wx.StaticText, 'label': 'Amount Used:', 'style': self.ST_STYLE},
                            {'widget': wx.TextCtrl, 'var': 'carbonation_used', 'event': {'event_type': wx.EVT_TEXT, 'method': self.dataChanged}},
                            )},
                        )
                    }
                            
                    )                
                }, # end fifth row              
                )

    def toggleMashSection(self, toggle):
        logging.debug('Setting mash editability to: %s' % toggle)
        self.toggleWidget(self.mash_choice, toggle)
        self.toggleWidget(self.mash_ctrl, toggle)
        self.toggleWidget(self.mash_add, toggle)
        self.toggleWidget(self.mash_delete, toggle)
        self.toggleWidget(self.mash_up, toggle)
        self.toggleWidget(self.mash_down, toggle)
        
    def toggleFermentationSection(self, number):
        logging.debug('in toggle fermentation with %s' % number)
        if number == 3:
            logging.debug('we have a triple stage fermentation.  you had better be beechwood aging this bitch')
            self.toggleWidget(self.tertiary_length, True)
            self.toggleWidget(self.tertiary_length, True)
            self.toggleWidget(self.tertiary_temp, True)
            self.toggleWidget(self.secondary_length, True)
            self.toggleWidget(self.secondary_temp, True)
        elif number == 2:
            logging.debug('we have double stage fermentation, setting secondary to true, teritary to false')       
            self.toggleWidget(self.tertiary_length, False)
            self.toggleWidget(self.tertiary_temp, False)
            self.toggleWidget(self.secondary_length, True)
            self.toggleWidget(self.secondary_temp, True)
        elif number == 1:
            logging.debug('we have single stage fermentation, setting everything to false')
            self.toggleWidget(self.tertiary_length, False)
            self.toggleWidget(self.tertiary_temp, False)
            self.toggleWidget(self.secondary_length, False)
            self.toggleWidget(self.secondary_temp, False)

    def setFermentationType(self, event=None):
        number = self.fermentation_type.GetSelection() + 1
        logging.debug('Setting fermentation number: %s' % number)
        self.toggleFermentationSection(number)

        if event:
            event.Skip()
                
    def setRecipeType(self, event=None):
        set_type = self.recipe_type.GetSelection()
        logging.debug('Recipe type set to: %s' % set_type)
        
        if set_type == self.recipe.EXTRACT:
            self.toggleMashSection(False)
        else:
            self.toggleMashSection(True)

        if event:           
            event.Skip()

    def grainAdd(self, event):
        self.inventoryAdd(event, 'Grain')
        event.Skip()
        
    def hopsAdd(self, event):
        self.inventoryAdd(event, 'Hop')
        event.Skip()

    def yeastAdd(self, event):
        self.inventoryAdd(event, 'Yeast')
        event.Skip()

    def miscAdd(self, event):
        self.inventoryAdd(event, 'Misc')
        event.Skip()
        
    def inventoryAdd(self, event, ingtype=None):            
        logging.debug('launching the ingredient browser, seeding with: %s' % ingtype)
        inventory = IngredientBrowser(self, -1, "Ingredient Browser", pos=(50,50), size=(800,600), ingtype=ingtype)
        inventory.CentreOnParent()
        if inventory.ShowModal() == wx.ID_OK:

            ing = RecipeIngredient(recipe=self.recipe.id, 
                ingredient_id=inventory.ingredients_ctrl.GetSelectedObject(), 
                amount=Measure(inventory.amount_ctrl.GetValue()), 
                use_in=inventory.use_choices.GetCurrentSelection(), 
                time_used=Measure(inventory.time_used_ctrl.GetValue()))
                
            self.recipe.add_to_total_weight(ing)
            self.ingredients_ctrl.AddObject(ing)
            self.updateRecipePercentage()
            self.ingredients_ctrl.AutoSizeColumns()
            
        inventory.Destroy()
        event.Skip()

    def updateRecipePercentage(self):
        for ingredient in self.ingredients_ctrl.GetObjects():
            ingredient.percentage = self.getPercentOfTotalBill(ingredient.amount_m, ingredient.ingredient_type)
            self.ingredients_ctrl.RefreshObject(ingredient)

    def getPercentOfTotalBill(self, new_amount, ingredient_type):
        total_ingredient = getattr(self.recipe, '%s_total_weight' % ingredient_type.lower())
        return (new_amount.convert('oz') / total_ingredient) * Decimal('100.0')

    def inventoryDelete(self, event):
        ingredient = self.ingredients_ctrl.GetSelectedObject()
        self.recipe.remove_from_total_weight(ingredient.amount.convert('oz'), ingredient.ingredient_type.lower())
        self.ingredients_ctrl.RemoveObject(ingredient)
        self.updateRecipePercentage()
        event.Skip()
        
    def updateRecipeStats(self, event):
        logging.debug('updating recipe stats')
        potential_in_gu = 0
        bitterness = 0
        color = 0
        for ingredient in self.ingredients_ctrl.GetObjects():
            if ingredient.ingredient_type in ingredient.sugar_types:
                # gravity stuff
                ingredient_potential = ingredient.gravity_units * ingredient.amount_m.convert('lbs')
                logging.debug('potential for %s: %s' % (ingredient.name, ingredient_potential))
                if ingredient.ingredient_type == 'Grain':
                    eff = Decimal("%s" % self.recipe_efficiency.GetValue())
                    logging.debug('got some grain here so we need to calculate an efficiency: %s' % eff)
                    ingredient_potential = ingredient_potential * (eff / Decimal('100.0'))
                    logging.debug('the ingredient is only giving us %s gravity units' % ingredient_potential)
                batch_volume = Measure(self.recipe_batch_volume.GetValue()).convert('gal')
                logging.debug('now we dilute this with the batch volume in gallons: %s' % batch_volume)
                diluted_potential = ingredient_potential / batch_volume
                logging.debug('which gives us %s g.u. in this batch' % diluted_potential)
                potential_in_gu = potential_in_gu + diluted_potential
                logging.debug('total potential after adding: %s' % potential_in_gu)
                
                # color stuff
                logging.debug('color calculations')
                mcu = ingredient.amount_m.convert('lbs') * ingredient.srm / batch_volume
                logging.debug('mcu for %s: %s' % (ingredient.name, mcu))
                color = color + srm_from_mcu(mcu)
                logging.debug('srm after addition: %s' % color)

            elif ingredient.ingredient_type in ingredient.hop_types:
                logging.debug('going to get bitterness')
                bitterness = bitterness + ingredient.ibu
        
        final_sg = sg_from_gu(potential_in_gu)
        logging.debug('final gravity: %s' % final_sg)
        self.recipe_og.SetValue("%.3f" % final_sg)
        self.recipe_ibu.SetValue("%s" % bitterness)
        self.recipe_srm.SetValue("%.1f" % color)
        pass
        
    def getStyleFromSelection(self):
        (style_id, style_name) = self.style_choices[self.recipe_style.GetCurrentSelection()].split(":")
        style = BJCPStyle.select(BJCPStyle.q.name==style_name.strip()).getOne()
        return style
        
    def getEquipmentFromSelection(self):
        try:
            equipment = EquipmentSet.select(EquipmentSet.q.name==self.equipment_choices[self.recipe_equipment.GetCurrentSelection()].strip()).getOne()
        except:
            equipment = None
        return equipment
    
    def getMashFromSelection(self):
        try:
            mash = MashProfile.select(MashProfile.q.name==self.mash_profiles[self.recipe_mash_choice.GetCurrentSelection()].strip()).getOne()
        except:
            mash = None
        return mash
        
    def updateStyleInfo(self, event=None):
        style = self.getStyleFromSelection()
        self.style_og.SetValue(style.og_range)
        self.style_fg.SetValue(style.fg_range)
        self.style_srm.SetValue(style.srm_range)
        self.style_abv.SetValue(style.abv_range)
        self.style_ibu.SetValue(style.ibu_range)
        br_high = calculateBitternessRatio(style.og_high, style.ibu_high)
        br_low = calculateBitternessRatio(style.og_low, style.ibu_low)
        self.style_br.SetValue("%s - %s" % (br_high, br_low))
        
        if event:
            event.Skip()

    def mashAdd(self, event):
        """docstring for mashAdd"""
        pass
    
    def mashDelete(self, event):
        """docstring for mashDelete"""
        pass
        
    def mashUp(self, event):
        """docstring for mashUp"""
        pass
        
    def mashDown(self, event):
        pass
        
    def getCarbonationTypeChoices(self):
        return Recipe.carbonation_types

    def getFermentationStageChoices(self):
        return Recipe.fermentation_types

    def getMashChoices(self):
        if MashProfile.select().count() == 0:
            self.mash_profiles =  ['No Mashes Defined',]
        else:
            self.mash_profiles = ['%s' % m.name for m in list(MashProfile.select())]
        return self.mash_profiles
                
    def gatherIngredients(self):
        self.recipe_name.SetValue(self.recipe.name) 
        # self.

    def setupIngredients(self):
        namec = ColumnDefn('Ingredient', 'left', 200, 'name', minimumWidth=200, isSpaceFilling=True)
        typec= ColumnDefn('Type', 'left', 100, 'ingredient_type')
        use_inc = ColumnDefn('Use', 'left', 100, 'use_in', stringConverter=getUseIn)
        percentc = ColumnDefn('%', 'left', 100, 'percentage', stringConverter="%.2f")
        timec = ColumnDefn('Time', 'left', 100, 'time_used_m', stringConverter="%s")
        amountc = ColumnDefn('Amount', 'left', 100, 'amount_m', stringConverter="%s")

        namec.freeSpaceProportion = 2
        
        self.ingredients_ctrl.oddRowsBackColor = wx.WHITE        
        self.ingredients_ctrl.SetColumns([namec, typec, amountc, use_inc, percentc, timec])

    def setupMashes(self):
        namec = ColumnDefn('Name', 'left', -1, 'name', isSpaceFilling=True)
        startc = ColumnDefn('Start Temp', 'left', 80, 'start_temp')
        endc = ColumnDefn('End Temp', 'left', 80, 'end_temp')
        timec = ColumnDefn('Time', 'left', 80, 'time')
        
        self.mash_ctrl.oddRowsBackColor = wx.WHITE
        self.mash_ctrl.SetColumns([namec, startc, endc, timec])
                    
    def getStyleChoices(self):
        self.style_choices =  ["%s: %s" % (st.combined_category_id, st.name) for st in list(BJCPStyle.select())]
        return self.style_choices
  
    def getRecipeTypeChoices(self):
        return Recipe.recipe_types
            
    def getEquipmentChoices(self):
        if EquipmentSet.select().count() == 0:
            self.equipment_choices =  ['Equipment Not Set',]
        else:
            self.equpiment_choices =  ['%s' % e.name for e in list(EquipmentSet.select())]
        return self.equipment_choices

    def dataChanged(self, event):
        # are we gonna save?
        # we need to make list of things we've "dirtied"
        # with unsaved data
        self.dirty_data.append(event.GetId())
        
        # if the timer is running, reset.  this makes it so we're
        # not saving while you're actually editing
        if self.timer_running:
            self.save_timer.Restart()
        else:
            self.save_timer = wx.FutureCall(1500, self.saveRecipe)
            self.timer_running = True
            
        # we need to make sure that any other method bound to this object gets called
        event.Skip()
  
    def saveRecipe(self):
        # ugh.  there's probably some pythonic way to do this better
        # that i'm just not fucking remembering.  but who doesn't love
        # a massively long if/elif/else statement!
        
        logging.debug('in the save function')
        
        try:
            self.recipe_brewed_on_id
        except:
            self.recipe_brewed_on_id = False
        
        for data in list(set(self.dirty_data)):
            if data == self.recipe_name_id:
                logging.debug('saving name: %s' % self.recipe_name.GetValue())
                self.recipe.name = self.recipe_name.GetValue()
                logging.debug('new value: %s' % self.recipe.name)
            elif data == self.recipe_style_id:
                logging.debug('saving recipe style: %s' % self.getStyleFromSelection())
                self.recipe.style = self.getStyleFromSelection()
                logging.debug('new value: %s' % self.recipe.style)
            elif data == self.recipe_brewer_id:
                logging.debug('saving brewer: %s' % self.recipe_brewer.GetValue())
                self.recipe.brewer = self.recipe_brewer.GetValue()
                logging.debug('new value: %s' % self.recipe.brewer)
            elif data == self.recipe_brewed_on_id:
                logging.debug('saving brewed on: %s' % self.recipe_brewed_on.GetValue())
                self.recipe.brewed_on = self.recipe_brewed_on.GetValue()
                logging.debug('new value: %s' % self.recipe.brewed_on)
            elif data == self.recipe_type_id:
                logging.debug('saving recipe type: %s' % self.recipe_type.GetCurrentSelection())
                self.recipe.recipe_type = self.recipe_type.GetCurrentSelection()
                logging.debug('new value: %s' % self.recipe.recipe_type)
            elif data == self.recipe_boil_volume_id:
                logging.debug('saving boil volume: %s' % self.recipe_boil_volume.GetValue())
                self.recipe.boil_volume = self.recipe_boil_volume.GetValue()
                logging.debug('new value: %s' % self.recipe.boil_volume)
            elif data == self.recipe_batch_volume_id:
                logging.debug('saving batch volume: %s' % self.recipe_batch_volume.GetValue())
                self.recipe.batch_volume = self.recipe_batch_volume.GetValue()
                logging.debug('new value: %s' % self.recipe.batch_volume)
            elif data == self.recipe_equipment_id:
                logging.debug('saving recipe equipment: %s' % self.getEquipmentFromSelection())
                self.recipe.equipment = self.getEquipmentFromSelection()
                logging.debug('new value: %s' % self.recipe.equipment)
            elif data == self.recipe_boil_set_to_equipment_id:
                logging.debug('saving recipe boil set to equipment: %s' % self.recipe_boil_set_to_equipment.GetValue())
                self.recipe.boil_set_to_equipment = self.recipe_boil_set_to_equipment.GetValue()
                logging.debug('new value: %s' % self.recipe.boil_set_to_equipment)
            elif data == self.recipe_efficiency_id:
                logging.debug('saving efficiency: %s' % self.recipe_efficiency.GetValue())
                self.recipe.efficiency = self.recipe_efficiency.GetValue()
                logging.debug('new value: %s' % self.recipe.efficiency)
            elif data == self.mash_choice_id:
                logging.debug('saving mash choice: %s' % self.getMashFromSelection())
                self.recipe.mash = self.getMashFromSelection()
                logging.debug('new value: %s' % self.recipe.mash)
            elif data == self.fermentation_type_id:
                logging.debug('saving fermentation type: %s' % self.fermentation_type.GetCurrentSelection())
                self.recipe.fermentation_type = self.fermentation_type.GetCurrentSelection()
                logging.debug('new value: %s' % self.recipe.fermentation_type)
            elif data == self.primary_length_id:
                logging.debug('saving primary length: %s' % self.primary_length.GetValue())
                self.recipe.primary_fermentation_length = self.primary_length.GetValue()
                logging.debug('new value: %s' % self.recipe.primary_fermentation_length)
            elif data == self.primary_temp_id:
                logging.debug('saving primary temp: %s' % self.primary_temp.GetValue())
                self.recipe.primary_fermentation_temp = self.primary_temp.GetValue()
                logging.debug('new value: %s' % self.recipe.primary_fermentation_temp)
            elif data == self.secondary_length_id:
                logging.debug('saving secondary length: %s' % self.secondary_length.GetValue())
                self.recipe.secondary_fermentation_length = self.secondary_length.GetValue()
                logging.debug('new value: %s' % self.recipe.secondary_fermentation_length)
            elif data == self.secondary_temp_id:
                logging.debug('saving 2nd temp: %s' % self.secondary_temp.GetValue())
                self.recipe.secondary_fermentation_temp = self.secondary_temp.GetValue()
                logging.debug('new value: %s' % self.recipe.secondary_fermentation_temp)
            elif data == self.tertiary_length_id:
                logging.debug('saving 3rd len: %s' % self.tertiary_length.GetValue())
                self.recipe.tertiary_fermentation_length = self.tertiary_length.GetValue()
                logging.debug('new value: %s' % self.recipe.tertiary_fermentation_length)
            elif data == self.tertiary_temp_id:
                logging.debug('saving 3rd temp: %s' % self.tertiary_temp.GetValue())
                self.recipe.tertiary_fermentation_temp = self.tertiary_temp.GetValue()
                logging.debug('new value: %s' % self.recipe.tertiary_fermentation_temp)
            elif data == self.carbonation_type_id:
                logging.debug('saving carb type: %s' % self.carbonation_type.GetCurrentSelection())
                self.recipe.carbonation_type = self.carbonation_type.GetCurrentSelection()
                logging.debug('new value: %s' % self.recipe.carbonation_type)
            elif data == self.carbonation_volumes_id: 
                logging.debug('saving carb vol: %s' % self.carbonation_volumes.GetValue())
                self.recipe.carbonation_volume = self.carbonation_volumes.GetValue()
                logging.debug('new value: %s' % self.recipe.carbonation_volume)
            elif data == self.carbonation_used_id:
                logging.debug('saving carb used: %s' % self.carbonation_used.GetValue())
                self.recipe.carbonation_used = self.carbonation_used.GetValue()
                logging.debug('new value: %s' % self.recipe.carbonation_amount)

        self.dirty_data = []
  
    def newRecipe(self):
        pass

    def newBatch(self):
        pass

    def viewEfficiency(self, event):
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
    LOG_FILENAME = '/tmp/editor.out'
    logging.basicConfig(filename=LOG_FILENAME,level=logging.DEBUG)
    
    R = RE(0)
    R.MainLoop()