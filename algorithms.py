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

from decimal import Decimal
from models import Measures

SG_QUANT = Decimal(10) ** -3

def sg_from_yield(y):
    return Decimal("%.1fe-3" % (y / 100.0 * 46.0)).quantize(SG_QUANT) + Decimal(1)

def yield_from_sg(sg):
    return ((sg/46)*100)
    
def f2c(f):
    return ((f-32)*5)/9

def c2f(c):
    return ((c*9)/5)+32
    
def convertToOz(amount, unit):
    unit = unit.lower()
    if Measures.measures.index(unit) not in Measures.weights:
        raise ConverterError('Cannot convert %s to a weight measure' % unit)
    else:
        if unit == 'kg':
            return amount * 35.27
        elif unit == 'mg':
            return amount / .0003527
        elif unit == 'lb':
            return amount * 16
        elif unit == 'gm':
            return amount / .003527
        elif unit == 'oz':
            return amount
        

class ConverterError(Exception):
    def __init__(self, value):
        self.value = value
    
    def __unicode__(self, value):
        return repr(self.value)
        