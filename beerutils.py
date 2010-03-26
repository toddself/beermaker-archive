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

from sqlobject import *
from sqlobject.col import pushKey
from decimal import Decimal
from math import exp, tanh

SG_QUANT = Decimal(10) ** -3
PERCENT_QUANT = Decimal(10) ** -2
SRM_QUANT = Decimal(10) ** -1
IBU_QUANT = Decimal(10) ** -1

def fg_from_og(og, attenuation=Decimal('75')):    
    fg = og - (attenuation / Decimal('100'))
    
    return fg.quantize(SG_QUANT) + Decimal('1')

def abv_from_fg_and_og(fg, og):
    abv = (og - fg) * Decimal('131')
    
    return abv

def srm_from_mcu(mcu):
    srm =  Decimal('1.4922') * (mcu ** Decimal('0.6859'))
    return srm.quantize(SRM_QUANT)

def rager(hop_ounces, alpha_acids, boil_gallons, boil_gravity, usage_minutes):
    utilization = Decimal('18.11') + Decimal('13.86') * (Decimal('%s' % tanh(((usage_minutes - Decimal('31.32')) / Decimal('18.27')))))
    utilization = utilization / Decimal('100')
    adjustment_limit = Decimal('1.050')
    if boil_gravity > adjustment_limit:
        gravity_adjustment = (boil_gravity - adjustment_limit) / Decimal('0.2')
    else:
        gravity_adjustment = 0
    alpha_acids = alpha_acids / Decimal('100')
    ibu = (hop_ounces * utilization * alpha_acids * Decimal('7462')) / (boil_gallons * (Decimal('1') + gravity_adjustment ))
    return ibu.quanitze(IBU_QUANT)

def tinseth(hop_ounces, alpha_acids, boil_gallons, boil_gravity, usage_minutes):
    bigness = Decimal('1.65') * Decimal('0.000125') ** (boil_gravity - Decimal('1'))
    boil_time_factor = (Decimal('1') - Decimal("%s" % exp(Decimal('-0.04') * usage_minutes))) / Decimal('4.15')
    decimal_aa = bigness * boil_time_factor
    alpha_acids = alpha_acids / Decimal('100')
    mgl_aa = alpha_acids * hop_ounces * Decimal('7490') / boil_gallons
    ibu = decimal_aa * mgl_aa
    return ibu.quanitze(IBU_QUANT)
    
def garetz(hop_ounces, alpha_acids, boil_gallons, boil_gravity, usage_minutes, batch_gallons, target_ibu, elevation_feet):
    cf = batch_gallons / boil_gallons
    bg = (cf * (boil_gravity - Decimal('1')) + Decimal('1'))
    gf = ((bg - Decimal('1.050')) / Decimal('0.2')) + 1
    hf = ((cf * target_ibu) / Decimal('260')) + 1
    tf = ((elevation_feet / Decimal('550')) * Decimal('0.02')) + 1
    ca = gf * hf * tf
    if usage_minutes <= 10:
        utilization = Decimal('0')
    elif usage_minutes > 10 and usage_minutes < 16:
        utilization = Decimal('2')
    elif usage_minutes > 15 and usage_minutes < 21:
        utilization = Decimal('5')
    elif usage_minutes > 20 and usage_minutes < 26:
        utilization = Decimal('8')
    elif usage_minutes > 25 and usage_minutes < 31:
        utilization = Decimal('11')
    elif usage_minutes > 30 and usage_minutes < 36:
        utilization = Decimal('14')
    elif usage_minutes > 35 and usage_minutes < 41:
        utilization = Decimal('16')
    elif usage_minutes > 40 and usage_minutes < 46:
        utilization = Decimal('18')
    elif usage_minutes > 45 and usage_minutes < 51:
        utilization = Decimal('19')
    elif usage_minutes > 50 and usage_minutes < 61:
        utilization = Decimal('20')
    elif usage_minutes > 60 and usage_minutes < 71:
        utilization = Decimal('21')
    elif usage_minutes > 70 and usage_minutes < 81:
        utilization = Decimal('22')
    else:
        utilization = Decimal('23')
    ibu = utilization * alpha_acids * hop_ounces * Decimal('0.749') / (boil_gallons * ca)
    return ibu.quanitze(IBU_QUANT)
    
def gu_from_sg(sg):
    return int((sg - 1) * 1000)

def sg_from_gu(gu):
    return Decimal("%s" % ((float(gu)/1000.0) + 1)).quantize(SRM_QUANT)

def calculateBitternessRatio(sg, ibu):
    gu = (sg - 1) * 1000
    br = Decimal("%s" % ibu) / gu
    return br.quantize(PERCENT_QUANT)

def sg_from_yield(y):
    return Decimal("%.1fe-3" % (y / 100.0 * 46.0)).quantize(SG_QUANT) + Decimal(1)

def yield_from_sg(sg):
    return ((sg/46)*100)
    
def f2c(f):
    return ((f-32)*5)/9

def c2f(c):
    return ((c*9)/5)+32     

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

class IBUCol(DecimalCol):
    """ Stores the International Bitterness Units value in a decimal column
    Size is fixed at 4, precision is set to 1
    
    ex: 2.0, 300.5
    
    """

    def __init__(self, **kw):
        pushKey(kw, 'size', 4)
        pushKey(kw, 'precision', 1)
        super(DecimalCol, self).__init__(**kw)        

class BatchIsNotMaster(Exception):
    def __init__(self,value):
        self.value = value
    def __unicode__(self,value):
        return repr(self.value)

class AmountSetError(Exception):
    def __init__(self, value):
        self.value = value
    def __unicode__(self, value):
        return repr(self.value)  