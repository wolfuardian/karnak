# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import

import os
import tempfile

from PySide2 import QtWidgets, QtCore
import maya.cmds as cmds


class MenubarMixin(object):
    """
    Menu bar creation
    """
    def __init__(self, parent=None):
        # Execute __init__ of the multiply inherited class on the right
        super(MenubarMixin, self).__init__(parent)
        self.__menu_bar = QtWidgets.QMenuBar(self)
        self.layout().setMenuBar(self.__menu_bar)

    @property
    def menu_bar(self):
        """
        Access to Menubar Widget
        """
        return self.__menu_bar


class MinimumHelpMenuMixin(object):
    """
    Creation of help menu assuming MenubarMixin
    """
    def __init__(self, parent=None):
        # Execute __init__ of the multiply inherited class on the right
        super(MinimumHelpMenuMixin, self).__init__(parent)

    def create_help_menu(self, link):
        """
        Help Menu Creation
        """
        doc_action = QtWidgets.QAction('document',
                                       self,
                                       triggered=lambda: cmds.launch(web=link))

        help_menu = self.menu_bar.addMenu('Help')
        help_menu.addAction(doc_action)


class MinimumFileMenuMixin(object):
    """
    File menu creation assuming MenubarMixin
    The UI where you want to save the state needs an ObjectName
    """
    def __init__(self, parent=None):
        # Execute __init__ of the multiply inherited class on the right
        super(MinimumFileMenuMixin, self).__init__(parent)

    @property
    def __setting(self):
        """
        Access to QSetting files
        """
        setting_file = os.path.join(tempfile.gettempdir(), self.objectName() + '.ini')
        return QtCore.QSettings(setting_file, QtCore.QSettings.IniFormat)

    def create_file_menu(self):
        """
        File Menu Creation
        """
        save_action = QtWidgets.QAction('save ui settings', self, triggered=self.save_state)
        load_action = QtWidgets.QAction('load ui settings', self, triggered=self.load_state)

        file_menu = self.menu_bar.addMenu('File')
        file_menu.addAction(save_action)
        file_menu.addAction(load_action)

    def save_state(self, current_widget=None):
        """
        UI state preservation process
        """
        get_map = {
            QtWidgets.QComboBox: lambda x: x.currentIndex(),
            QtWidgets.QLineEdit: lambda x: x.text(),
            QtWidgets.QCheckBox: lambda x: x.checkState(),
        }

        w = current_widget or self
        for obj in w.children():
            name = obj.objectName()
            get_func = get_map.get(obj.__class__, None)

            if get_func:
                self.__setting.setValue(name, get_func(obj))
            if hasattr(obj, 'children'):
                self.save_state(obj)

    def load_state(self, current_widget=None):
        """
        UI state restoration process
        """
        set_map = {
            QtWidgets.QComboBox: lambda x, v: x.setCurrentIndex(int(v)),
            QtWidgets.QLineEdit: lambda x, v: x.setText(v),
            QtWidgets.QCheckBox: lambda x, v: x.setChecked(v == 2),
        }

        w = current_widget or self
        for obj in w.children():
            name = obj.objectName()
            set_func = set_map.get(obj.__class__, None)

            if set_func and self.__setting.value(name) is not None:
                set_func(obj, self.__setting.value(name))
            if hasattr(obj, 'children'):
                self.load_state(obj)
