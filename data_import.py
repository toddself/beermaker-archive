#!/usr/bin/env python
from xml.dom import minidom

import db
from models import Hop, Grain, Extract, HoppedExtract, Yeast, Measures, Fining, Mineral, Flavor, Spice, Herb, Misc
from algorithms import sg_from_yield, c2f

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
                dry_yield_fine_grain = float(g('YIELD')[0].firstChild.data)
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
            
    for y in d.getElementsByTagName('YEAST'):
        g = y.getElementsByTagName
        
        #set some reasonable defaults
        name = lab = yeast_id = best_for = notes = None
        yeast_type = yeast_form = flocc = starter_size =\
            starter_units = avg_attenuation = min_temp =\
            max_temp = temp_units = max_reuse = 0
        use_starter = secondary = False        
        
        try:
            name = unicode(g('NAME')[0].firstChild.data)
        except AttributeError:
            pass
        try:
            yeast_type = Yeast.yeast_types.index(g('TYPE')[0].firstChild.data)
        except AttributeError:
            pass
        try:
            yeast_form = Yeast.yeast_forms.index(g('FORM')[0].firstChild.data)
        except AttributeError:
            pass
        try:
            yeast_id = unicode(g('PRODUCT_ID')[0].firstChild.data)
        except AttributeError:
            pass
        try:
            flocc = Yeast.yeast_flocculations.index(g('FLOCCULATION')[0].firstChild.data)
        except AttributeError:
            pass
        try:
            avg_attenuation = float(g('ATTENUATION')[0].firstChild.data)
        except AttributeError:
            pass
        try:
            min_temp = c2f(float(g('MIN_TEMPERATURE')[0].firstChild.data))
        except AttributeError:
            pass
        try:
            max_temp = c2f(float(g('MAX_TEMPERATURE')[0].firstChild.data))
        except AttributeError:
            pass
        try:
            max_reuse = int(g('MAX_REUSE')[0].firstChild.data)
        except AttributeError:
            pass
        try:
            best_for = unicode(g('BEST_FOR')[0].firstChild.data)
        except AttributeError:
            pass
        try:
            notes = unicode(g('NOTES')[0].firstChild.data)
        except AttributeError:
            pass            
        try:
            if g('ADD_TO_SECONDARY')[0].firstChild.data == 'FALSE':
                add_to_secondary = False
            else:
                add_to_secondary = True
        except AttributeError:
            pass
        try:
            amount = float(g('AMOUNT')[0].firstChild.data)*1000
        except AttributeError:
            pass
        try:
            if g('AMOUNT_IS_WEIGHT')[0].firstChild.data == 'FALSE':
                amount_units = Measures.ML
            else:
                amount_units = Measures.GM
        except AttributeError:
            pass

        temp_units = Measures.FAHRENHEIT            
        if yeast_type == Yeast.yeast_forms.index('Liquid'):
            use_starter = True
        else:
            use_starter = False
        
        thisYeast = Yeast(name=name,
        yeast_type=yeast_type,
        yeast_form=yeast_form,
        yeast_id=yeast_id,
        flocc=flocc,
        avg_attenuation=avg_attenuation,
        min_temp=min_temp,
        max_temp=max_temp,
        max_reuse=max_reuse,
        best_for=best_for,
        notes=notes,
        secondary=add_to_secondary,
        temp_units=temp_units,
        use_starter=use_starter,
        amount=amount,
        amount_units=amount_units
        )

    for m in d.getElementsByTagName('MISC'):
        g = m.getElementsByTagName
        
        misc_type = g('TYPE')[0].firstChild.data
        if misc_type == "Fining":
            misc_obj = Fining
        elif misc_type == 'Other':
            misc_obj = Misc
        elif misc_type == 'Flavor':
            misc_obj = Flavor
        elif misc_type == 'Water Agent':
            misc_obj = Mineral
        else:
            print "No matched type, boss %s" % misc_type
            pass



        name = use_for = notes = None
        rec_amount = rec_units = batch_size = batch_size_units = \
            use_in = use_time = use_time_units = 0

        try:
            name = unicode(g('NAME')[0].firstChild.data)
        except AttributeError:
            pass
        try:
            use_for = unicode(g('USE_FOR')[0].firstChild.data)
        except AttributeError:
            pass
        try:
            use_in = Misc.misc_use_ins.index(g('USE')[0].firstChild.data)
        except AttributeError:
            pass
        

        thisMisc = misc_obj(name=name,
            use_for=use_for,
            rec_amount=rec_amount,
            rec_units=rec_units,
            batch_size=batch_size,
            batch_size_units=batch_size_units,
            use_in=use_in,
            use_time=use_time,
            use_time_units=use_time_units
        )