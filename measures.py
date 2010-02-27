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

class Measures():
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
    FAHRENHEIT = 45
    CELSIUS = 46
    F = 47
    C = 48
    
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
    f = [FAHRENHEIT, F]
    c = [CELSIUS, C]

    measures = ['mg', 'milligram', 'milligrams', 'gm', 'grams', 'gram', 'g', 
        'oz', 'ounces', 'ounce', 'lb', 'lbs', 'pounds', 'pound', 'kg', 
        'kilo', 'kilograms', 'kilogram', 'ml','milliliters', 'milliliter', 
        'mils', 'tsp', 'teaspoon', 'teaspoons', 'tbls', 'tbsp', 'tablespoon',
        'tablespoons', 'cup', 'cups', 'pt', 'pint', 'pints', 'qt', 
        'quart','quarts', 'l', 'liter', 'gal', 'gallon', 'gallons', 'items', 
        'item', 'fahrenheit', 'celsius', 'f','c']
            
    weights = [MG, MILLIGRAM, MILLIGRAMS, GM, GRAMS, GRAM, G, OZ, OUNCES,
        OUNCE, LB, LBS, POUNDS, POUND, KG, KILOS, KILOGRAMS, KILOGRAM]

    volumes = [OZ, OUNCES, OUNCE, ML, MILLILITERS, MILLILITER, MILS, TSP,
        TEASPOON, TEASPOONS, CUP, CUPS, PT, PINT, PINTS, QT, QUART,
        QUARTS, L, LITER, LITERS, GAL, GALLON, GALLONS]
        
    temperatures = [FAHRENHEIT, CELSIUS, F, C]
    
    matters =  weights + volumes + temperatures
        
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
    timing_parts = ['min', 'minute', 'minutes', 'hrs', 'hour', 'hours',
        'days', 'day', 'weeks', 'week']
    
    minute = [MIN, MINUTE, MINUTES]
    hr = [HRS, HOUR, HOURS]
    day = [DAY, DAY]
    week = [WEEK, WEEKS]
    
    times = minute + hr + day + week
        
    TIME = 0
    MATTER = 1
    
    convert_values = {
        KG: {OZ: Decimal("35.27"), LB: Decimal("2.21"), MG: Decimal("1000000"), GM: Decimal("1000"))},
        OZ: {KG: Decimal('0.03'), LB: Decimal('0.06'), MG: Decimal("28349.52"), GM: Decimal("28.35"))},
        LB: {OZ: Decimal('16'), KG: Decimal('0.45'), MG: Decimal('453592.37'), GM: Decimal('45.36'))},
        GM: {OZ: Decimal('0.03'), LB: Decimal('0.002'), MG: Decimal('1000'), KG: Decimal('0.001'))},
        MG: {OZ: Decimal('0.00004'), LB: Decimal('0.000002'), KG: Decimal('0.000001', GM: Decimal('0.001'))},
        ML: {TSP: Decimal('0.203'), TBSP: Decimal('0.068'), CUP: Decimal('0.004'), PT: Decimal('0.002'), QT: Decimal('0.001'), L: Decimal('0.001'), GAL: Decimal('0.0003')},
        TSP: {ML, TBSP, CUP, PT, QT, L, GAL},
        TBSP: {ML, TSP, CUP, PT, QT, L, GAL},
        CUP: {ML, TSP, TBSP, PT, QT, L, GAL},
        PT: {ML, TSP, TBSP, CUP, QT, L, GAL},
        QT: {ML, TSP, TBSP, PT, CUP, L, GAL},
        L: {ML, TSP, TBSP, PT, QT, CUP, GAL},
        GAL: {ML, TSP, TBSP, PT, QT, CUP, L}
        
    
    }
    
        
    def __init__(self, amount_str, default_unit=0):
        self.amount_str = amount_str
        self.default_unit = default_unit
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
            unit = self.amount_str[start_pos:]
            
        # we gotta do something if we can't figure out what the unit is
        if unit not in self.measures and unit not in self.timing_parts:
            unit = self.default_unit

        if unit in self.measures:
            self.unit = self.measures.index(unit)    
            self.unit_type = self.MATTER
        elif unit in self.timing_parts:
            self.unit = self.timing_parts.index(unit)
            self.unit_type = self.TIME
            
        try:
            self.count = Decimal(val)
        except ValueError:
            self.count = 0.0
            
    def convert(self, convert_to):
        if convert_to in self.timing_parts:
            self.convert_to = self.timing_parts[convert_to]
            self.convert_type = self.TIME
        elif convert_to in self.measures:
            self.convert_to = self.measures[convert_to]
            self.convert_type = self.MATTER
        elif int(convert_to):
            if convert_to in self.matters:
                self.convert_to = convert_to
                self.convert_type = self.MATTER
            elif convert_to in self.times:
                self.convert_to = convert_to
                self.convert_type - self.TIME
            else:
                raise ConvertError("I'm not sure how to convert this measurement into that unit.")
                return 0
        else:
            raise ConvertError("%s is not a valid unit that I know how to convert into." % convert_to)
            return 0
        
        if self.convert_type == self.unit_type:
            convert_value = self.converters[self.unit_type][self.convert_type]
            converted = convert_value * self.amount
            return converted
        else:
            raise ConvertError("You can't convert a measure of physical matter to a measure of time or vice versa")
            return 0
            
    def __unicode__(self):
        if self.unit_type == self.TIME:
            unit_string = self.timing_parts[self.unit]
        else:
            unit_string = self.measures[self.unit]
            
        return "%s %s" % (self.count, unit_string)
        
    def __str__(self):
        return self.__unicode__()
        
    def __repr__(self):
        return self.__unicode__()

class ConvertError(Exception):
    pass