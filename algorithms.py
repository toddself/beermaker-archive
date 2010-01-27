from decimal import Decimal

SG_QUANT = Decimal(10) ** -3

def sg_from_yield(y):
    return Decimal("%.1fe-3" % (y / 100.0 * 46.0)).quantize(SG_QUANT) + Decimal(1)

    
def yield_from_sg(sg):
    return ((sg/46)*100)
    
def f2c(f):
    return ((f-32)*5)/9

def c2f(c):
    return ((c*9)/5)+32