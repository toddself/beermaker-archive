#!/usr/bin/env python
from xml.dom import minidom

from sqlobject import *
from sqlobject.dberrors import DuplicateEntryError

from db import DataStore
from models import BJCPCategory, BJCPStyle

if __name__ == '__main__':
    # connect to the database
    data = DataStore()
    
    # import the XML
    styledoc = minidom.parse('styleguide2008.xml')
 
  # generate categories
    for beer_class in styledoc.getElementsByTagName('class'):
        this_class = unicode(beer_class.getAttribute('type'))
        for category in beer_class.getElementsByTagName('category'):            
            name = unicode(category.getElementsByTagName('name')[0].firstChild.data)
            category_id = int(category.getAttribute('id'))
            notes = ""
            if category.getElementsByTagName('notes'):
                for note in category.getElementsByTagName('notes'):
                    for child in note.childNodes:
                        notes = notes + "\n\n" + child.toxml()
            try:
                this_category = BJCPCategory(name=name, category_id=category_id, notes=notes)
            except DuplicateEntryError:
                this_category = BJCPCategory.selectBy(category_id=category_id)
            
            # generate styles for this category
            for sub_category in category.getElementsByTagName('subcategory'):
                # we're only interested in the last letter -- the number is duplicative data
                subcategory_id = unicode(sub_category.getAttribute('id')[-1:]).upper()
                # initialize the variables needed
                name = aroma = appearance = mouthfeel = impression = comments = examples = \
                og_low = og_high = fg_low = fg_high = srm_low = srm_high = abv_low = ibu_low = ibu_high = None

                # loop over the text nodes and set the value of the node equal to the xml node name
                for element in sub_category.childNodes:
                    if element.localName != None and element.localName != "stats":
                        try:
                            vars()[element.localName] = unicode(element.firstChild.data)
                        except AttributeError:
                            pass
                    # stats we'll have to handle differently
                    elif element.localName == "stats":
                        for stat in element.childNodes:
                            if stat.localName != None and stat.localName != "exceptions":
                                if stat.localName == 'ibu':
                                    ibu_low = int(stat.getElementsByTagName('low')[0].firstChild.data)
                                    ibu_high = int(stat.getElementsByTagName('high')[0].firstChild.data)
                                else:
                                    vars()["%s_high" % stat.localName] = float(stat.getElementsByTagName('high')[0].firstChild.data)
                                    vars()["%s_low" % stat.localName] = float(stat.getElementsByTagName('low')[0].firstChild.data)
                          
            BJCPStyle(name = name, 
                    beer_type = this_class, 
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