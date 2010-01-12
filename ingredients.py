from datetime import datetime

class Ingredient:
	mg = 0
	gm = 1
	oz = 2
	lb = 3
	kg = 4
	lb = 5
	ml = 6
	tsp = 7
	tbls = 8
	cup = 9
	pt = 10
	qt = 11
	l = 12
	gal = 13
	items = 14
	ingredient_measures = ['mg','gm','oz','lb','kg','ml','tsp','tbls',
		'cup','pt','qt','l','gal','items']

	MIN = 0
	HRS = 1
	DAYS = 2
	WEEKS = 3
	timing_parts = ['min', 'hrs', 'days', 'weeks']

	def __init__(self):
		pass
    
class Hop(Ingredient):
	BITTERING = 0
	AROMA = 1
	BOTH = 2
	LEAF = 0
	PELLET = 1
	PLUG = 2
	hop_types = ['Bittering', 'Aroma', 'Both',]
	hop_forms = ['Leaf', 'Pellet', 'Plug']

	def __init__(self, hop_type = None, hop_form = None, alpha = 0.0, 
		beta = 0.0 , stability = 0.0, origin = None, name = None, 
		description = None):
		
		self.hop_type = hop_type
		self.hop_form = hop_form
		self.alpha = alpha
		self.beta = beta
		self.stability = stability
		self.origin = origin
		self.name = name
		self.description = description
    
class Grain(Ingredient):

	def __init__(self, name = None, origin = None, color = 0.0, 
		potential = 0.0, dry_yield_fine_grain = 0.0, 
		coarse_fine_difference = 0.0, moisture = 0.0, diastic_power = 0.0, 	
		max_in_batch = 0.0, protein = 0.0, must_mash = False, 
		add_after_boil = False, notes = None,):
		
		self.name = name
		self.origin = origin
		self.color = color
		self.potential = potential
		self.dry_yield_fine_grain = dry_yield_fine_grain
		self.coarse_fine_difference = coarse_fine_difference
		self.moisture = moisture
		self.diastic_power = diastic_power
		self.max_in_batch = max_in_batch
		self.protein = protein
		self.must_mash = must_mash
		self.add_after_boil = add_after_boil
		self.notes = notes
    
class Extract(Ingredient):

	def __init__(self, name = None, origin = None, color = 0.0, 
		potential = 0.0, dry_yield_fine_grain = 0.0, 
		max_in_batch = 0.0, add_after_boil = False, notes = None,):
		
		self.name = name
		self.origin = origin
		self.color = color
		self.potential = potential
		self.dry_yield_fine_grain = dry_yield_fine_grain
		self.max_in_batch = max_in_batch
		self.add_after_boil = add_after_boil
		self.notes = notes
    
class Yeast(Ingredient):
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
		
	def __init__(self, name = None, lab = None, ID = None, 
		yeast_type = 0, yeast_form = 0, flocc = 0, starter_size = 0.0,
		avg_attenuation = 0.0, min_temp = 0.0, max_temp = 0.0, 
		max_reuse = 0, best_for = None, notes = None, 
		use_starter = False, secondary = False):
		
		self.name = name
		self.lab = lab
		self.ID = ID
		self.yeast_type = yeast_type
		self.yeast_form = yeast_form
		self.flocc = flocc
		self.starter_size = starter_size
		self.avg_attenuation = avg_attenuation
		self.min_temp = min_temp
		self.max_temp = max_temp
		self.max_reuse = max_reuse
		self.best_for = best_for
		self.notes = notes
		self.use_starter = use_starter
		self.secondary = secondary

    
class Water(Ingredient):
	molecule_types = {'ca': 'Calcium', 'mg': 'Magnesium', 'na': 'Sodium',
		'so4': 'Sulfate', 'cl': 'Chloride', 'hco3': 'Bicarbonate'}
	
	def __init__(self, name = None, pH = 0.0, ca  = 0.0, mg = 0.0, na = 0.0, 
		so4 = 0.0, cl = 0.0, hco3 = 0.0, notes = None):
		
		self.name = name
		self.pH = pH
		self.ca = ca
		self.mg = mg
		self.na = na
		self.so4 = so4
		self.cl = cl
		self.hco3 = hco3
		self.notes = notes

class Misc(Ingredient):
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

	def __init__(self, name = None, use_for = None, 
		rec_amount = 0.0, rec_units = 0, batch_size = 0.0, 
		batch_size_units = 0, use_in = 0, use_time = 0, use_time_units = 0, 
		misc_type = 0):
		
		self.name = name
		self.misc_type = misc_type
		self.use_for = use_for
		self.rec_amount = rec_amount
		self.rec_units = rec_units
		self.batch_size = batch_size
		self.batch_size_units = batch_size_units
		self.use_in = use_in
		self.use_time = use_time
		self.use_time_units = use_time_units

class Mineral(Misc):
	def __init__(self, name = None, use_for = None, 
		rec_amount = 0.0, rec_units = 0, batch_size = 0.0, 
		batch_size_units = 0, use_in = 0, use_time = 0, use_time_units = 0, 
		misc_type = 0):

		Misc.__init__(self, name, use_for, 
			rec_amount, rec_units, batch_size , 
			batch_size_units, use_in, use_time, use_time_units, 
			misc_type = Misc.WATER_AGENT)
    
class Fining(Misc):
	def __init__(self, name = None, use_for = None, 
		rec_amount = 0.0, rec_units = 0, batch_size = 0.0, 
		batch_size_units = 0, use_in = 0, use_time = 0, use_time_units = 0, 
		misc_type = 0):

		Misc.__init__(self, name, use_for, 
			rec_amount, rec_units, batch_size , 
			batch_size_units, use_in, use_time, use_time_units, 
			misc_type = Misc.FINING)


class Flavor(Misc):
	def __init__(self, name = None, use_for = None, 
		rec_amount = 0.0, rec_units = 0, batch_size = 0.0, 
		batch_size_units = 0, use_in = 0, use_time = 0, use_time_units = 0, 
		misc_type = 0):

		Misc.__init__(self, name, use_for, 
			rec_amount, rec_units, batch_size , 
			batch_size_units, use_in, use_time, use_time_units, 
			misc_type = Misc.FLAVOR)
	
class Spice(Misc):
	def __init__(self, name = None, use_for = None, 
		rec_amount = 0.0, rec_units = 0, batch_size = 0.0, 
		batch_size_units = 0, use_in = 0, use_time = 0, use_time_units = 0, 
		misc_type = 0):

		Misc.__init__(self, name, use_for, 
			rec_amount, rec_units, batch_size , 
			batch_size_units, use_in, use_time, use_time_units, 
			misc_type = Misc.SPICE)


class Herb(Misc):
	def __init__(self, name = None, use_for = None, 
		rec_amount = 0.0, rec_units = 0, batch_size = 0.0, 
		batch_size_units = 0, use_in = 0, use_time = 0, use_time_units = 0, 
		misc_type = 0):

		Misc.__init__(self, name, use_for, 
			rec_amount, rec_units, batch_size , 
			batch_size_units, use_in, use_time, use_time_units, 
			misc_type = Misc.HERB)	
