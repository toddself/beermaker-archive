




               # name = unicode(sub_category.getElementsByTagName('name')[0].firstChild.data)
               # aroma = unicode(sub_category.getElementsByTagName('aroma')[0].firstChild.data)
               # appearance = unicode(sub_category.getElementsByTagName('aroma')[0].firstChild.data)
               # mouthfeel = unicode(sub_category.getElementsByTagName('mouthfeel')[0].firstChild.data)
               # impression = unicode(sub_category.getElementsByTagName('impression')[0].firstChild.data)
               # comments = unicode(sub_category.getElementsByTagName('comments')[0].firstChild.data)
               # ingredients = unicode(sub_category.getElementsByTagName('ingredients')[0].firstChild.data)
               # examples = unicode(sub_category.getElementsByTagName('examples')[0].firstChild.data)
               # for stat in sub_category.getElementsByTagName('stats'):
               #     if stat.getElementsByTagName('exceptions'):
               #         pass
               #     else:
               #         og_low = float(stat.getElementsByTagName('og')[0].getElementsByTagName('low')[0].firstChild.data)
               #         og_high = float(stat.getElementsByTagName('og')[0].getElementsByTagName('high')[0].firstChild.data)
               #         fg_low = float(stat.getElementsByTagName('fg')[0].getElementsByTagName('low')[0].firstChild.data)
               #         fg_high = float(stat.getElementsByTagName('fg')[0].getElementsByTagName('high')[0].firstChild.data)
               #         ibu_low = int(stat.getElementsByTagName('ibu')[0].getElementsByTagName('low')[0].firstChild.data)
               #         ibu_high = int(stat.getElementsByTagName('ibu')[0].getElementsByTagName('high')[0].firstChild.data)
               #         srm_low = float(stat.getElementsByTagName('srm')[0].getElementsByTagName('low')[0].firstChild.data)
               #         srm_high = float(stat.getElementsByTagName('srm')[0].getElementsByTagName('high')[0].firstChild.data)
               #         abv_low = float(stat.getElementsByTagName('abv')[0].getElementsByTagName('low')[0].firstChild.data)
               #         abv_high = float(stat.getElementsByTagName('abv')[0].getElementsByTagName('high')[0].firstChild.data)
               



# 
#  
# 
# #get the document root node
# root = styledoc.getElementsByTagName(doc.documentElement.localName)[0]
# 
# #discern the classes.  we can't use the name given in the XML sadly due to a namespace collision
# for element in root.childNodes:
#     if element.localName != None:
#         beer_class = element.getAttribute('name')
#         for category in beer_class.childNodes:
#             if category.localName != None:
#                 category_id = int(category.getAttribute('id'))
#                 category_name = unicode(category.getElementsByTagName('name')[0].firstChild.data)
#                 this_category = BJCPCategory(category_id = category_id, name = category_name)
#                 for subcat in category.getElementsByTagName('subcategory'):
#                     subcat_id = unicode(subcat.getAttribute('id')[-1:]).upper()
#                     for entry_attribute in subcat.childNodes:
#                         if entry_attribute.localName != None:
#                             if "_"
#                             vars()[entry_attribute.localName] = unicode(entry_attribute.firstChild.data)
#         
# 
# 
# 
# 
#                     BJCPStyle(name = name, 
#                               beer_type = this_class.capitalize(), 
#                               category = this_category,
#                               subcategory = subcategory_id,                      
#                               aroma = aroma,
#                               appearance = appearance,
#                               flavor = flavor,
#                               mouthfeel = mouthfeel,
#                               impression = impression,
#                               comments = comments,
#                               examples = examples,
#                               og_low = og_low,
#                               og_high = og_high,
#                               fg_low = fg_low,
#                               fg_high = fg_high,
#                               srm_low = srm_low,
#                               srm_high = srm_high,
#                               ibu_low = ibu_low,
#                               ibu_high = ibu_high,
#                               abv_low = abv_low,
#                               abv_high = abv_high,
#                               )