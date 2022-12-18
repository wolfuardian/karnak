# -*- coding: utf-8 -*-
import os
import sys

import glob

from PySide2 import QtCore
from PySide2 import QtUiTools
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.cmds as cmds
import maya.OpenMayaUI as omui

version = '0.0.1'
windows_title = 'Point Editor {} (Karnak)'.format(version)

def maya_main_window():
    """
    Return the Maya main window widget as a Python object
    """
    maya_main_ptr = omui.MQtUtil.mainWindow()
    if sys.version_info.major >= 3:
        return wrapInstance(int(maya_main_ptr), QtWidgets.QWidget)
    else:
        return wrapInstance(long(maya_main_ptr), QtWidgets.QWidget)


class PreferencesDialog(QtWidgets.QDialog):
    def __init__(self, parent=maya_main_window()):
        super(PreferencesDialog, self).__init__(parent)

        self.setWindowTitle("Preferences")
        self.setMinimumSize(960, 540)

        self.init_ui()
        self.create_layout()
        self.create_connection()

    def init_ui(self):
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load("C:/Users/eos/PycharmProjects/karnak/eil/tool/karnak/ui/preferences.ui")

    def create_layout(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.ui)

    def create_connection(self):
        self.ui.okButton.clicked.connect(self.accept)
        self.ui.cancelButton.clicked.connect(self.close)

    def get_option_a(self):
        return self.ui.checkBoxA.isChecked()

    def get_option_b(self):
        return self.ui.checkBoxB.isChecked()

    def get_option_c(self):
        return self.ui.checkBoxC.isChecked()


class MainDialog(QtWidgets.QDialog):
    def __init__(self, parent=maya_main_window()):
        super(MainDialog, self).__init__(parent)

        # self.setWindowTitle("Test Dialog")
        self.ui = None
        self.setWindowTitle(windows_title)

        self.setMinimumSize(960, 540)

        self.init_ui()
        self.create_layout()
        self.create_connections()

    def init_ui(self):
        loader = QtUiTools.QUiLoader()
        self.ui = loader.load("C:/Users/eos/PycharmProjects/karnak/eil/tool/karnak/ui/main.ui")

    def create_layout(self):
        main_layout = QtWidgets.QVBoxLayout(self)
        main_layout.setContentsMargins(2, 2, 2, 2)
        main_layout.setSpacing(2)
        main_layout.addWidget(self.ui)

    def create_connections(self):
        self.ui.preferences_action.triggered.connect(self.show_preferences)

    def show_preferences(self):
        preferences_dialog = PreferencesDialog(self)
        result = preferences_dialog.exec_()

        if result == QtWidgets.QDialog.Accepted:
            print("Option A Checked: {0}".format(preferences_dialog.get_option_a()))
            print("Option B Checked: {0}".format(preferences_dialog.get_option_b()))
            print("Option C Checked: {0}".format(preferences_dialog.get_option_c()))


if __name__ == "__main__":
    try:
        main_dialog.close()
        main_dialog.deleteLater()

    except AttributeError:
        print("AttributeError: Will skip")
        pass
    main_dialog = MainDialog()
    main_dialog.show()
