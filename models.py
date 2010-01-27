from sqlobject import *
from sqlobject.col import pushKey


class SGCol(DecimalCol):
    """ Stores Specific Gravity in a decimal column
    Size is fixed at 4, and the precision is set to 3
    
    ex: 1.045    
    
    """
    
    def __init__(self, **kw):
        pushKey(kw, 'size', 4)
        pushKey(kw, 'precision', 3)
        super(DecimalCol, self).__init__(**kw)

class PercentCol(DecimalCol):
    """Stores percentages in a decimal column
    Size is fixed at 5, and the precision is set to 2.  
    
    *nb* size is fixed at 5 to allow for 100.00%
    
    """
    
    def __init__(self, **kw):
        pushKey(kw, 'size', 5)
        pushKey(kw, 'precision', 2)
        super(DecimalCol, self).__init__(**kw)

class SRMCol(DecimalCol):
    """ Stores the Standard Reference Method color value in a decimal column
    Size is fixed at 5, precision is set to 1
    
    ex: 2.0, 300.5
    
    """

    def __init__(self, **kw):
        pushKey(kw, 'size', 5)
        pushKey(kw, 'precision', 1)
        super(DecimalCol, self).__init__(**kw)

class Measures():
    MG = 0
    GM = 1
    OZ = 2
    LB = 3
    KG = 4
    LB = 5
    ML = 6
    TSP = 7
    TBLS = 8
    CUP = 9
    PT = 10
    QT = 11
    L = 12
    GAL = 13
    ITEMS = 14
    FAHRENHEIT = 15
    CELSIUS = 16
    measures = ['mg','gm','oz','lb','kg','ml','tsp','tbls',
        'cup','pt','qt','l','gal','items', 'f', 'c']

    MIN = 0
    HRS = 1
    DAYS = 2
    WEEKS = 3
    timing_parts = ['min', 'hrs', 'days', 'weeks']


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
    
class Extract(SQLObject):
    name = UnicodeCol(length=64, default=None)
    origin = UnicodeCol(default=None)
    color = SRMCol(default=1.0)
    potential = SGCol(default=1.000)
    max_in_batch = PercentCol(default=0.0)
    add_after_boil = BoolCol(default=False)
    notes = UnicodeCol(default=None)
    supplier = UnicodeCol(default=None, length=128)

class HoppedExtract(Extract, Measures):
    alpha = PercentCol(default=0.0)
    hop_usage = IntCol(default=0)
    hop_usage_unit = IntCol(default=Measures.MIN)
    hop_by_weight = DecimalCol(size=4, precision=2, default=0.0)
    hop_by_weight_unit = IntCol(default=Measures.LB)

class Yeast(SQLObject, Measures):
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
    amount_units = IntCol(default=Measures.ML)
    starter_size = DecimalCol(size=10, precision=10, default=0.0)
    starter_units = IntCol(default=Measures.ML)
    avg_attenuation = PercentCol(default=0.0)
    min_temp = DecimalCol(size=5, precision=5, default=0.0)
    max_temp = DecimalCol(size=5, precision=5, default=0.0)
    temp_units = IntCol(default=Measures.FAHRENHEIT)
    max_reuse = IntCol(default=0)
    best_for = UnicodeCol(default=None)
    notes = UnicodeCol(default=None)
    use_starter = BoolCol(default=False)
    secondary = BoolCol(default=False)

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
        
    
class Misc(SQLObject, Measures):
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
    rec_units = IntCol(default=Measures.OZ)
    batch_size = DecimalCol(size=5, precision=5, default=0.0)
    batch_size_units = IntCol(default=Measures.GAL)
    use_in = IntCol(default=BOIL)
    use_time = IntCol(default=0)
    use_time_units = IntCol(default=Measures.MIN)
    misc_type = IntCol(default=SPICE)

class Mineral(Misc):
    def __init__(self):
        misc_type = Misc.WATER_AGENT

    
class Fining(Misc):
    def __init__(self):
        misc_type = Misc.FINING

class Flavor(Misc):
    def __init__(self):
        misc_type =Misc.FLAVOR
    
class Spice(Misc):
    def __init__(self):
        misc_type = Misc.SPICE


class Herb(Misc):
    def __init__(self):
        misc_type = Misc.HERB

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

class MashTun(SQLObject, Measures):
    volume = DecimalCol(size=5, precision=2, default=0.0)
    volume_unit = IntCol(default=Measures.GAL)
    temp_loss_30 = DecimalCol(size=5, precision=2, default=0.0)
    dead_space = DecimalCol(size=5, precision=2, default=0.0)
    dead_space_unit = IntCol(default=Measures.GAL)
    top_up_water = DecimalCol(size=5, precision=2, default=0.0)
    top_up_water_unit = IntCol(default=Measures.GAL)
    
class BoilKettle(SQLObject, Measures):
    boil_volume = DecimalCol(size=5, precision=2, default=0.0)
    boil_volume_unit = IntCol(default=Measures.GAL)
    evaporation_rate = PercentCol(default=0.0)
    dead_space = DecimalCol(size=5, precision=2, default=0.0)
    dead_space_unit = IntCol(default=Measures.GAL)
    top_up_water = DecimalCol(size=5, precision=2, default=0.0)
    top_up_water_unit = IntCol(default=Measures.GAL)
    final_volume = DecimalCol(size=5, precision=2, default=0.0)
    final_water_unit = IntCol(default=Measures.GAL)
    boil_time = IntCol(default=0)
    boil_time_unit = IntCol(default=Measures.MIN)
    boil_off = DecimalCol(size=3, precision=2, default=0.0)
    boil_off_unit = IntCol(default=Measures.GAL)
    cooling_loss = PercentCol(default=0.0)
    cooling_loss_vol = DecimalCol(size=3, precision=2, default=0.0)
    cooling_loss_unit = IntCol(default=Measures.GAL)
    
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
    
class MashStep(SQLObject, Measures):
    INFUSION = 0
    DECOCTION = 1
    TEMPERATURE = 2
    step_types = ['Infusion', 'Decoction', 'Temperature',]
    
    name = UnicodeCol(length=64, default=None)
    mash_type = IntCol(default=INFUSION)
    fixed_water_addition = DecimalCol(size=5, precision=2, default=0.0)
    fixed_water_addition_unit = IntCol(default=Measures.QT)
    water_grain_ratio = DecimalCol(size=5, precision=2, default=0.0)
    water_ratio_unit = IntCol(default=Measures.QT)
    grain_ratio_unit = IntCol(default=Measures.LB)
    step_temp = DecimalCol(size=4, precision=1, default=0.0)
    step_temp_unit = IntCol(default=Measures.FAHRENHEIT)
    step_time = DecimalCol(size=3, precision=1, default=0.0)
    rise_time = DecimalCol(size=3, precision=1, default=0.0)
    mash_steps = ForeignKey('MashStepOrder')

class MashStepOrder(SQLObject):
    position = IntCol(default=1)
    step = ForeignKey('MashStep')

class Recipe(SQLObject, Measures):
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
    boil_volume_units = IntCol(default=Measures.GAL)
    batch_volume = DecimalCol(size=5, precision=2, default=0)
    batch_volume_units = IntCol(default=Measures.GAL)
    equipment = ForeignKey('EquipmentSet')
    base_boil_on_equipment = BoolCol(default=True)
    grains = MultipleJoin('Grain')
    hops = MultipleJoin('Hop')
    extract = MultipleJoin('Extract')
    fining = MultipleJoin('Fining')
    flavor = MultipleJoin('Flavor')
    herb = MultipleJoin('Herb')
    hoppedextract = MultipleJoin('HoppedExtract')
    mineral = MultipleJoin('Mineral')
    spice = MultipleJoin('Spice')
    water = MultipleJoin('Water')
    yeast = MultipleJoin('Yeast')
    og = SGCol(default=0)
    fg = SGCol(default=0)
    color = SRMCol(default=0)
    ibu = IntCol(default=0)
    fermentation_type = IntCol(default=SINGLE)
    fermentation_stage_1 = IntCol(default=0)
    fermentation_stage_2 = IntCol(default=0)
    fermentation_stage_3 = IntCol(default=0)
    mash = ForeignKey('MashProfile')
    carbonation_type = IntCol(default=FORCED_CO2)
    carbonation_volume = DecimalCol(size=3, precision=1, default=0)
    carbonation_amount = DecimalCol(size=4, precision=2, default=0)

class Batch(SQLObject):
    pass