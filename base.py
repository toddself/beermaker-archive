#!/usr/bin/env python

# Copyright (C) 2010 Todd Kennedy <todd.kennedy@gmail.com>
# 
# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import wx        

class BaseWindow():
    """
    BaseWindow() provides some useful utilities for creating and managing application windows
    """

    TC_STYLE = wx.ALL|wx.ALIGN_CENTER_VERTICAL
    ST_STYLE = wx.ALL|wx.ALIGN_RIGHT|wx.ALIGN_CENTER_VERTICAL

    def __init__(self):
        pass
        
    def buildToolbar(self):
        """
        buildToolbar will generate a toolbar on the window with Text labels.  It expects 
        whatever is subclassing it to have a method called toolbarData which, when called
        returns a tuple of tuples matching the following spec:
        (ID, ICON, LABEL, HELP, METHOD)
        
        providing a tuple with a empty string for id will create a separator
        """
        toolbar = wx.ToolBar(self, -1, style=wx.TB_TEXT)
        self.SetToolBar(toolbar)
        for button in self.toolbarData():
            self._createTool(toolbar, *button)
        toolbar.Realize()
        
    def _createTool(self, toolbar, tb_id, fn_icon, label, help, handler):
        """
        _createTool should never be called directly, but rather from buildToolbar. It accepts the data
        about the tool to be created, creates it, places it in the toolbar and then binds the action
        to the method.  if the id is an empty string it'll create a separator
        """
        if not tb_id:
            toolbar.AddSeparator()
            return
        else:
            icon = wx.Bitmap(fn_icon, wx.BITMAP_TYPE_ANY)
            tool = toolbar.AddLabelTool(tb_id, label, icon, icon, wx.ITEM_NORMAL, label, help)
            self.Bind(wx.EVT_MENU, handler, tool)    
    
    def buildMenuBar(self):
        """
        buildMenuBar will build your applications menus and attach all relevant submenus and bind
        the events to the appropriate methods.  when called it'll expect whatever is subclassing
        BaseWindow to have a method defined named menuData that returns a tuple of menus.  the menus
        are tuples of dictionaries, each dictionary representing a unique item on the menu
        
        name: name of the menu or menu item
        method: method to be called upon selection
        id: guid for this menu option
        help: a help string
        
        to create a submenu, do not add the method, id and help keys, but rather an items key
        which contains a tuple of dictionaries as defined above
        """
        menu_bar = wx.MenuBar()
        for menu in self.menuData():
            label = menu['name']
            items = menu['items']
            menu_bar.Append(self._createMenu(items), label)
        self.SetMenuBar(menu_bar)
    
    def _createMenu(self, items):
        """ 
        _createMenu is a helper method for buildMenuBar and should never be called directly.
        it accepts a tuple of menu dictionaries and returns a menu.  if additional tuples are 
        found, it will generate submenus and attach them to the parent menu
        """
        menu = wx.Menu()
        for item in items:
            if item.has_key('items'):
                menu_id = wx.NewId()
                label = item['name']
                sub_menu = self._createMenu(item['items'])
                menu.AppendMenu(menu_id, label, sub_menu)
            else:
                self._createMenuItem(menu, item['id'], item['name'], item['help'], item['method'])
        return menu
        
    def _createMenuItem(self, menu, menu_id, name, help, method, kind=wx.ITEM_NORMAL):
        """
        _createMenuItem is a helper method for buildMenuBar and should never be called directly.
        it accepts all the arguments for terminal (non-submenu) menu item, creates the menu item,
        attaches it to the menu and then binds the menu item to the specified method
        """
        if menu_id == 'separator':
            menu.AppendSeparator()
            return
        menu_item = menu.Append(menu_id, name, help, kind)
        self.Bind(wx.EVT_MENU, method, menu_item)
        
    def _doLayout(self):
        """
        _doLayout generates the ui from a list of dictionaries.  This method expects a method to be defined
        called layoutData which returns a list.  this does not handle creating frames or dialogs, just the ui 
        for a pre-defined window.
        
        _doLayout returns a wx.BoxSizer(wx.VERTICAL) containing all the items defined by your dictionary list
        """

        for w in self.layoutData():
            if w.haskey('sizer'):
                s = self._createSizer(self, w)
            else:
                raise LayoutEngineError('Expected outer element to be a sizer')
            
            if w.haskey('widgets'):
                for e in w.widgets:
                    self._addWidgetToSizer(e, s)
            else:
                raise LayoutEngineError('Sizer is empty. Expected at least one element')
    
    def _createSizer(self, sizer):
        pass
                
    def _addWidgetToSizer(self, widget, sizer):
        """
        required info for adding to sizer
        proportion
        sizer_style
        border
        
        optional information:
        TODO: add info about other sizers
        """
        args = {'proportion': 0, 'sizer_style': wx.ALL, 'border': 0}
        for key in args.keys():
            if widget.haskey(key):
                args[key] = widget[key]
        sizer.Add(self._createWidget(), *args.values())
                
        
    def _createWidget(self, widget):
        """
        full definition:
        widget - this is the widget we'll be making
        value - any default value the widget should get
        input - 
        choices
        style
        sizer_style
        optional - method or parameter to check. if this key is present,
            item is considered to be optional and will only be displayed if the condition is true
        """
        
                
    
    def _createSectionHeader(self, title, font=None, scale=-1):
        if font == None:
            try:
                self.ui_font
            except AttributeError:
                f = wx.SystemSettings.GetFont(wx.SYS_DEFAULT_GUI_FONT)
                f.SetPointSize(f.GetPointSize() + scale)
            else:
                f = self.ui_font
        else:
            f = font
                
        section_head = wx.StaticText(self.main_panel, -1, title)
        section_head.SetFont(f)
        section_line = wx.StaticLine(self.main_panel, -1, style=wx.LI_HORIZONTAL)
        
        tb = wx.BoxSizer(wx.HORIZONTAL)
        tb.Add(section_head, 0, wx.ALL|wx.ALIGN_BOTTOM, 3)
        tb.Add(section_line, 1, wx.ALIGN_BOTTOM|wx.BOTTOM, 6)
        
        return tb