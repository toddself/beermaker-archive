#!/usr/bin/env python

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

class Measure(object):
    MG = 0
    MILLIGRAM = 1
    MILLIGRAMS = 2
    GM = 3
    GRAMS = 4
    GRAM = 5
    G = 6
    OZ = 7
    OUNCES = 8 
    OUNCE = 9
    LB = 10
    LBS = 11
    POUNDS = 12
    POUND = 13
    KG = 14
    KILOS = 15
    KILOGRAMS = 16
    KILOGRAM = 17
    ML = 18
    MILLILITERS = 19
    MILLILITER = 20
    MILS = 21
    TSP = 22
    TEASPOON = 23
    TEASPOONS = 24
    TBLS = 25
    TBSP = 26
    TABLESPOON = 27
    TABLESPOONS = 28
    CUP = 29
    CUPS = 30
    PT = 31
    PINT = 32
    PINTS = 33
    QT = 34
    QUART = 35
    QUARTS = 36
    L = 37
    LITER = 38
    LITERS = 39
    GAL = 40
    GALLON = 41
    GALLONS = 42
    ITEMS = 43
    ITEM = 44
        
    mg = [MG, MILLIGRAM, MILLIGRAMS]
    gm = [GM, GRAMS, GRAM, G]
    oz = [OZ, OUNCES, OUNCE]
    lb = [LB, LBS, POUNDS, POUND]
    kg = [KG, KILOS, KILOGRAMS, KILOGRAM]
    ml = [ML, MILLILITER, MILLILITERS]
    tsp = [TSP, TEASPOON, TEASPOONS]
    tbls = [TBLS, TBSP, TABLESPOON, TABLESPOONS]
    cup = [CUP, CUPS]
    pt = [PT, PINT, PINTS]
    qt = [QT, QUART, QUARTS]
    l = [L, LITER, LITERS]
    gal = [GAL, GALLON, GALLONS]
    item = [ITEM, ITEMS]
    

    measures = ['mg', 'milligram', 'milligrams', 'gm', 'grams', 'gram', 'g', 'oz', 'ounces', 'ounce', 'lb', 'lbs', 'pounds', 'pound', 'kg', 'kilos', 'kilograms', 'kilogram', 'ml', 'milliliters', 'milliliter', 'mils', 'tsp', 'teaspoon', 'teaspoons', 'tbls', 'tbsp', 'tablespoon', 'tablespoons', 'cup', 'cups', 'pt', 'pint', 'pints', 'qt', 'quart', 'quarts', 'l', 'liter', 'liters', 'gal', 'gallon', 'gallons', 'items', 'item']            
            
    weights = [MG, MILLIGRAM, MILLIGRAMS, GM, GRAMS, GRAM, G, OZ, OUNCES,
        OUNCE, LB, LBS, POUNDS, POUND, KG, KILOS, KILOGRAMS, KILOGRAM]

    volumes = [OZ, OUNCES, OUNCE, ML, MILLILITERS, MILLILITER, MILS, TSP,
        TEASPOON, TEASPOONS, CUP, CUPS, PT, PINT, PINTS, QT, QUART,
        QUARTS, L, LITER, LITERS, GAL, GALLON, GALLONS]
        


    FAHRENHEIT = 0
    CELSIUS = 1
    F = 2
    C = 3
    temperatures = ['fahrenheit', 'celsius', 'f', 'c'] 
    
    f = [FAHRENHEIT, F]
    c = [CELSIUS, C]
    temps = [FAHRENHEIT, CELSIUS, F, C]
    
    matters =  weights + volumes
        
    MIN = 0
    MINUTE = 1
    MINUTES = 2
    HRS = 3
    HOUR = 4
    HOURS = 5
    DAYS = 6
    DAY = 7
    WEEKS = 8
    WEEK = 9
    HR = 10
    timing_parts = ['min', 'minute', 'minutes', 'hrs', 'hour', 'hours',
        'days', 'day', 'weeks', 'week', 'hr']
    
    minute = [MIN, MINUTE, MINUTES]
    hr = [HRS, HOUR, HOURS, HR]
    day = [DAYS, DAY]
    week = [WEEK, WEEKS]
    
    times = minute + hr + day + week
        
    TIME = 0
    MATTER = 1
    TEMPERATURE = 2 
    
    all_strings = timing_parts + measures + temperatures
    
    convert_dict = {
        KG: {OZ: Decimal("35.27"), LB: Decimal("2.21"), MG: Decimal("1000000"), GM: Decimal("1000")},
        OZ: {KG: Decimal('0.03'), LB: Decimal('0.06'), MG: Decimal("28349.52"), GM: Decimal("28.35"), ML: Decimal('29.57'), TSP: Decimal('6'), TBSP: Decimal('2'), PT: Decimal('0.0625'), QT: Decimal('.0313'), CUP: Decimal('0.125'), GAL: Decimal('0.008')},
        LB: {OZ: Decimal('16'), KG: Decimal('0.45'), MG: Decimal('453592.37'), GM: Decimal('45.36')},
        GM: {OZ: Decimal('0.03'), LB: Decimal('0.002'), MG: Decimal('1000'), KG: Decimal('0.001')},
        MG: {OZ: Decimal('0.00004'), LB: Decimal('0.000002'), KG: Decimal('0.000001'), GM: Decimal('0.001')},
        ML: {OZ: Decimal('0.034'), TSP: Decimal('0.20'), TBSP: Decimal('0.068'), CUP: Decimal('0.004'), PT: Decimal('0.002'), QT: Decimal('0.001'), L: Decimal('0.001'), GAL: Decimal('0.0003')},
        TSP: {OZ: Decimal('0.167'), ML: Decimal('4.93'), TBSP: Decimal('0.333'), CUP: Decimal('0.021'), PT: Decimal('0.01'), QT: Decimal('0.005'), L: Decimal('0.005'), GAL: Decimal('0.001')},
        TBSP: {OZ: Decimal('0.333'), ML: Decimal('14.78'), TSP: Decimal('3'), CUP: Decimal('0.063'), PT: Decimal('0.031'), QT: Decimal('0.016'), L: Decimal('0.015'), GAL: Decimal('0.004')},
        CUP: {OZ: Decimal('8'), ML: Decimal('236.59'), TSP: Decimal('48'), TBSP: Decimal('16'), PT: Decimal('0.5'), QT: Decimal('0.25'), L: Decimal('0.247'), GAL: Decimal('0.063')},
        PT: {OZ: Decimal('16'), ML: Decimal('473.18'), TSP: Decimal('96'), TBSP: Decimal('32'), CUP: Decimal('2'), QT: Decimal('0.5'), L: Decimal('0.47'), GAL: Decimal('0.125')},
        QT: {OZ: Decimal('32'), ML: Decimal('946.35'), TSP: Decimal('192'), TBSP: Decimal('64'), PT: Decimal('2'), CUP: Decimal('4'), L: Decimal('0.95'), GAL: Decimal('0.25')},
        L: {OZ: Decimal('33.81'), ML: Decimal('1000'), TSP: Decimal('202.88'), TBSP: Decimal('67.63'), PT: Decimal('2.11'), QT: Decimal('1.06'), CUP: Decimal('4.23'), GAL: Decimal('0.26')},
        GAL: {OZ: Decimal('128'), ML: Decimal('3785.41'), TSP: Decimal('768'), TBSP: Decimal('256'), PT: Decimal('8'), QT: Decimal('4'), CUP: Decimal('16'), L: Decimal('3.79')},
    }
    
    time_convert_dict = {
        DAY: {WEEK: Decimal('0.143'), HRS: Decimal('24'), MIN: Decimal('1440')},
        HRS: {DAY: Decimal('0.042'), WEEK: Decimal('0.0059'), MIN: Decimal('60')},
        WEEK: {DAY: Decimal('7'), HRS: Decimal('168'), MIN: Decimal('10080')},
        MIN: {WEEK: Decimal('0.00099'), HOUR: Decimal('0.017'), DAY:Decimal('0.0007')},
    }
    
        
    def __init__(self, amount_str):
        self.amount_str = amount_str
        self.converted = 0
        self.convert_type = None

        self._parseAmount()
        
    def _parseAmount(self):
        if ' ' in self.amount_str:
            (val, unit) = self.amount_str.split(' ')
        else:
            matched = False
            for x, c in enumerate(self.amount_str):
                if matched:
                    break
                if type(self.amount_str[x]) == type(''):
                    start_pos = x
                    matched = True
                
            val = self. amount_str[:start_pos-1]
            unit = self.amount_str[start_pos:].lower()
            
        if unit in self.measures:
            self.unit = self._getStandardUnit(self.measures.index(unit), self.MATTER)
            self.unit_type = self.MATTER
        elif unit in self.timing_parts:
            self.unit = self._getStandardUnit(self.timing_parts.index(unit), self.TIME)
            self.unit_type = self.TIME
        elif unit in self.temperatures:
            self.unit = self._getStandardUnit(self.temperatures.index(unit), self.TEMPERATURE)
            self.unit_type = self.TEMPERATURE
        else:
            raise ValueError('%s is not a known type of measurement' % unit)
            
        try:
            self.count = Decimal("%s" % val)
        except ValueError:
            raise ValueError('%s is not a valid number' % val)
            self.count = 0.0
            
    def _getStandardUnit(self, unit, unit_type):
        if unit_type == self.TEMPERATURE:
            if unit in self.c:
                return self.C
            elif unit in self.f:
                return self.F
            else:
                raise ValueError('I thought %s was a measure of temperature.'% self.temperatures[unit])
        elif unit_type == self.TIME:
            if unit in self.day:
                return self.DAY
            elif unit in self.hr:
                return self.HRS
            elif unit in self.week:
                return self.WEEK
            elif unit in self.minute:
                return self.MIN
            else:
                raise ValueError('I thought %s was a measure of time' % self.timing_parts[unit])            
        elif unit_type == self.MATTER:
            if unit in self.mg:
                return self.MG
            elif unit in self.gm:
                return self.GM
            elif unit in self.oz:
                return self.OZ
            elif unit in self.lb:
                return self.LB
            elif unit in self.kg:
                return self.KG
            elif unit in self.ml:
                return self.ML
            elif unit in self.tsp:
                return self.TSP
            elif unit in self.tbls:
                return self.TBSP
            elif unit in self.cup:
                return self.CUP
            elif unit in self.pt:
                return self.PT
            elif unit in self.qt:
                return self.QT
            elif unit in self.l:
                return self.L
            elif unit in self.gal:
                return self.GAL
            elif unit in self.item:
                return self.ITEM
            else:
                raise ValueError('I thought %s was a measure of physical items' % self.measures[unit])
        else:
            raise ValueError("I'm not sure what type of matter you're trying to measure")
            
    def convert(self, convert_to):
        # have we done this yet?
        if self.converted and self.convert_type == convert_to:
            return self.converted
        try:    
            if convert_to in self.timing_parts:
                self.convert_to = self._getStandardUnit(self.timing_parts.index(convert_to), self.TIME)
                self.convert_type = self.TIME
            elif convert_to in self.measures:
                self.convert_to = self._getStandardUnit(self.measures.index(convert_to), self.MATTER)
                self.convert_type = self.MATTER
            elif convert_to in self.temperatures:
                self.convert_to = self._getStandardUnit(self.temperatures.index(convert_to), self.TEMPERATURE)
                self.convert_type = self.TEMPERATURE
            elif int(convert_to):
                if convert_to in self.matters:
                    self.convert_to = self._getStandardUnit(convert_to, self.MATTER)
                    self.convert_type = self.MATTER
                elif convert_to in self.times:
                    self.convert_to = self._getStandardUnit(convert_to, self.TIME)
                    self.convert_type - self.TIME
                elif convert_to in self.temps:
                    self.convert_to = self._getStandardUnit(convert_to, self.TEMPERATURE)
                    self.convert_type = self.TEMPERATURE
                else:
                    raise ValueError("I'm not sure how to convert %s measurement into that %s." % (self.all_strings[self.unit], self.all_strings[convert_to]))
                    return 0
            else:
                raise ValueError("%s is not a valid unit that I know how to convert %s to." % (convert_to, self.all_strings[self.unit]))
                return 0
        except ValueError:
            raise ValueError("%s is not a valid unit I know how to convert %s to." % (convert_to, self.all_strings[self.unit]))

        # are we already using the right unit
        if self.convert_to == self.unit:
            return self.count
    
        if self.convert_type == self.unit_type:
            if self.convert_type == self.TEMPERATURE:
                if self.convert_to == self.F:
                    return Decimal("%s" % (((self.count*9)/5)+32)) 
                else:
                    return Decimal("%s" % (((self.count-32)*5)/9))
            else:
                if self.convert_type == self.TIME:
                    conversions = self.time_convert_dict
                else:
                    conversions = self.convert_dict     
                self.convert_value = conversions[self.unit][self.convert_to]
                self.converted = self.convert_value * self.count
                return Decimal("%s" % round(self.converted, 2))
        else:
            raise ValueError("%s and %s are incompatible types" % (self.all_strings[self.convert_type], self.all_strings[self.unit_type]))
            return 0
            
    def __unicode__(self):
        if self.unit_type == self.TIME:
            unit_string = self.timing_parts[self.unit]
        elif self.unit_type == self.TEMPERATURE:
            unit_string = self.temperatures[self.unit]
        else:
            unit_string = self.measures[self.unit]
            
        return "%s %s" % (self.count, unit_string)
        
    def __str__(self):
        return self.__unicode__()
        
    def __repr__(self):
        return self.__unicode__()

class ConvertError(Exception):
    pass