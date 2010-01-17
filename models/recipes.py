from sqlobject import *

class Recipe(SQLObject):
    name = UnicodeCol(length=255, default=None)
    brewer = UnicodeCol(length=255, default=None)
    assistantBrewer = UnicodeCol(length=255, default=None)
    style = ForeignKey('BJCPStyle')