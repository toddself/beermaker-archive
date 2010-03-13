# Copyright (C) 2010 Todd Kennedy <todd.kennedy@gmail.com>
# 
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
from datetime import datetime
from decimal import Decimal

from sqlobject import *
from sqlobject.versioning import Versioning

from beerutils import *
from measures import *

class Hop(SQLObject):
    BITTERING = 0 
    AROMA = 1
    BOTH = 2
    LEAF = 0
    PELLET = 1
    PLUG = 2
    hop_types = ['Bittering', 'Aroma', 'Both',]
    hop_forms = ['Leaf', 'Pellet', 'Plug',]
    
    hop_type = IntCol(default=BITTERING)
    hop_form = IntCol(default=LEAF)
    alpha = PercentCol(default=0.0)
    beta = PercentCol(default=0.0)
    stability = PercentCol(default=0.0)
    origin = UnicodeCol(default=None)
    name = UnicodeCol(length=64, default=None)
    description = UnicodeCol(default=None)
    substitutes = UnicodeCol(default=None)
    versions = Versioning()
    
    def _get_inventory(self):
        try:
            inv = list(Inventory.select(Inventory.q.hop == self.id))[0]
        except:
            return 0
        
        return "%s %s" % (inv.amount, Measure.Measure[inv.amount_units])
    
class Grain(SQLObject):
    name = UnicodeCol(length=64, default=None)
    origin = UnicodeCol(length=128, default=None)
    color = SRMCol(default=1.0)
    potential = SGCol(default=1.000)
    dry_yield_fine_grain = PercentCol(default=0.0)
    coarse_fine_difference = PercentCol(default=0.0)
    moisture = PercentCol(default=0.0)
    diastatic_power = DecimalCol(size=4, precision=1, default=0.0)
    max_in_batch = PercentCol(default=100.00)
    protein = PercentCol(default=0.0)
    must_mash = BoolCol(default=False)
    add_after_boil = BoolCol(default=False)
    notes = UnicodeCol(default=None)
    maltster = UnicodeCol(default=None, length=128)
    versions = Versioning()
            
    def _get_inventory(self):
        try:
            inv = list(Inventory.select(Inventory.q.grain == self.id))[0]
        except:
            return 0
        
        return "%s %s" % (inv.amount, Measure.Measure[inv.amount_units])
    
class Extract(SQLObject):
    name = UnicodeCol(length=64, default=None)
    origin = UnicodeCol(default=None)
    color = SRMCol(default=1.0)
    potential = SGCol(default=1.000)
    max_in_batch = PercentCol(default=0.0)
    add_after_boil = BoolCol(default=False)
    notes = UnicodeCol(default=None)
    supplier = UnicodeCol(default=None, length=128)
    versions = Versioning()
    
    def _get_inventory(self):
        try:
            inv = list(Inventory.select(Inventory.q.extract == self.id))[0]
        except:
            return 0
        
        return "%s %s" % (inv.amount, Measure.Measure[inv.amount_units])

class HoppedExtract(Extract, Measure):
    alpha = PercentCol(default=0.0)
    hop_usage = IntCol(default=0)
    hop_usage_unit = IntCol(default=Measure.MIN)
    hop_by_weight = DecimalCol(size=4, precision=2, default=0.0)
    hop_by_weight_unit = IntCol(default=Measure.LB)
    versions = Versioning()
    
    def _get_inventory(self):
        try:
            inv = list(Inventory.select(Inventory.q.hopped_extract == self.id))[0]
        except:
            return 0
        
        return "%s %s" % (inv.amount, Measure.Measure[inv.amount_units])

class Yeast(SQLObject, Measure):
    LAGER = 0
    ALE = 1
    HYBRID = 2
    WINE = 3
    CHAMPAGNE = 4
    CIDER = 5
    MEAD = 6
    SAKE = 7
    yeast_types = ['Lager', 'Ale', 'Hybrid', 'Wine', 'Champagne', 
                   'Cider', 'Mead', 'Sake']
    LIQUID = 0
    DRY = 1
    SLANT = 2
    CULTURE = 3
    yeast_forms = ['Liquid', 'Dry', 'Slant', 'Culture', ]
    LOW = 0
    MEDIUM = 1
    HIGH = 2
    VERY_HIGH = 3
    yeast_flocculations = ['Low','Medium','High','Very High', ]

    name = UnicodeCol(length=64, default=None)
    lab = UnicodeCol(length=255, default=None)
    yeast_id = UnicodeCol(length=64, default=None)
    yeast_type = IntCol(default=LAGER)
    yeast_form = IntCol(default=LIQUID)
    flocc = IntCol(default=LOW)
    amount = DecimalCol(size=5, precision=2, default=0)
    amount_units = IntCol(default=Measure.ML)
    starter_size = DecimalCol(size=10, precision=10, default=0.0)
    starter_units = IntCol(default=Measure.ML)
    avg_attenuation = PercentCol(default=0.0)
    min_temp = DecimalCol(size=5, precision=5, default=0.0)
    max_temp = DecimalCol(size=5, precision=5, default=0.0)
    temp_units = IntCol(default=Measure.FAHRENHEIT)
    max_reuse = IntCol(default=0)
    best_for = UnicodeCol(default=None)
    notes = UnicodeCol(default=None)
    use_starter = BoolCol(default=False)
    secondary = BoolCol(default=False)
    versions = Versioning()
    
    def _get_inventory(self):
        try:
            inv = list(Inventory.select(Inventory.q.yeast == self.id))[0]
        except:
            return 0
        
        return "%s %s" % (inv.amount, Measure.Measure[inv.amount_units])

class Water(SQLObject):
    molecule_types = {'ca': 'Calcium', 'mg': 'Magnesium', 'na': 'Sodium',
        'so4': 'Sulfate', 'cl': 'Chloride', 'hco3': 'Bicarbonate'}
    
    name = UnicodeCol(length=64, default=None)
    pH = DecimalCol(size=8, precision=8, default=0.0)
    ca  = DecimalCol(size=8, precision=8, default=0.0)
    mg = DecimalCol(size=8, precision=8, default=0.0)
    na = DecimalCol(size=8, precision=8, default=0.0)
    so4 = DecimalCol(size=8, precision=8, default=0.0)
    cl = DecimalCol(size=8, precision=8, default=0.0)
    hco3 = DecimalCol(size=8, precision=8, default=0.0)
    notes = UnicodeCol(default=None)
    versions = Versioning()
        
    def _get_inventory(self):
        try:
            inv = list(Inventory.select(Inventory.q.water == self.id))[0]
        except:
            return 0
        
        return "%s %s" % (inv.amount, Measure.Measure[inv.amount_units])        
    
class Misc(SQLObject, Measure):
    SPICE = 0
    FINING = 1
    HERB = 2
    FLAVOR = 3
    OTHER = 4
    WATER_AGENT = 5
    misc_types = ['Spice', 'Fining', 'Herb', 'Flavor', 'Other', 'Water Agent']
    MASH = 0
    BOIL = 1
    PRIMARY = 2
    SECONDARY = 3
    BOTTLING = 4
    misc_use_ins = ['Mash', 'Boil', 'Primary', 'Secondary', 'Bottling']

    name = UnicodeCol(length=64, default=None)
    use_for = UnicodeCol(default=None)
    rec_amount = DecimalCol(size=5, precision=5, default=0.0)
    rec_units = IntCol(default=Measure.OZ)
    batch_size = DecimalCol(size=5, precision=5, default=0.0)
    batch_size_units = IntCol(default=Measure.GAL)
    use_in = IntCol(default=BOIL)
    use_time = IntCol(default=0)
    use_time_units = IntCol(default=Measure.MIN)
    misc_type = IntCol(default=SPICE)
    notes = UnicodeCol(default=None)
    versions = Versioning()

class Mineral(Misc):
    def __init__(self, *args, **kw):
        misc_type = Misc.WATER_AGENT
        Misc.__init__(self, *args, **kw)
        versions = Versioning()
        
    def _get_inventory(self):
        try:
            inv = list(Inventory.select(Inventory.q.mineral == self.id))[0]
        except:
            return 0
        
        return "%s %s" % (inv.amount, Measure.Measure[inv.amount_units])    
    
class Fining(Misc):
    def __init__(self, *args, **kw):
        misc_type = Misc.FINING
        Misc.__init__(self, *args, **kw)

    def _get_inventory(self):
        try:
            inv = list(Inventory.select(Inventory.q.fining == self.id))[0]
        except:
            return 0
        
        return "%s %s" % (inv.amount, Measure.Measure[inv.amount_units])        

class Flavor(Misc):
    def __init__(self, *args, **kw):
        misc_type = Misc.FLAVOR
        Misc.__init__(self, *args, **kw)   

    def _get_inventory(self):
        try:
            inv = list(Inventory.select(Inventory.q.flavor == self.id))[0]
        except:
            return 0
        
        return "%s %s" % (inv.amount, Measure.Measure[inv.amount_units])             
    
class Spice(Misc):
    def __init__(self, *args, **kw):
        misc_type = Misc.SPICE
        Misc.__init__(self, *args, **kw)

    def _get_inventory(self):
        try:
            inv = list(Inventory.select(Inventory.q.spice == self.id))[0]
        except:
            return 0
        
        return "%s %s" % (inv.amount, Measure.Measure[inv.amount_units])

class Herb(Misc):
    def __init__(self, *args, **kw):
        misc_type = Misc.HERB
        Misc.__init__(self, *args, **kw)

    def _get_inventory(self):
        try:
            inv = list(Inventory.select(Inventory.q.herb == self.id))[0]
        except:
            return 0
        
        return "%s %s" % (inv.amount, Measure.Measure[inv.amount_units])        


class BJCPStyle(SQLObject):
    name = UnicodeCol(length=128, default=None)
    beer_type = UnicodeCol(length=5, default=None)
    category = ForeignKey('BJCPCategory')
    subcategory = UnicodeCol(length=1, default=None)
    aroma = UnicodeCol(default=None)
    appearance = UnicodeCol(default=None)
    flavor = UnicodeCol(default=None)
    mouthfeel = UnicodeCol(default=None)
    impression = UnicodeCol(default=None)
    comments = UnicodeCol(default=None)
    examples = UnicodeCol(default=None)
    og_low = SGCol(default=None)
    og_high = SGCol(default=None)
    fg_low = SGCol(default=None)
    fg_high = SGCol(default=None)
    ibu_low = IntCol(default=None)
    ibu_high = IntCol(default=None)
    srm_low = SRMCol(default=None)
    srm_high = SRMCol(default=None)
    abv_low = DecimalCol(size=3, precision=1, default=None)
    abv_high = DecimalCol(size=3, precision=1, default=None)
    versions = Versioning()
    
    def _get_combined_category_id(self):
        return "%s%s" % (self.category.category_id, self.subcategory)
    
    def _get_og_range(self):
        low = self._SO_get_og_low()
        high = self._SO_get_og_high()
        
        if low == 0 and high == 0:
            return "varies"
        else:
            return "%.3f - %.3f" % (low, high)

    def _get_fg_range(self):
        low = self._SO_get_fg_low()
        high = self._SO_get_fg_high()

        if low == 0 and high == 0:
            return "varies"
        else:
            return "%.3f - %.3f" % (low, high)

    def _get_srm_range(self):
        low = self._SO_get_srm_low()
        high = self._SO_get_srm_high()
        
        if low == 0 and high == 0:
            return "varies"
        else:
            return "%.1f - %.1f" % (low, high)

    def _get_abv_range(self):
        low = self._SO_get_abv_low()
        high = self._SO_get_abv_high()
        
        if low == 0 and high == 0:
            return "varies"
        else:
            return "%.2f%% - %.2f%%" % (low, high)
            
    def _get_ibu_range(self):
        low = self._SO_get_ibu_low()
        high = self._SO_get_ibu_high()
        
        if low == 0 and high == 0:
            return "varies"
        else:
            return "%i - %i" % (low, high)


class BJCPCategory(SQLObject):
    name = UnicodeCol(length=48, default=None)
    category_id = IntCol(default=None)  
    notes = UnicodeCol()
    versions = Versioning()

class MashTun(SQLObject, Measure):
    volume = DecimalCol(size=5, precision=2, default=0.0)
    volume_unit = IntCol(default=Measure.GAL)
    temp_loss_30 = DecimalCol(size=5, precision=2, default=0.0)
    dead_space = DecimalCol(size=5, precision=2, default=0.0)
    dead_space_unit = IntCol(default=Measure.GAL)
    top_up_water = DecimalCol(size=5, precision=2, default=0.0)
    top_up_water_unit = IntCol(default=Measure.GAL)
    versions = Versioning()
    
class BoilKettle(SQLObject, Measure):
    boil_volume = DecimalCol(size=5, precision=2, default=0.0)
    boil_volume_unit = IntCol(default=Measure.GAL)
    evaporation_rate = PercentCol(default=0.0)
    dead_space = DecimalCol(size=5, precision=2, default=0.0)
    dead_space_unit = IntCol(default=Measure.GAL)
    top_up_water = DecimalCol(size=5, precision=2, default=0.0)
    top_up_water_unit = IntCol(default=Measure.GAL)
    final_volume = DecimalCol(size=5, precision=2, default=0.0)
    final_water_unit = IntCol(default=Measure.GAL)
    boil_time = IntCol(default=0)
    boil_time_unit = IntCol(default=Measure.MIN)
    boil_off = DecimalCol(size=3, precision=2, default=0.0)
    boil_off_unit = IntCol(default=Measure.GAL)
    cooling_loss = PercentCol(default=0.0)
    cooling_loss_vol = DecimalCol(size=3, precision=2, default=0.0)
    cooling_loss_unit = IntCol(default=Measure.GAL)
    versions = Versioning()
    
class EquipmentSet(SQLObject):
    name = UnicodeCol(length=64, default=None)
    notes = UnicodeCol(default=None)
    mash_tun = ForeignKey('MashTun')
    boil_kettle = ForeignKey('BoilKettle')
    hop_utilization_factor = PercentCol(default=100)
    versions = Versioning()
    
class MashProfile(SQLObject):
    BATCH = 0
    FLY = 1
    sparge_types = ['Batch', 'Fly']
    
    name = UnicodeCol(length=64, default=None)
    pH = DecimalCol(size=2, precision=1, default=5.4)
    sparge_type = IntCol(default=BATCH)
    num_sparges = IntCol(default=1)
    notes = UnicodeCol(default=None)
    versions = Versioning()
    
class MashStep(SQLObject, Measure):
    INFUSION = 0
    DECOCTION = 1
    TEMPERATURE = 2
    step_types = ['Infusion', 'Decoction', 'Temperature',]
    
    name = UnicodeCol(length=64, default=None)
    mash_type = IntCol(default=INFUSION)
    fixed_water_addition = DecimalCol(size=5, precision=2, default=0.0)
    fixed_water_addition_unit = IntCol(default=Measure.QT)
    water_grain_ratio = DecimalCol(size=5, precision=2, default=0.0)
    water_ratio_unit = IntCol(default=Measure.QT)
    grain_ratio_unit = IntCol(default=Measure.LB)
    step_temp = DecimalCol(size=4, precision=1, default=0.0)
    step_temp_unit = IntCol(default=Measure.FAHRENHEIT)
    step_time = DecimalCol(size=3, precision=1, default=0.0)
    rise_time = DecimalCol(size=3, precision=1, default=0.0)
    mash_steps = ForeignKey('MashStepOrder')
    mash = ForeignKey('MashProfile')
    versions = Versioning()

class MashStepOrder(SQLObject):
    position = IntCol(default=1)
    step = ForeignKey('MashStep')
    versions = Versioning()

class Recipe(SQLObject, Measure):
    EXTRACT = 0
    PARTIAL_MASH = 1
    ALL_GRAIN = 2
    recipe_types = ['Extract','Partial Mash','All Grain',]
    
    SINGLE = 0
    DOUBLE = 1
    TRIPLE = 2
    fermentation_types = ['Single Stage', 'Double Stage', 'Triple Stage']
    
    FORCED_CO2 = 0
    TABLE_SUGAR = 1
    CORN_SUGAR = 2
    DRIED_MALT_EXTRACT = 3
    KRAUSEN = 4
    carbonation_types = ['Forced CO2', 'Table Sugar', 'Corn Sugar', 'Dried Malt Extract', 'Krausen',]
    
    name = UnicodeCol(length=64, default=None)
    style = ForeignKey('BJCPStyle', default=None)
    brewer = UnicodeCol(length=255, default=None)
    recipe_type = IntCol(default=EXTRACT)
    boil_volume = DecimalCol(size=5, precision=2, default=0)
    boil_volume_units = IntCol(default=Measure.GAL)
    batch_volume = DecimalCol(size=5, precision=2, default=0)
    batch_volume_units = IntCol(default=Measure.GAL)
    equipment = ForeignKey('EquipmentSet', default=None)
    base_boil_on_equipment = BoolCol(default=True)
    efficiency = PercentCol(default=0)
    og = SGCol(default=0)
    fg = SGCol(default=0)
    color = SRMCol(default=0)
    ibu = IntCol(default=0)
    ingredient = MultipleJoin('RecipeIngredient')
    fermentation_type = IntCol(default=SINGLE)
    fermentation_stage_1_temp = DecimalCol(size=5, precision=2, default=0)
    fermentation_stage_1_temp_units = IntCol(default=Measure.F)
    fermentation_stage_2_temp = DecimalCol(size=5, precision=2, default=0)
    fermentation_stage_2_temp_units = IntCol(default=Measure.F)
    fermentation_stage_3_temp = DecimalCol(size=5, precision=2, default=0)
    fermentation_stage_3_temp_units = IntCol(default=Measure.F)
    fermentation_stage_1_length = IntCol(default=0)
    fermentation_stage_2_length = IntCol(default=0)
    fermentation_stage_3_length = IntCol(default=0)
    fermentation_stage_1_length_units = IntCol(default=0)
    fermentation_stage_2_length_units = IntCol(default=0)
    fermentation_stage_3_length_units = IntCol(default=0)
    mash = ForeignKey('MashProfile', default=None)
    carbonation_type = IntCol(default=FORCED_CO2)
    carbonation_volume = DecimalCol(size=3, precision=1, default=0)
    carbonation_amount = DecimalCol(size=4, precision=2, default=0)
    carbonation_amount_units = IntCol(default=Measure.OZ)
    brewed_on = DateCol(default=datetime.now())
    is_batch = BoolCol(default=False)
    master_recipe = IntCol(default=0)
    grain_total_weight = DecimalCol(size=5, precision=2, default=0)
    hops_total_weight = DecimalCol(size=5, precision=2, default=0)
    versions = Versioning()

    def _set_carbonation_used(self, value):
        if type(value) == type(int()) or type(value) == type(float()):
            value = Measure("%s oz" % value)
        else:
            value = Measure(value)
            
        self.carbonation_amount = value.count
        self.carbonation_amount_units = value.unit

    def _set_primary_fermentation_temp(self, value):
        if type(value) == type(int()) or type(value) == type(float()):
            value = Measure("%s C" % value)
        else:
            value = Measure(value)
            
        self.fermentation_stage_1_temp_units = value.unit
        self.fermentation_stage_1_temp = value.count
    
    def _get_primary_fermentation_temp(self):
        return Measure('%s %s' % (self.fermentation_stage_1_temp, Measure.temperatures[self.fermentation_stage_1_temp_units]))

    def _set_secondary_fermentation_temp(self, value):
        if type(value) == type(int()) or type(value) == type(float()):
            value = Measure("%s C" % value)
        else:
            value = Measure(value)            

        self.fermentation_stage_2_temp_units = value.unit
        self.fermentation_stage_2_temp = value.count

    def _get_secondary_fermentation_temp(self):
        return Measure('%s %s' % (self.fermentation_stage_2_temp, Measure.temperatures[self.fermentation_stage_2_temp_units]))

    def _set_tertiary_fermentation_temp(self, value):
        if type(value) == type(int()) or type(value) == type(float()):
            value = Measure("%s C" % value)
        else:
            value = Measure(value)    

        self.fermentation_stage_3_temp_units = value.unit
        self.fermentation_stage_3_temp = value.count

    def _get_tertiary_fermentation_temp(self):
        return Measure('%s %s' % (self.fermentation_stage_3_temp, Measure.temperatures[self.fermentation_stage_3_temp_units]))

    def _set_primary_fermentation_length(self, value):
        if type(value) == type(int()) or type(value) == type(float()):
            value = Measure("%s days" % value)
        else:
            value = Measure(value)            
        
        self.fermentation_stage_1_length = int(value.count)
        self.fermentation_stage_1_length_units = value.unit
        
    def _get_primary_fermentation_length(self):
        return Measure('%s %s' % (self.fermentation_stage_1_length, Measure.timing_parts[self.fermentation_stage_1_length_units]))
   
    def _set_secondary_fermentation_length(self, value):
        if type(value) == type(int()) or type(value) == type(float()):
            value = Measure("%s days" % value)
        else:
            value = Measure(value)

        self.fermentation_stage_2_length = int(value.count)
        self.fermentation_stage_2_length_units = value.unit

    def _get_secondary_fermentation_length(self):
        return Measure('%s %s' % (self.fermentation_stage_2_length, Measure.timing_parts[self.fermentation_stage_2_length_units]))

    def _set_tertiary_fermentation_length(self, value):
        if type(value) == type(int()) or type(value) == type(float()):
            value = Measure("%s days" % value)
        else:
            value = Measure(value)

        self.fermentation_stage_3_length = int(value.count)
        self.fermentation_stage_3_length_units = value.unit

    def _get_tertiary_fermentation_length(self):
        return Measure('%s %s' % (self.fermentation_stage_3_length, Measure.timing_parts[self.fermentation_stage_3_length_units]))
        
    def _set_boil_volume(self, value):
        if type(value) == type(int()) or type(value) == type(float()):
            value = Measure("%s gal" % value)
        else:
            value = Measure(value)

        self.boil_volume_units = value.unit
        self._SO_set_boil_volume(value.count)
    
    def _get_boil_volume_m(self):
        return Measure('%s %s' % (self._SO_get_boil_volume, Measure.measures[self.boil_volume_units]))

    def _set_batch_volume(self, value):
        if type(value) == type(int()) or type(value) == type(float()):
            value = Measure("%s gal" % value)
        else:
            value = Measure(value)    

        self.batch_volume_units = value.unit
        self._SO_set_batch_volume(value.count)

    def _get_batch_volume_m(self):
        return Measure('%s %s' % (self._SO_get_batch_volume, Measure.measures[self.batch_volume_units]))
    
    def add_to_total_weight(self, ing):
        if ing.ingredient_type.lower() == 'grain':
            new = self.grain_total_weight + ing.amount_m.convert('oz')
            self.grain_total_weight = new
        elif ing.ingredient_type.lower() == 'hop':
            new = self.hop_total_weight + ing.amount_m.convert('oz')
            self.hop_total_weight = new
    
    def _set_master_recipe(self, value):
        if self.is_batch:
            for item in list(self.select()):
                if item.id == value and item.is_batch == False:
                    valid_master_id = True
                
            if valid_master_id:
                self.is_batch = True
                self._SO_set_master_recipe(value)
            else:
                raise BatchIsNotMaster('The master recipe cannot be a batch and it must exist')
        else:
            self._SO_set_master_recipe(0)

class RecipeIngredient(SQLObject):
    sugar_types = ['Grain', 'Extract', 'HoppedExtract']
    hop_types = ['Hop', 'HoppedExtract']
        
    recipe = ForeignKey('Recipe', default=0)
    ingredient_id = IntCol(default=0)
    ingredient_type = UnicodeCol(default=None)
    amount = DecimalCol(size=5, precision=2, default=0)
    amount_units = IntCol(default=Measure.LB)
    percentage  = PercentCol(default=0)
    use_in = IntCol(default=Misc.BOIL)
    time_used = DecimalCol(size=5, precision=2, default=0)
    time_used_units = IntCol(default=Measure.MIN)
    versions = Versioning()
    
    def _get_gravity_units(self):
        if self.ingredient_type in self.sugar_types:
            return gu_from_sg(eval(self.ingredient_type).get(self.ingredient_id).potential)            
        else:
            return 0
    
    def _get_name(self):
        return eval(self.ingredient_type).get(self.ingredient_id).name
    
    def _set_ingredient_id(self, value):
        try:
            self.ingredient_type = value.sqlmeta.table.title()
            self._SO_set_ingredient_id(value.id)
        except AttributeError:
            self.ingredient_type = 'Grain'
            self._SO_set_ingredient_id(value)
    
    def _set_time_used(self, value):
        if type(value) == type(int()):
            value = Measure("%s min" % value)
            
        self.time_used_units = value.unit
        self._SO_set_time_used(value.count)
                
    def _get_time_used_m(self):
        return Measure("%s %s" % (self._SO_get_time_used(), Measure.timing_parts[self.time_used_units]))
    
    def _get_amount_m(self):
        return Measure("%s %s" % (self._SO_get_amount(), Measure.measures[self.amount_units]))
    
    def _set_amount(self, value):
        if type(value) == type(int()):
            value = Measure("%s oz" % value)

        self.amount_units = value.unit
        self._SO_set_amount(value.count)

class Inventory(SQLObject):
    inventory_item_id = IntCol(default=0)
    amount = DecimalCol(size=6, precision=2, default=0)
    amount_units = IntCol(default=Measure.GM)
    purchased_on = DateCol(default=datetime.now())
    purchased_from = UnicodeCol(default=None, length=256)
    price = CurrencyCol(default=0)
    notes = UnicodeCol(default=None)
    inventory_type = UnicodeCol(default=None)
    versions = Versioning()

    def _get_name(self):
        return eval(self.inventory_type).get(self.inventory_item_id).name
    
    def _set_inventory_item_id(self, value):
        self.inventory_type = value.sqlmeta.table.title()
        self._SO_set_inventory_item_id(value.id)

def cloneRecipe(clone, master):
    clone = cloneSQLObject(clone, master)
    for ing in master.ingredient:
        cloned_ing = cloneSQLObject(RecipeIngredient(), ing)
        cloned_ing.recipeID = clone
    return clone

def cloneSQLObject(clone, master):
    for attr in master.__dict__:
        if "_SO_val_" in attr:
            attribute_name = '_'.join(attr.split('_')[3:])
            value = getattr(master, attribute_name)
            setattr(clone, attribute_name, value)   
    return clone

def getHopType(hop_idx):
    try:
        hop_type = Hop.hop_types[hop_idx]
    except:
        hop_type = ''
    return hop_type

def getYeastType(yeast_idx):
    try:
        yeast_type = Yeast.yeast_types[yeast_idx]
    except:
        yeast_type = ''
    return yeast_type

def getYeastFlocc(yeast_idx):
    try:
        yeast_flocc = Yeast.yeast_flocculations[yeast_idx]
    except:
        yeast_flocc = ''
    return yeast_flocc

def getYeastForm(yeast_idx):
    try:
        yeast_form = Yeast.yeast_forms[yeast_idx]
    except:
        yeast_form = ''
    return yeast_form

def getYeastAtten(yeast_att):
    if yeast_att:
        yeast_att = '%.0f%%' % yeast_att
    else:
        yeast_att = ''
    return yeast_att

def getUseIn(use_in):
    if use_in != None:
        use_in_name = Misc.misc_use_ins[use_in]
    else:
        use_in_name = ''
    return use_in_name   