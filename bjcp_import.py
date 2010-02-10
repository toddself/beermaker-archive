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

from xml.dom import minidom

from sqlobject import *
from sqlobject.dberrors import DuplicateEntryError

import db
from models import BJCPCategory, BJCPStyle

if __name__ == '__main__':
    process_bjcp_styles()

def process_bjcp_styles():
    # connect to the database
    data = db.DataStore()
    
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
                name = aroma = flavor = appearance = mouthfeel = impression = comments = examples = None
                og_low = og_high = abv_high = fg_low = fg_high = srm_low = srm_high = abv_low = ibu_low = ibu_high = 0

                g = sub_category.getElementsByTagName
                # loop over the text nodes and set the value of the node equal to the xml node name
                try:
                    name = unicode(g('name')[0].firstChild.data)
                except (IndexError, AttributeError):
                    pass
                try:
                    aroma = unicode(g('aroma')[0].firstChild.data)
                except (IndexError, AttributeError):
                    pass
                try:
                    appearance = unicode(g('appearance')[0].firstChild.data)
                except (IndexError, AttributeError):
                    pass
                try:
                    flavor = unicode(g('flavor')[0].firstChild.data)
                except (IndexError, AttributeError):
                    pass
                try:
                    mouthfeel = unicode(g('mouthfeel')[0].firstChild.data)
                except (IndexError, AttributeError):
                    pass
                try:
                    impression = unicode(g('impression')[0].firstChild.data)
                except (IndexError, AttributeError):
                    pass
                try:
                    comments = unicode(g('comments')[0].firstChild.data)
                except (IndexError, AttributeError):
                    pass
                try:
                    examples = unicode(g('examples')[0].firstChild.data)
                except (IndexError, AttributeError):
                    pass

                s = g('stats')[0].getElementsByTagName
        
                if not s('exceptions'):                
                    try:
                        ibu_low = int(s('ibu')[0].getElementsByTagName('low')[0].firstChild.data)
                    except (IndexError, AttributeError):
                        pass
                    try:
                        ibu_high = int(s('ibu')[0].getElementsByTagName('high')[0].firstChild.data)
                    except (IndexError, AttributeError):
                        pass
                    try:
                        og_low = float(s('og')[0].getElementsByTagName('low')[0].firstChild.data)
                    except (IndexError, AttributeError):
                        pass
                    try:
                        og_high = float(s('og')[0].getElementsByTagName('high')[0].firstChild.data)
                    except (IndexError, AttributeError):
                        pass
                    try:
                        fg_low = float(s('fg')[0].getElementsByTagName('low')[0].firstChild.data)
                    except (IndexError, AttributeError):
                        pass
                    try:
                        fg_high = float(s('fg')[0].getElementsByTagName('high')[0].firstChild.data)
                    except (IndexError, AttributeError):
                        pass
                    try:
                        srm_low = float(s('srm')[0].getElementsByTagName('low')[0].firstChild.data)
                    except (IndexError, AttributeError):
                        pass
                    try:
                        srm_high = float(s('srm')[0].getElementsByTagName('high')[0].firstChild.data)
                    except (IndexError, AttributeError):
                        pass
                    try:
                        abv_low = float(s('abv')[0].getElementsByTagName('low')[0].firstChild.data)
                    except (IndexError, AttributeError):
                        pass
                    try:
                        abv_high = float(s('abv')[0].getElementsByTagName('high')[0].firstChild.data)
                    except (IndexError, AttributeError):
                        pass

                # I have no fucking clue why this stopped fucking working
                # for element in sub_category.childNodes:
                #     if element.localName != None and element.localName != "stats":
                #         try:
                #             print element.localName
                #             print element.firstChild.data
                #             vars()[element.localName] = unicode(element.firstChild.data)
                #             print "this name: %s" % vars()[element.localName]
                #         except AttributeError:
                #             pass
                #     # stats we'll have to handle differently
                #     elif element.localName == "stats":
                #         for stat in element.childNodes:
                #             if stat.localName != None and stat.localName != "exceptions":
                #                 if stat.localName == 'ibu':
                #                     ibu_low = int(stat.getElementsByTagName('low')[0].firstChild.data)
                #                     ibu_high = int(stat.getElementsByTagName('high')[0].firstChild.data)
                #                 else:
                #                     vars()["%s_high" % stat.localName] = float(stat.getElementsByTagName('high')[0].firstChild.data)
                #                     vars()["%s_low" % stat.localName] = float(stat.getElementsByTagName('low')[0].firstChild.data)

                print "adding style: %s" % name          
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