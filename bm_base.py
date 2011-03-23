import wx
from base import BaseWindow

class BMB(wx.Frame, BaseWindow):
    """
    Set up and define all the base functions for launching new windows, handling cut and paste, etc
    """
    
    def newRecipe(self, event):
        from recipe_editor import RecipeEditor
        recipe_editor = RecipeEditor(self, -1, "", size=(1024,768), pos=(10,50))
        recipe_editor.Show()
    
    def newBatch(self):
        pass
        
    def viewInventory(self):
        """docstring for viewIventory"""
        pass
        
    def viewMashes(self):
        """docstring for viewMashes"""
        pass 
    
    def viewEquipment(self):
        """docstring for viewEquipment"""
        pass

    def viewIngredients(self):
        """docstring for viewIngredients"""
        pass

    def viewCalculators(self):
        """docstring for viewCalculators"""
        pass
        
    def viewPreferences(self):
        """docstring for viewPreferences"""
        pass
        
    def printItem(self):
        """docstring for printItem"""
        pass
    
    def quitApplication(self):
        """docstring for quitApplication"""
        pass
    
    def visitWebsite(self):
        """docstring for visitWebsite"""
        pass
        
    def undo(self):
        """docstring for undo"""
        pass

    def redo(self):
        """docstring for redo"""
        pass

    def copy(self):
        """docstring for copy"""
        pass

    def paste(self):
        """docstring for paste"""
        pass

    def cut(self):
        """docstring for cut"""
        pass

    