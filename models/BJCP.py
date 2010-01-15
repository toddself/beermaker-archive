from sqlobject import *

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
    og_low = DecimalCol(size=4, precision=3, default=None)
    og_high = DecimalCol(size=4, precision=3, default=None)
    fg_low = DecimalCol(size=4, precision=3, default=None)
    fg_high = DecimalCol(size=4, precision=3, default=None)
    ibu_low = IntCol(default=None)
    ibu_high = IntCol(default=None)
    srm_low = DecimalCol(size=2, precision=1, default=None)
    srm_high = DecimalCol(size=2, precision=1, default=None)
    abv_low = DecimalCol(size=3, precision=1, default=None)
    abv_high = DecimalCol(size=3, precision=1, default=None)
    
class BJCPCategory(SQLObject):
    name = UnicodeCol(length=48, default=None)
    category_id = IntCol(default=None)  
    notes = UnicodeCol()
