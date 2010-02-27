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

from datetime import datetime
from decimal import Decimal

from sqlobject import *

from beersql import *
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

class Mineral(Misc):
    def __init__(self, *args, **kw):
        misc_type = Misc.WATER_AGENT
        Misc.__init__(self, *args, **kw)
        
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
    
    def _get_combined_category_id(self):
        return "%s%s" % (self.category.category_id, self.subcategory)
    
    def _get_og_range(self):
        low = self._SO_get_og_low()
        high = self._SO_get_og_high()
        
        if low == 0 and high == 0:
            return "varies"
        else:
            return "%.3f SG - %.3f SG" % (low, high)

    def _get_fg_range(self):
        low = self._SO_get_fg_low()
        high = self._SO_get_fg_high()

        if low == 0 and high == 0:
            return "varies"
        else:
            return "%.3f SG - %.3f SG" % (low, high)

    def _get_srm_range(self):
        low = self._SO_get_srm_low()
        high = self._SO_get_srm_high()
        
        if low == 0 and high == 0:
            return "varies"
        else:
            return "%.1f SRM - %.1f SRM" % (low, high)

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
            return "%i IBU - %i IBU" % (low, high)


class BJCPCategory(SQLObject):
    name = UnicodeCol(length=48, default=None)
    category_id = IntCol(default=None)  
    notes = UnicodeCol()

class MashTun(SQLObject, Measure):
    volume = DecimalCol(size=5, precision=2, default=0.0)
    volume_unit = IntCol(default=Measure.GAL)
    temp_loss_30 = DecimalCol(size=5, precision=2, default=0.0)
    dead_space = DecimalCol(size=5, precision=2, default=0.0)
    dead_space_unit = IntCol(default=Measure.GAL)
    top_up_water = DecimalCol(size=5, precision=2, default=0.0)
    top_up_water_unit = IntCol(default=Measure.GAL)
    
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
    
class EquipmentSet(SQLObject):
    name = UnicodeCol(length=64, default=None)
    notes = UnicodeCol(default=None)
    mash_tun = ForeignKey('MashTun')
    boil_kettle = ForeignKey('BoilKettle')
    hop_utilization_factor = PercentCol(default=100)
    
class MashProfile(SQLObject):
    BATCH = 0
    FLY = 1
    sparge_types = ['Batch', 'Fly']
    
    name = UnicodeCol(length=64, default=None)
    pH = DecimalCol(size=2, precision=1, default=5.4)
    sparge_type = IntCol(default=BATCH)
    num_sparges = IntCol(default=1)
    notes = UnicodeCol(default=None)
    
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

class MashStepOrder(SQLObject):
    position = IntCol(default=1)
    step = ForeignKey('MashStep')

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
    style = ForeignKey('BJCPStyle')
    brewer = UnicodeCol(length=255, default=None)
    recipe_type = IntCol(default=EXTRACT)
    boil_volume = DecimalCol(size=5, precision=2, default=0)
    boil_volume_units = IntCol(default=Measure.GAL)
    batch_volume = DecimalCol(size=5, precision=2, default=0)
    batch_volume_units = IntCol(default=Measure.GAL)
    equipment = ForeignKey('EquipmentSet')
    base_boil_on_equipment = BoolCol(default=True)
    og = SGCol(default=0)
    fg = SGCol(default=0)
    color = SRMCol(default=0)
    ibu = IntCol(default=0)
    ingredient = MultipleJoin('RecipeIngredient')
    fermentation_type = IntCol(default=SINGLE)
    fermentation_stage_1 = IntCol(default=0)
    fermentation_stage_2 = IntCol(default=0)
    fermentation_stage_3 = IntCol(default=0)
    mash = ForeignKey('MashProfile')
    carbonation_type = IntCol(default=FORCED_CO2)
    carbonation_volume = DecimalCol(size=3, precision=1, default=0)
    carbonation_amount = DecimalCol(size=4, precision=2, default=0)
    brewed_on = DateCol(default=datetime.now())
    is_batch = BoolCol(default=False)
    master_recipe = IntCol(default=0)
    
    def _set_master_recipe(self, value):
        valid_master_id = False
        for item in list(self.select()):
            if item.id == value and item.is_batch == False:
                valid_master_id = True
                
        if valid_master_id:
            self.is_batch = True
            self._SO_set_master_recipe(value)
        else:
            raise BatchIsNotMaster('The master recipe cannot be a batch and it must exist')

class RecipeIngredient(SQLObject, Measure):
    recipe = ForeignKey('Recipe')
    ingredient_id = IntCol(default=0)
    ingredient_type = UnicodeCol(default=None)
    amount = DecimalCol(size=5, precision=2, default=0)
    amount_units = IntCol(default=Measure.LB)
    percentage  = PercentCol(default=0)
    use_in = IntCol(default=Misc.BOIL)
    time_used = IntCol(default=0)
    time_used_units = IntCol(default=Measure.MIN)
    
    def _get_name(self):
        return eval(self.ingredient_type).get(self.ingredient_id).name
    
    def _set_ingredient_id(self, value):
        self.ingredient_type = value.sqlmeta.table.title()
        self._SO_set_ingredient_id(value.id)
    
    def _set_time_used(self, value):
        (time, unit) = getTimeFromString(value)
        if time and unit:
            self.time_used_units = unit
            self._SO_set_time_used(time)
                
    def _get_time_used(self):
        return "%s %s" % (self._SO_get_time_used(), Measure.timing_parts[self.time_used_units])
    
    def _get_amount_string(self):
        amt = self._SO_get_amount()
        if amt % 10:
            formatter = "%.2f %s"
        else:
            formatter = "%.0f %s"
            
        return formatter % (amt, Measure.Measure[self.amount_units])
    
    def _set_amount(self, value):
        (amount, unit) = getAmountFromString(value)
        if unit and amount:
            self.amount_units = unit
            self._SO_set_amount(amount)
            

class Inventory(SQLObject):
    inventory_item_id = IntCol(default=0)
    amount = DecimalCol(size=6, precision=2, default=0)
    amount_units = IntCol(default=Measure.GM)
    purchased_on = DateCol(default=datetime.now())
    purchased_from = UnicodeCol(default=None, length=256)
    price = CurrencyCol(default=0)
    notes = UnicodeCol(default=None)
    inventory_type = UnicodeCol(default=None)

    def _get_name(self):
        return eval(self.inventory_type).get(self.inventory_item_id).name
    
    def _set_inventory_item_id(self, value):
        self.inventory_type = value.sqlmeta.table.title()
        self._SO_set_inventory_item_id(value.id)

        
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
    
def getTimeFromString(time_str):
    try:
        (time, time_unit_str) = time_str.split(' ')
    except ValueError:
        raise AmountSetError('You must specify the amount of time as well as the unit of time.  I.E.: 1 min, 2 sec, 3 hrs')
        return (None, None)
    else:
        if time_unit_str.lower() not in Measure.timing_parts:
            time_units = Measure.MIN
        else:
            time_units = Measure.timing_parts.index(time_unit_str)

        try:
            time = int(time)
        except ValueError:
            raise ('The amount of time must be a positive integer and it must preceed the unit. IE: 1 min, 2 sec, 3 hrs')    
            return (None, None)

    return (time, time_units)

def getAmountFromString(amount_str):
    try:
        (amount, amount_unit_str) = amount_str.split(' ')
    except ValueError:
        raise AmountSetError('You must specify the unit of measurement as well as the amount.  I.E.: 12 OZ, 3 GAL')
        return (None, None)
    else:            
        if amount_unit_str.lower() not in Measure.Measure:
            amount_unit = Measure.OZ
        else:
            amount_unit = Measure.Measure.index(amount_unit_str)

        try:
            amount = Decimal(amount)
        except ValueError:
            raise AmountSetError('The amount of the ingredient must preceed the unit. IE: 12 OZ, 3 GAL')
            return (None, None)

    return (amount, amount_unit)