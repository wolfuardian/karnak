# -*- coding: utf-8 -*-
import os

import glob

from PySide2 import QtCore
from PySide2 import QtWidgets
from shiboken2 import wrapInstance

import maya.cmds as cmds
import maya.OpenMayaUI as omui

version = '0.0.1'
windows_title = 'Point Editor {} (Karnak)'.format(version)

mdl_res = 'C:/Users/eos/PycharmProjects/karnak/eil/resources/models/' + 'NADI_OCMS_ASSETS'
ui_res = 'C:/Users/eos/PycharmProjects/karnak/eil/tool/karnak/ui/'

loader = QUiLoader()


# class MainWidget(QWidget):
#     def __init__(self, parent=None):
#         super(MainWidget, self).__init__(parent)


# class MainWindow(QMainWindow):
#     def __init__(self, ui, parent=None):
#         super(MainWindow, self).__init__(parent)
#         self.mainWidget = MainWidget(self)
#
#         # self.setObjectName('MainWindow')
#         self.setWindowTitle(windows_title)
#         display = 1
#         screen_size = (1920, 1080)
#         windows_size = (720, 640)
#         # windows_size = (self.size().width(), self.size().height())
#         pivot = (
#             (display * screen_size[0]) + screen_size[0] / 2 - windows_size[0] / 2,
#             screen_size[1] / 2 - windows_size[1] / 2
#         )
#         self.setGeometry(pivot[0], pivot[1], windows_size[0], windows_size[1])
#         # QMainWindow.__init__(self, parent)
#
#     def setup(self):
#         self.setObjectName('MainWindow')
#         self.setWindowTitle(windows_title)
#         display = 1
#         screen_size = (1920, 1080)
#         windows_size = (self.size().width(), self.size().height())
#         pivot = (
#             (display * screen_size[0]) + screen_size[0] / 2 - windows_size[0] / 2,
#             screen_size[1] / 2 - windows_size[1] / 2
#         )
#         self.setGeometry(pivot[0], pivot[1], windows_size[0], windows_size[1])
#         self.listWidget.addItems(cmds.ls(type='transform'))
#         self.pushButton.clicked.connect(self.update_listview())
#
#     def update_listview(self):
#         self.listWidget.clear()
#         # fbx_ls = [f for f in glob.glob("*.txt") if isfile(join(mypath, f))]


def maya_main_window():
    """
    Return the Maya main window widget as a Python object
    """
    maya_main_ptr = omui.MQtUtil.mainWindow()
    return wrapInstance(int(maya_main_ptr), QtWidgets.QWidget)

class DesignerUI(QtWidgets.QDialog):
    def __init__(self, parent=maya_main_window()):
        super(DesignerUI, self).__init__(parent)

        self

# def list_files():
#     folders = glob.glob(mdl_res + '/*')
#     for folder in folders:
#         print(os.path.basename(folder))
#         print(glob.glob(folder + '/*'))
#
#
# def load(path):
#     file = QFile(path)
#     file.open(QFile.ReadOnly)
#     main_window = QUiLoader().load(file)
#     file.close()
#     return main_window
#
#
# window = None


def process():
    # global window
    # # Clear the existing window
    # if window is not None:
    #     window.deleteLater()
    #     window = None
    #
    # # Use the QFile method to load ui from a file
    # window = load(ui_res + 'form.ui')

    # Decorate ui using my way (display and behavior)
    # UIDecorator.setup(window)
    w = MainWindow()
    w.show()

    # window.show()


process()
