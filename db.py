#!/usr/bin/env python
import sys
import inspect
import os

from sqlobject import *

import models

import bjcp_import
import data_import

class DataStore():
    db_filename = os.path.abspath('beermaker.db')
    db_driver = 'sqlite'

    def __init__(self, debug=False):
        try:
            debug = GLOBAL_DEBUG
        except NameError:
            pass
            
        if sys.platform == 'win32':
            self.db_filename = "/"+self.db_filename.replace(":","|")

        if debug:
            if os.path.exists(self.db_filename):    
                print "Do you want to replace the currently existing database: %s [Y/n]" % self.db_filename    
                delete = raw_input().upper()
                if delete == "Y" or delete == '':
                    
                    os.unlink(self.db_filename)            

        connection_string = "%s:%s" % (self.db_driver, self.db_filename)
        connection = connectionForURI(connection_string)
        sqlhub.processConnection = connection
        
if __name__ == '__main__':
    data = DataStore(True)
    for table in [member[1] for member in inspect.getmembers(models,inspect.isclass) if member[1].__module__ == 'models']:
        if "tableExists" in [member[0] for member in inspect.getmembers(table,inspect.ismethod)]:
            if table.tableExists():
                print "Table: %s exists, dropping" % table.__name__
                table.dropTable()
        
            table.createTable()
            print "Created: %s" % table.__name__
    
    print "importing bjcp styles"
    bjcp_import.process_bjcp_styles()
    print "importing data"
    data_import.process_bt_database()
