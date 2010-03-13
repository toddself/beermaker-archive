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
from math import exp

SG_QUANT = Decimal(10) ** -3
PERCENT_QUANT = Decimal(10) ** -2

def tinseth_utilization(bg, t):
    return (1.65 * (0.000125 ** (bg - 1))) * ((1 - exp(-0.04 * t)) / 4.15)
    
def daniels_utilization(form, time):
    hop_utilizations = {'Leaf': [0, 5, 12, 15, 19, 22, 24, 27], 'Pellet':  [0, 6 ,15, 19, 24, 27, 30, 34]}
    if form == 'Plug':
        form = 'Leaf'
    
    if time < 1:
        utilization = hop_utilizations[form][0]
    elif time >= 1 and time < 10:
        utilization = hop_utilizations[form][1]
    elif time >= 10 and time < 20:
        utilization = hop_utilizations[form][2]
    elif time >= 20 and time < 30:
        utilization = hop_utilizations[form][3]
    elif time >= 30 and time < 45:
        utilization = hop_utilizations[form][4]
    elif time >= 45 and time < 60:
        utilization = hop_utilizations[form][5]
    elif time >= 60 and time < 75:
        utilization = hop_utilizations[form][6]
    else:
        utilization = hop_utilizations[form][7]
        
    return Decimal("%.2f" % (float(utilization)/100.0))    


def get_ibu(hop, boil_volume, boil_gravity, method='daniels'):
    alpha = Hop.get(hop.ingredient_id).alpha
    logger.debug('hop used: %s [%.2f]' % (hop.name, alpha))
    if method == 'daniels':
        logger.debug('we are using the daniels equation for hop utilization')        
        if wort_gravity > Decimal('1.050'):
            correction = 1 + ((wort_gravity - Decimal('1.050')) / Decimal('0.2'))
        else:
            correction = 1
        logger.debug('correction: %s' % correction)
        ibu = ((hop.amount_m.convert('oz') * hop.utilization * alpha * Decimal('7489')) / (boil_volume.convert('gal') * correction))
        logger.debug('ibus: %.2f' % ibu)
    elif method == 'tinseth':
        logger.debug('we are using the tinseth curve equation for hop utilization')
        aau = (hop.amount_m.convert('oz') * alpha)
        logger.debug('aau: %s' % aau)
        utilization = tinseth_utilization(boil_gravity, hop.time_used_m.convert('min'))
        logger.debug('utilization: %s' % utilization)
        ibu = (aau * utilization * 75) / boil_volume
      
    logger.debug('ibus: %s' % ibu)  
    return ibu

def gu_from_sg(sg):
    return int((sg - 1) * 1000)

def sg_from_gu(gu):
    return Decimal("%s" % ((float(gu)/1000.0) + 1))

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