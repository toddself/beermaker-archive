#!/usr/bin/env python

from db import DataStore
from sqlobject import *
from xml.dom import minidom
from recipes import BJCPCategory, BJCPStyle

if __name__ == '__main__':
    # connect to the database
    data = DataStore()
    
    # init the db if necessary
    BJCPCategory.createTable(ifNotExists=True)
    BJCPStyle.createTable(ifNotExists=True)
    
    # import the XML
    styledoc = minidom.parse('styleguide2008.xml')
    
    # generate categories
    for beer_class in styledoc.getElementsByTagName('class'):
        this_class = unicode(beer_class.getAttribute('type'))
        for category in beer_class.getElementsByTagName('category'):
            name = unicode(category.getElementsByTagName('name')[0].firstChild.data)
            category_id = int(category.getAttribute('id'))
            this_category = BJCPCategory(name=name, category_id=category_id)
            # generate styles for this category
            for sub_category in category.getElementsByTagName('subcategory'):
                # we're only interested in the last letter -- the number is duplicative data
                subcategory_id = unicode(sub_category.getAttribute('id')[-1:])
                name = unicode(sub_category.getElementsByTagName('name')[0].firstChild.data)
                print name                
                aroma = unicode(sub_category.getElementsByTagName('aroma')[0].firstChild.data)
                appearance = unicode(sub_category.getElementsByTagName('appearance')[0].firstChild.data)
                flavor = unicode(sub_category.getElementsByTagName('flavor')[0].firstChild.data)
                mouthfeel = unicode(sub_category.getElementsByTagName('mouthfeel')[0].firstChild.data)
                impression = unicode(sub_category.getElementsByTagName('impression')[0].firstChild.data)
                comments = unicode(sub_category.getElementsByTagName('comments')[0].firstChild.data)
                ingredients = unicode(sub_category.getElementsByTagName('ingredients')[0].firstChild.data)
                examples = unicode(sub_category.getElementsByTagName('examples')[0].firstChild.data)
                for stat in sub_category.getElementsByTagName('stats'):
                    if stat.getElementsByTagName('exceptions'):
                        pass
                    else:
                        og_low = float(stat.getElementsByTagName('og')[0].getElementsByTagName('low')[0].firstChild.data)
                        og_high = float(stat.getElementsByTagName('og')[0].getElementsByTagName('high')[0].firstChild.data)
                        fg_low = float(stat.getElementsByTagName('fg')[0].getElementsByTagName('low')[0].firstChild.data)
                        fg_high = float(stat.getElementsByTagName('fg')[0].getElementsByTagName('high')[0].firstChild.data)
                        ibu_low = int(stat.getElementsByTagName('ibu')[0].getElementsByTagName('low')[0].firstChild.data)
                        ibu_high = int(stat.getElementsByTagName('ibu')[0].getElementsByTagName('high')[0].firstChild.data)
                        srm_low = float(stat.getElementsByTagName('srm')[0].getElementsByTagName('low')[0].firstChild.data)
                        srm_high = float(stat.getElementsByTagName('srm')[0].getElementsByTagName('high')[0].firstChild.data)
                        abv_low = float(stat.getElementsByTagName('abv')[0].getElementsByTagName('low')[0].firstChild.data)
                        abv_high = float(stat.getElementsByTagName('abv')[0].getElementsByTagName('high')[0].firstChild.data)

                                
            BJCPStyle(name = name, 
                      beer_type = this_class.capitalize(), 
                      category = this_category,
                      subcategory = subcategory_id,                      
                      aroma = aroma,
                      appearance = appearance,
                      flavor = flavor,
                      mouthfeel = mouthfeel,
                      impression = impression,
                      comments = comments,
                      examples = examples,
                      og_low = og_low,
                      og_high = og_high,
                      fg_low = fg_low,
                      fg_high = fg_high,
                      srm_low = srm_low,
                      srm_high = srm_high,
                      ibu_low = ibu_low,
                      ibu_high = ibu_high,
                      abv_low = abv_low,
                      abv_high = abv_high,
                      )
