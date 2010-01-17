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
        

class Measures:
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
	name = UnicodeCol(size=64, default=None)
	description = UnicodeCol(default=None)
    
class Grain(SQLObject):
    name = UnicodeCol(size=64, default=None)
    origin = UnicodeCol(size=128, default=None)
    color = SRMCol(default=1.0)
    potential = SGCol(default=1.000)
    dry_yield_fine_grain = PercentCol(default=0.0)
    coarse_fine_difference = PercentCol(default=0.0)
    moisture = PercentCol(default=0.0)
    diastic_power = DecimalCol(size=4, precision=4, default=0.0)
    max_in_batch = PercentCol(default=100.00)
    protein = PercentCol(default=0.0)
    must_mash = BoolCol(default=False)
    add_after_boil = BoolCol(default=False)
    notes = UnicodeCol(default=None)
    
class Extract(SQLObject):
    name = UnicodeCol(size=64, default=None)
    origin = UnicodeCol(default=None)
    color = SRMCol(default=1.0)
    potential = SGCol(default=1.000)
    dry_yield_fine_grain = PercentCol(default=0.0)
    max_in_batch = PercentCol(default=0.0)
    add_after_boil = BoolCol(default=False)
    notes = UnicodeCol(default=None)

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

    name = UnicodeCol(size=64, default=None)
    lab = UnicodeCol(size=255, default=None)
    ID = UnicodeCol(size=64, default=None)
    yeast_type = IntCol(default=LAGER)
    yeast_form = IntCol(default=LIQUID)
    flocc = IntCol(default=LOW)
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
	
	name = UnicodeCol(size=64, default=None)
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

    name = UnicodeCol(size=64, default=None)
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

class BJCPCategory(SQLObject):
    name = UnicodeCol(length=48, default=None)
    category_id = IntCol(default=None)  
    notes = UnicodeCol()
