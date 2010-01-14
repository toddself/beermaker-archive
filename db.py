from sqlobject import *
import sys, os

class DataStore():
    db_filename = os.path.abspath('beermaker.db')
    db_driver = 'sqlite'

    def __init__(self):
        connection_string = "%s:%s" % (self.db_driver, self.db_filename)
        connection = connectionForURI(connection_string)
        sqlhub.processConnection = connection