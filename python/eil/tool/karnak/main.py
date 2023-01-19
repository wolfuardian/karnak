# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import

import functools
import json
import ast
import os
import re
import io

import pymel.core as pm
import maya.cmds as cmds

from PySide2 import QtCore, QtGui, QtWidgets, QtUiTools
from maya.app.general import mayaMixin

from python.eil.util import common, qt
from python.eil.mixin import menu

import xml.etree.ElementTree as ET

import glob

proj_dir = 'C:/Users/eos/PycharmProjects/karnak/python/eil/tool/karnak'
settings = 'py_settings'


# Python 執行期間透過 Maya Object 存放所有資料
# 新建一個空物體
def create_node():
    if not cmds.objExists(settings):
        cmds.spaceLocator(name=settings)
    cmds.setAttr(settings + '.useOutlinerColor', True)
    cmds.setAttr(settings + '.outlinerColor', 1, 0, 0)
    cmds.hide(settings)
    cmds.select(cl=True)


# 新增、設置屬性
def add_attr():
    py_settings = pm.PyNode(settings)
    if not py_settings.hasAttr('initialization'):
        cmds.addAttr(settings, longName='initialization', dataType='string')
        cmds.addAttr(settings, longName='location', dataType='string')
        cmds.addAttr(settings, longName='resources', dataType='string')
        cmds.addAttr(settings, longName='resources_list', dataType='string')
        cmds.addAttr(settings, longName='resources_list_disp', dataType='string')
        cmds.addAttr(settings, longName='xml', dataType='string')
        cmds.addAttr(settings, longName='xml_data', dataType='string')

        cmds.setAttr(settings + '.initialization', type='string', lock=True)
        cmds.setAttr(settings + '.resources_list', '{}', type='string')
        cmds.setAttr(settings + '.resources_list_disp', 'short', type='string')
        cmds.setAttr(settings + '.xml_data', '{}', type='string')


def initialize_settings():
    create_node()
    add_attr()


initialize_settings()


class AboutDialog(QtWidgets.QDialog):
    def __init__(self, parent=qt.maya_main_window()):
        super(AboutDialog, self).__init__(parent)

        self.ui = None
        self.setWindowTitle("About Karnak")
        self.setMinimumSize(584, 630)
        self.setWindowFlags(self.windowFlags() & ~QtCore.Qt.WindowContextHelpButtonHint)

        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        self.setLayout(layout)

        loader = QtUiTools.QUiLoader()
        __about_menu_ui = loader.load("{0}/{1}".format(proj_dir, 'ui/menu/about.ui'))
        __about_menu_ui.setMinimumHeight(__about_menu_ui.height())

        __about_menu_ui.ok_button.clicked.connect(self.close)

        self.layout().addWidget(__about_menu_ui)

    def get_option_a(self):
        return self.ui.checkBoxA.isChecked()

    def get_option_b(self):
        return self.ui.checkBoxB.isChecked()

    def get_option_c(self):
        return self.ui.checkBoxC.isChecked()


class FrameLayoutWidget(mayaMixin.MayaQWidgetDockableMixin, mayaMixin.MayaQWidgetBaseMixin, qt.QtDefaultWidget):
    def __init__(self, parent=qt.maya_main_window()):
        super(FrameLayoutWidget, self).__init__(parent)
        self.resources_dict = {}
        self.setWindowTitle('Karnak ( Dev )')

        # Used to control the size of the window
        self.setMinimumSize(500, self.height())

        # Set the basic layout
        layout = QtWidgets.QVBoxLayout()
        layout.setAlignment(QtCore.Qt.AlignTop)
        layout.setSpacing(0)
        self.setLayout(layout)

        """
        Settings __tab
        """
        self.__tab_1 = QtWidgets.QWidget()
        self.__tab_edit = QtWidgets.QWidget()
        self.__tab_output = QtWidgets.QWidget()

        """
        Start set __menu_bar
        """
        __menu_bar = QtWidgets.QMenuBar(self)

        # 1
        __file_menu = __menu_bar.addMenu('檔案')

        __save_action = QtWidgets.QAction('儲存設定', self)
        __save_action.triggered.connect(self.push_settings)
        __load_action = QtWidgets.QAction('讀取設定', self)
        __load_action.triggered.connect(self.pull_settings)
        __reset_action = QtWidgets.QAction('TODO: 『恢復預設值』', self)
        __reset_action.setEnabled(False)

        __file_menu.addAction(__save_action)
        __file_menu.addAction(__load_action)
        __file_menu.addSeparator()
        __file_menu.addAction(__reset_action)

        # 2
        __help_menu = __menu_bar.addMenu('幫助')
        __language_menu = __help_menu.addMenu('選擇語系')

        __lang_zh_tw_action = QtWidgets.QAction('TODO: 『正體中文』', self)
        __lang_zh_tw_action.setEnabled(False)
        __lang_en_us_action = QtWidgets.QAction('TODO: 『英文』', self)
        __lang_en_us_action.setEnabled(False)
        __doc_action = QtWidgets.QAction('TODO: 『使用手冊』', self)
        __doc_action.setEnabled(False)

        __about_action = QtWidgets.QAction('關於 Karnak', self)
        __about_action.triggered.connect(self.show_about)

        __help_menu.addMenu(__language_menu)
        __help_menu.addSeparator()
        __help_menu.addAction(__doc_action)
        __help_menu.addAction(__about_action)

        __language_menu.addAction(__lang_zh_tw_action)
        __language_menu.addAction(__lang_en_us_action)

        self.layout().setMenuBar(__menu_bar)

        """
        Settings __scroll
        """
        self.__scroll_layout = QtWidgets.QVBoxLayout()
        self.__scroll_layout.setObjectName('scroll_layout')
        self.__scroll_layout.setContentsMargins(8, 8, 8, 8)
        self.__scroll_layout.setSpacing(6)
        self.__scroll_layout.setAlignment(QtCore.Qt.AlignTop)

        self.__scroll_widget = QtWidgets.QWidget()
        self.__scroll_widget.setLayout(self.__scroll_layout)

        self.__tab_new = QtWidgets.QScrollArea(self)
        self.__tab_new.setWidgetResizable(True)
        self.__tab_new.setWidget(self.__scroll_widget)

        """
        Settings __dummy_frame
        """
        self.__get_all_frames = []
        # 1
        self.__tutorial_frame = qt.FrameLayout(self)
        self.__get_all_frames.append(self.__tutorial_frame)
        self.__tutorial_frame.frame_btn.setText('教學')
        self.__tutorial_frame.frame_layout.setContentsMargins(0, 0, 0, 0)
        self.__scroll_layout.addWidget(self.__tutorial_frame)

        # 2
        self.__project_frame = qt.FrameLayout(self)
        self.__get_all_frames.append(self.__project_frame)
        self.__project_frame.frame_btn.setText('專案設定')
        self.__project_frame.frame_layout.setContentsMargins(0, 0, 0, 0)
        self.__scroll_layout.addWidget(self.__project_frame)

        # 4
        self.__xml_frame = qt.FrameLayout(self)
        self.__get_all_frames.append(self.__xml_frame)
        self.__xml_frame.frame_btn.setText('點位表')
        self.__xml_frame.frame_layout.setContentsMargins(0, 0, 0, 0)
        self.__scroll_layout.addWidget(self.__xml_frame)

        """
        Settings __frame_ui created by QtDesigner
        """

        # -- 教學 __tutorial_frame - 1 --
        loader = QtUiTools.QUiLoader()
        self.__tutorial_frame_ui = loader.load(proj_dir + '/ui/frame/tutorial.ui')
        self.__tutorial_frame_ui.setMinimumHeight(self.__tutorial_frame_ui.height())
        self.__tutorial_frame.frame_layout.addWidget(self.__tutorial_frame_ui)

        # -- 專案 __project_frame - 2 --
        loader = QtUiTools.QUiLoader()
        self.__project_frame_ui = loader.load(proj_dir + '/ui/frame/project.ui')
        self.__project_frame_ui.setMinimumHeight(self.__project_frame_ui.height())

        # [專案目錄 (location)]
        self.__project_frame_ui.location_le = QtWidgets.QLineEdit()
        self.__project_frame_ui.location_btn = QtWidgets.QPushButton()
        self.__project_frame_ui.location_btn.setMaximumSize(20, 20)
        self.__project_frame_ui.location_btn.setIcon(QtGui.QIcon(proj_dir + '/resources/folder.png'))
        self.__project_frame_ui.location_layout.addWidget(self.__project_frame_ui.location_le)
        self.__project_frame_ui.location_layout.addWidget(self.__project_frame_ui.location_btn)

        self.__project_frame_ui.location_le.textChanged.connect(self.push_location_directory)
        self.__project_frame_ui.location_btn.clicked.connect(self.browse_location)

        # [模型目錄 (resources)]
        self.__project_frame_ui.resources_le = QtWidgets.QLineEdit()
        self.__project_frame_ui.resources_btn = QtWidgets.QPushButton()
        self.__project_frame_ui.resources_btn.setMaximumSize(20, 20)
        self.__project_frame_ui.resources_btn.setIcon(QtGui.QIcon(proj_dir + '/resources/folder.png'))
        self.__project_frame_ui.resources_layout.addWidget(self.__project_frame_ui.resources_le)
        self.__project_frame_ui.resources_layout.addWidget(self.__project_frame_ui.resources_btn)

        self.__project_frame_ui.resources_le.textChanged.connect(self.push_resources_directory)
        self.__project_frame_ui.resources_btn.clicked.connect(self.browse_resources)

        # [模型列表 (resources_list)]
        self.__project_frame_ui.resources_list_lw = QtWidgets.QListWidget()
        self.__project_frame_ui.resources_list_btn = QtWidgets.QPushButton()
        self.__project_frame_ui.resources_list_lw.setFixedHeight(140)
        self.__project_frame_ui.resources_list_btn.setMaximumSize(20, 20)
        self.__project_frame_ui.resources_list_btn.setIcon(QtGui.QIcon(proj_dir + '/resources/switch_h.png'))
        self.__project_frame_ui.resources_list_lw.setSelectionMode(QtWidgets.QAbstractItemView.NoSelection)
        self.__project_frame_ui.resources_list_layout.addWidget(self.__project_frame_ui.resources_list_lw)
        self.__project_frame_ui.resources_list_layout.addWidget(self.__project_frame_ui.resources_list_btn)

        self.__project_frame_ui.resources_list_lw.currentItemChanged.connect(self.push_resources_list)
        self.__project_frame_ui.resources_list_btn.clicked.connect(self.switch_resources_list)

        # ---
        self.__project_frame.frame_layout.addWidget(self.__project_frame_ui)

        # -- 點位表 __xml_frame - 3 --
        loader = QtUiTools.QUiLoader()
        self.__xml_frame_ui = loader.load(proj_dir + '/ui/frame/xml.ui')
        self.__xml_frame_ui.setMinimumHeight(self.__xml_frame_ui.height())

        # [XML檔案 (xml)]
        self.__xml_frame_ui.xml_le = QtWidgets.QLineEdit()
        self.__xml_frame_ui.xml_btn = QtWidgets.QPushButton()
        self.__xml_frame_ui.xml_btn.setMaximumSize(20, 20)
        self.__xml_frame_ui.xml_btn.setIcon(QtGui.QIcon(proj_dir + '/resources/folder.png'))
        self.__xml_frame_ui.xml_layout.addWidget(self.__xml_frame_ui.xml_le)
        self.__xml_frame_ui.xml_layout.addWidget(self.__xml_frame_ui.xml_btn)

        self.__xml_frame_ui.xml_le.textChanged.connect(self.push_xml_directory)
        self.__xml_frame_ui.xml_btn.clicked.connect(self.browse_xml)
        self.pull_settings()

        # ---
        self.__xml_frame.frame_layout.addWidget(self.__xml_frame_ui)

        self.__tutorial_frame.frame_btn.toggle = False
        self.__project_frame.frame_btn.toggle = True
        # self.__project_frame.frame_btn.collapsed()
        # self.__resources_frame.frame_btn.toggle = False
        self.__xml_frame.frame_btn.toggle = True

        """
        Assemble __tab
        """
        # self.layout().addWidget(self.__scroll)
        self.__tab = QtWidgets.QTabWidget(self)
        self.__tab.addTab(self.__tab_new, '基本設定')
        self.__tab.addTab(self.__tab_edit, '編輯')
        self.__tab.addTab(self.__tab_output, '輸出')
        self.__tab.currentChanged.connect(self.validate_tab_index)
        self.layout().addWidget(self.__tab)

        """
        Bottom __prev_next_button
        """
        loader = QtUiTools.QUiLoader()
        self.__prev_next_common_ui = loader.load(proj_dir + '/ui/common/prev_next.ui')
        self.__prev_next_common_ui.setMinimumHeight(self.__prev_next_common_ui.height())
        self.__prev_next_common_ui.setMaximumHeight(self.__prev_next_common_ui.height())

        self.__prev_next_common_ui.prev_button.clicked.connect(self.goto_prev_tab)
        self.__prev_next_common_ui.next_button.clicked.connect(self.goto_next_tab)
        self.layout().addWidget(self.__prev_next_common_ui)

        self.validate_tab_index()

        self.current_step = 0

    def goto_next_tab(self):
        self.__tab.setCurrentIndex(self.__tab.currentIndex() + 1)
        self.validate_tab_index()

    def goto_prev_tab(self):
        self.__tab.setCurrentIndex(self.__tab.currentIndex() - 1)
        self.validate_tab_index()

    def validate_tab_index(self):
        self.__prev_next_common_ui.prev_button.setEnabled(False)
        self.__prev_next_common_ui.next_button.setEnabled(False)
        if self.__tab.currentIndex() > 0:
            self.__prev_next_common_ui.prev_button.setEnabled(True)
        if self.__tab.currentIndex() < 2:
            self.__prev_next_common_ui.next_button.setEnabled(True)
        self.__prev_next_common_ui.tab_label.setText(self.__tab.tabText(self.__tab.currentIndex()))

    def show_about(self):
        preferences_dialog = AboutDialog(self)
        result = preferences_dialog.exec_()

    def pull_location_directory(self):
        self.__project_frame_ui.location_le.setText(cmds.getAttr(settings + '.location'))

    def pull_resources_directory(self):
        self.__project_frame_ui.resources_le.setText(cmds.getAttr(settings + '.resources'))

    def pull_resources_list(self):
        self.resources_dict = json.loads(cmds.getAttr(settings + '.resources_list'))
        self.__project_frame_ui.resources_list_lw.clear()
        if cmds.getAttr(settings + '.resources_list_disp') == 'short':
            self.__project_frame_ui.resources_list_lw.addItems(self.resources_dict.keys())
        elif cmds.getAttr(settings + '.resources_list_disp') == 'long':
            self.__project_frame_ui.resources_list_lw.addItems(self.resources_dict.values())

    def pull_xml_directory(self):
        self.__xml_frame_ui.xml_le.setText(cmds.getAttr(settings + '.xml'))

    def pull_settings(self):
        self.pull_location_directory()
        self.pull_resources_directory()
        self.pull_resources_list()
        self.pull_xml_directory()

    def push_location_directory(self):
        cmds.setAttr(settings + '.location', self.__project_frame_ui.location_le.text(), type='string')

    def push_resources_directory(self):
        cmds.setAttr(settings + '.resources', self.__project_frame_ui.resources_le.text(), type='string')

    def push_resources_list(self):
        cmds.setAttr(settings + '.resources_list', json.dumps(self.resources_dict), type='string')

    def push_xml_directory(self):
        cmds.setAttr(settings + '.xml', self.__xml_frame_ui.xml_le.text(), type='string')

    def push_settings(self):
        self.push_location_directory()
        self.push_resources_directory()
        self.push_resources_list()
        self.push_xml_directory()

    def browse_location(self):
        path = pm.fileDialog2(fileMode=3)[0]
        self.__project_frame_ui.location_le.setText(path)

        if self.__project_frame_ui.location_le is not None:
            self.__project_frame_ui.location_le.setText(path)

    def browse_resources(self):
        path = pm.fileDialog2(fileMode=3)[0]
        self.__project_frame_ui.resources_le.setText(path)

        if self.__project_frame_ui.resources_le is not None:
            self.__project_frame_ui.resources_le.setText(path)

        values = common.list_files(path, 'fbx')
        keys = common.basenames(values)

        self.resources_dict = common.rebind_dict(keys, values)

        self.push_resources_list()
        self.pull_resources_list()

    def switch_resources_list(self):
        if cmds.getAttr(settings + '.resources_list_disp') == 'short':
            cmds.setAttr(settings + '.resources_list_disp', 'long', type='string')
        elif cmds.getAttr(settings + '.resources_list_disp') == 'long':
            cmds.setAttr(settings + '.resources_list_disp', 'short', type='string')
        self.pull_resources_list()

    def browse_xml(self):
        def get_path():
            return pm.fileDialog2(fileMode=1)[0]

        def set_attrs(__path):
            def push_path_attr():
                if self.__xml_frame_ui.xml_le is not None:
                    self.__xml_frame_ui.xml_le.setText(__path)

            def push_data_attr():
                f = io.open(__path, mode='r', encoding='utf-16')
                r = f.read()
                cmds.setAttr(settings + '.xml_data', r, type='string')

            push_path_attr()
            push_data_attr()

        path = get_path()
        set_attrs(path)

        # directory = os.path.dirname(path)
        #
        # tree = ET.parse(path)
        # root = tree.getroot()
        #
        # data = {}

        # for elem, path in self.etree_iter_path(root):
        #     if elem.tag == 'Object':
        #         name = elem.get('name')
        #         if elem.get('type') == 'Device':
        #             cmds.spaceLocator(name=name)
        #         else:
        #             cmds.group(em=True, name=name)
        #
        #         # Initial data.
        #         px, py, pz = 0, 0, 0
        #         rx, ry, rz = 0, 0, 0
        #         sx, sy, sz = 1, 0, 1
        #
        #         tr_exist = elem.find('Transform') if elem.find('Transform') else None
        #         if tr_exist and elem is not None:
        #             for tr in elem.find('Transform'):
        #                 if tr.tag == 'position':
        #                     px = tr.attrib['x'] if tr.attrib['x'] else 0
        #                     py = tr.attrib['y'] if tr.attrib['y'] else 0
        #                     pz = tr.attrib['z'] if tr.attrib['z'] else 0
        #                 elif tr.tag == 'rotation':
        #                     rx = tr.attrib['x'] if tr.attrib['x'] else 0
        #                     ry = tr.attrib['y'] if tr.attrib['y'] else 0
        #                     rz = tr.attrib['z'] if tr.attrib['z'] else 0
        #                 elif tr.tag == 'scale':
        #                     sx = tr.attrib['x'] if tr.attrib['x'] else 1
        #                     sy = tr.attrib['y'] if tr.attrib['y'] else 1
        #                     sz = tr.attrib['z'] if tr.attrib['z'] else 1
        #
        #         dict_data = {
        #             'name': name,
        #             'uuid': cmds.ls(name, uuid=True)[0],
        #             'position': (px, py, pz),
        #             'rotation': (rx, ry, rz),
        #             'scale': (sx, sy, sz)
        #         }
        #         data[path] = dict_data
        #
        #         current = renaming(data[path])
        #         cmds.rename(name, current)
        #         cmds.move(px, py, pz, current)
        #         cmds.rotate(rx, ry, rz, current)
        #         # cmds.scale( sx, sy, sz, current )
        #
        #         cmds.addAttr(current, longName='bundle', dataType='string')
        #         cmds.addAttr(current, longName='time', dataType='string')
        #         try:
        #             bundle = elem.get('bundle')
        #             time = elem.get('time')
        #             cmds.setAttr('{}.bundle'.format(current), bundle, type='string')
        #             cmds.setAttr('{}.time'.format(current), time, type='string')
        #             # cmds.deleteAttr( current, attribute='greenBow' )
        #         except:
        #             # cmds.addAttr( current, longName='bundle', dataType='string' )
        #             None
        #
        #         par_path = '{}'.format(re.split('/' + name, path)[0])
        #         parent = renaming(data[par_path])
        #         cmds.parent(current, parent)

    # def load_project_path(self):
    #     try:
    #         xmlfile = pm.fileDialog2(fileMode=1)[0]
    #         if not xmlfile.split('.')[-1] == 'xml':
    #             print("檔案類型錯誤: 請選擇XML檔案")
    #             self.nfo_f_ct_le.setText(u'檔案類型錯誤: 請選擇XML檔案')
    #             self.nfo_f_ct_le.setStyleSheet('background-color: rgb(196, 50, 44); color: rgb(0, 0, 0);')
    #             return
    #         print(u"已選擇的XML: \'{}\'".format(xmlfile))
    #         print("正在匯入 XML檔案 從 ...")
    #     except TypeError:
    #         print("操作錯誤: 使用者已取消")
    #         self.nfo_f_ct_le.setText(u'操作錯誤: 使用者已取消')
    #         self.nfo_f_ct_le.setStyleSheet('background-color: rgb(196, 50, 44); color: rgb(0, 0, 0);')
    #         return
    #     except:
    #         print("未知錯誤: 發生未知的錯誤")
    #         self.nfo_f_ct_le.setText(u'未知錯誤: 發生未知的錯誤')
    #         self.nfo_f_ct_le.setStyleSheet('background-color: rgb(196, 50, 44); color: rgb(0, 0, 0);')
    #         return


if __name__ == "__main__":
    try:
        win.close()
        win.deleteLater()

    except AttributeError:
        print("AttributeError: Will skip")
    except NameError:
        print("NameError: Will initialize new dialog")
        win = FrameLayoutWidget()
    except RuntimeError:
        print("RuntimeError: Will initialize new dialog")
        win = FrameLayoutWidget()

    win = FrameLayoutWidget()
    win.update()
    win.show(dockable=True, area='left')
