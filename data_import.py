#!/usr/bin/env python
from xml.dom import minidom

import db
from models import Hop, Grain, Extract, HoppedExtract, Yeast
from algorithms import sg_from_yield

if __name__ == '__main__':
    main()
    
def main():
    ds = db.DataStore()
    
    d = minidom.parse('database.xml')
    
    # process all the hops
    for hop in d.getElementsByTagName('HOP'):
        g = hop.getElementsByTagName
        name = origin = substitutes = description = None
        alpha = beta = hop_type = hop_form = stability = 0
        
        try:
            name = unicode(g('NAME')[0].firstChild.data)
        except AttributeError:
            pass
        try:    
            alpha = float(g('ALPHA')[0].firstChild.data)
        except AttributeError:
            pass
        try:    
            beta = float(g('BETA')[0].firstChild.data)
        except AttributeError:
            pass
        try:    
            origin = unicode(g('ORIGIN')[0].firstChild.data)
        except AttributeError:
            pass
        try:    
            substitutes = unicode(g('SUBSTITUTES')[0].firstChild.data)
        except AttributeError:
            pass
        try:    
            description = unicode(g('NOTES')[0].firstChild.data)
        except AttributeError:
            pass
        try:    
            hop_type = Hop.hop_types.index(g('TYPE')[0].firstChild.data)
        except AttributeError:
            pass
        try:    
            hop_form = 0
        except AttributeError:
            pass
        try:    
            stability = float(g('HSI')[0].firstChild.data)
        except AttributeError:
            pass

        thisHop = Hop(name=name,
            alpha=alpha,
            beta=beta,
            origin=origin,
            substitutes=substitutes,
            description=description,
            hop_type=hop_type,
            hop_form=hop_form,
            stability=stability
            )
        
    # process all the fermentables
    for f in d.getElementsByTagName('FERMENTABLE'):
        g = f.getElementsByTagName
        key = g('TYPE')[0].firstChild.data.lower()
        # grains...
        if key == 'grain' or key == 'adjunct':
            # set the grain defaults
            name = origin = maltster = notes = None
            color = potential = dry_yield_fine_grain = coarse_fine_difference = moisture =\
            diastatic_power = max_in_batch = protein = 0
            must_mash = add_after_boil = True
            
            try:
                name = unicode(g('NAME')[0].firstChild.data)
            except AttributeError:
                pass
            try:
                origin = unicode(g('ORIGIN')[0].firstChild.data)
            except AttributeError:
                pass
            try:
                maltster = unicode(g('SUPPLIER')[0].firstChild.data)
            except AttributeError:
                pass
            try:
                color = float(g('COLOR')[0].firstChild.data)
            except AttributeError:
                pass
            try:    
                potential = sg_from_yield(float(g('YIELD')[0].firstChild.data))
            except AttributeError:
                pass
            try:    
                dry_yield_fine_grain = 0
            except AttributeError:
                pass
            try:    
                coarse_fine_difference = float(g('COARSE_FINE_DIFF')[0].firstChild.data)                
            except AttributeError:
                pass
            try:    
                moisture = float(g('MOISTURE')[0].firstChild.data)
            except AttributeError:
                pass
            try:    
                diastatic_power = float(g('DIASTATIC_POWER')[0].firstChild.data)
            except AttributeError:
                pass
            try:    
                max_in_batch = float(g('MAX_IN_BATCH')[0].firstChild.data)
            except AttributeError:
                pass
            try:    
                if g('IS_MASHED')[0].firstChild.data == 'FALSE':
                    must_mash = False
                else:
                    must_mash = True
            except AttributeError:
                pass
            try:    
                if g('ADD_AFTER_BOIL')[0].firstChild.data == 'FALSE':
                    add_after_boil = False
                else:
                    add_after_boil = True
            except AttributeError:
                pass
            try:    
                notes = unicode(g('NOTES')[0].firstChild.data)
            except AttributeError:
                pass
                
            thisGrain = Grain(name=name,
                origin=origin,
                maltster=maltster,
                color=color,
                potential=potential,
                dry_yield_fine_grain=dry_yield_fine_grain,
                coarse_fine_difference=coarse_fine_difference,
                moisture=moisture,
                diastatic_power=diastatic_power,
                max_in_batch=max_in_batch,
                must_mash=must_mash,
                add_after_boil=add_after_boil,
                notes=notes
            )
        elif key == 'extract' or key == 'sugar' or key == 'dry extract':
            name = origin = supplier = notes = None
            color = potential = max_in_batch = 0
            add_after_boil = False
            
            try:
                name = unicode(g('NAME')[0].firstChild.data)
            except AttributeError:
                 pass
            try:                 
                origin = unicode(g('ORIGIN')[0].firstChild.data)
            except AttributeError:
                 pass
            try:
                 supplier = unicode(g('SUPPLIER')[0].firstChild.data)
            except AttributeError:
                 pass
            try:
                notes = unicode(g('NOTES')[0].firstChild.data)
            except AttributeError:
                 pass
            try:
                color = float(g('COLOR')[0].firstChild.data)
            except AttributeError:
                 pass
            try:
                potential = sg_from_yield(float(g('YIELD')[0].firstChild.data))
            except AttributeError:
                 pass
            try:    
                max_in_batch = float(g('MAX_IN_BATCH')[0].firstChild.data)
            except AttributeError:
                 pass
            try:
                if g('ADD_AFTER_BOIL')[0].firstChild.data == 'FALSE':
                    add_after_boil = False
                else:
                    add_after_boil = True
            except AttributeError:
                 pass

            thisExtract = Extract(name=name,
            origin=origin,
            supplier=supplier,
            notes=notes,
            color=color,
            potential=potential,
            max_in_batch=max_in_batch,
            add_after_boil=add_after_boil
            )