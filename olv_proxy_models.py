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

from models import Grain


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
        
class Grain():
    
    def __init__(self, name=None, origin=None, potential=None, inventory_amt=None):
        self.name = name
        self.origin = origin
        self.potential = potential
        self.inventory_amt = inventory_amt
        
    def setGrain(self, grain_id):
        grain = Grain.get(grain_id)
        inv_grain = list(Inventory.select(Inventory.q.grain=grain))[0]
        self.name = grain.name
        self.origin = grain.origin
        self.potential = grain.potential
        self.inventory_amt = "%s %s" % (inv_grain.amount, Measures.measures[inv_grain.amount_units])
        
        