# -*- coding: utf-8 -*-
from __future__ import print_function, division, absolute_import

import functools
import os

import pymel.core as pm
import maya.cmds as cmds

from PySide2 import QtCore, QtGui, QtWidgets, QtUiTools
from maya.app.general import mayaMixin

from python.eil.util import common, qt, io
from python.eil.mixin import menu

import glob

widget_id = 'Karnak ( Dev )'
ui_path = "C:/Users/eos/PycharmProjects/karnak/python/eil/tool/karnak/ui"


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

        # self.create_connection()

        loader = QtUiTools.QUiLoader()
        __about_menu_ui = loader.load("{0}/{1}/{2}".format(ui_path, 'menu', 'about.ui'))
        __about_menu_ui.setMinimumHeight(__about_menu_ui.height())

        __about_menu_ui.ok_button.clicked.connect(self.close)

        self.layout().addWidget(__about_menu_ui)

    # def create_connection(self):
    #     self.ui.okButton.clicked.connect(self.accept)
    #     self.ui.cancelButton.clicked.connect(self.close)

    def get_option_a(self):
        return self.ui.checkBoxA.isChecked()

    def get_option_b(self):
        return self.ui.checkBoxB.isChecked()

    def get_option_c(self):
        return self.ui.checkBoxC.isChecked()


class FrameLayoutWidget(mayaMixin.MayaQWidgetDockableMixin, mayaMixin.MayaQWidgetBaseMixin, qt.QtDefaultWidget):
    def __init__(self, parent=qt.maya_main_window()):
        super(FrameLayoutWidget, self).__init__(parent)
        self.resources_dicts = {}
        self.setWindowTitle(widget_id)

        # Used to control the size of the window
        self.setMinimumSize(430, self.height())

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

        __save_action = QtWidgets.QAction('TODO: 『儲存設定』', self)
        __save_action.setEnabled(False)
        __load_action = QtWidgets.QAction('TODO: 『讀取設定』', self)
        __load_action.setEnabled(False)
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
        # self.__tab_new.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
        # self.__tab_new.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
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
        # # layout
        # self.__introduction_frame_layout = QtWidgets.QVBoxLayout()
        # self.__introduction_frame_layout.setObjectName('scroll_layout')
        # self.__introduction_frame_layout.setContentsMargins(16, 6, 0, 0)
        # self.__introduction_frame_layout.setAlignment(QtCore.Qt.AlignTop)
        #
        # # 1.1
        # self.__XXXX_frame = qt.FrameLayout(self)
        # self.__XXXX_frame.frame_btn.setText('XXXX')
        # # self.__XXXX_frame.frame_layout.setContentsMargins(0, 0, 0, 0)
        # self.__XXXX_frame.frame_layout.setContentsMargins(0, 3, 0, 3)
        # self.__introduction_frame_layout.addWidget(self.__XXXX_frame)
        #
        # self.__introduction_frame.frame_layout.addLayout(self.__introduction_frame_layout)

        # 2
        self.__project_frame = qt.FrameLayout(self)
        self.__get_all_frames.append(self.__project_frame)
        self.__project_frame.frame_btn.setText('專案')
        self.__project_frame.frame_layout.setContentsMargins(0, 0, 0, 0)
        self.__scroll_layout.addWidget(self.__project_frame)

        # 3
        self.__resources_frame = qt.FrameLayout(self)
        self.__get_all_frames.append(self.__resources_frame)
        self.__resources_frame.frame_btn.setText('資源')
        self.__resources_frame.frame_layout.setContentsMargins(0, 0, 0, 0)
        self.__scroll_layout.addWidget(self.__resources_frame)

        # 4
        self.__nodetree_frame = qt.FrameLayout(self)
        self.__get_all_frames.append(self.__nodetree_frame)
        self.__nodetree_frame.frame_btn.setText('點位表')
        self.__nodetree_frame.frame_layout.setContentsMargins(0, 0, 0, 0)
        self.__scroll_layout.addWidget(self.__nodetree_frame)

        """
        Settings __frame_ui created by QtDesigner
        """

        # 1
        loader = QtUiTools.QUiLoader()
        self.__tutorial_frame_ui = loader.load("{0}/{1}/{2}".format(ui_path, 'frame', 'tutorial.ui'))
        self.__tutorial_frame_ui.setMinimumHeight(self.__tutorial_frame_ui.height())
        self.__tutorial_frame.frame_layout.addWidget(self.__tutorial_frame_ui)

        # # 1.1
        # loader = QtUiTools.QUiLoader()
        # __XXXX_frame_ui = loader.load("{0}/{1}/{2}".format(ui_path, 'frame', 'short.ui'))
        # __XXXX_frame_ui.setMinimumHeight(__XXXX_frame_ui.height())
        #
        # self.__XXXX_frame.frame_layout.addWidget(__XXXX_frame_ui)

        # 2 __project_frame
        loader = QtUiTools.QUiLoader()
        self.__project_frame_ui = loader.load("{0}/{1}/{2}".format(ui_path, 'frame', 'project.ui'))
        self.__project_frame_ui.setMinimumHeight(self.__project_frame_ui.height())

        # Project Directory
        self.__project_frame_ui.project_path_lineedit = QtWidgets.QLineEdit()
        self.__project_frame_ui.project_path_lineedit.setReadOnly(True)
        self.__project_frame_ui.project_path_button = QtWidgets.QPushButton()
        self.__project_frame_ui.project_path_button.setText('...')
        self.__project_frame_ui.project_path_layout.addWidget(self.__project_frame_ui.project_path_lineedit)
        self.__project_frame_ui.project_path_layout.addWidget(self.__project_frame_ui.project_path_button)

        # self.__project_frame_ui.resource_detail_frame.setEnabled(False)

        # avoid GC
        self.__project_frame_ui.project_name_lineedit = QtWidgets.QLineEdit()
        self.__project_frame_ui.project_name_lineedit.setReadOnly(True)
        self.__project_frame_ui.detail_layout.addWidget(self.__project_frame_ui.project_name_lineedit)

        self.__project_frame_ui.project_path_button.clicked.connect(self.load_project_path)
        self.__project_frame.frame_layout.addWidget(self.__project_frame_ui)

        # 3 __resources_frame
        loader = QtUiTools.QUiLoader()
        self.__resources_frame_ui = loader.load("{0}/{1}/{2}".format(ui_path, 'frame', 'resources.ui'))
        self.__resources_frame_ui.setMinimumHeight(self.__resources_frame_ui.height())

        # avoid GC
        self.__resources_frame_ui.resources_path_lineedit = QtWidgets.QLineEdit()
        self.__resources_frame_ui.resources_path_lineedit.setEnabled(False)
        self.__resources_frame_ui.resources_path_lineedit.setReadOnly(True)
        self.__resources_frame_ui.resources_path_button = QtWidgets.QPushButton()
        self.__resources_frame_ui.resources_path_button.setText('...')
        self.__resources_frame_ui.resources_path_layout.addWidget(self.__resources_frame_ui.resources_path_lineedit)
        self.__resources_frame_ui.resources_path_layout.addWidget(self.__resources_frame_ui.resources_path_button)

        # self.__project_frame_ui.resource_detail_frame.setEnabled(False)

        # avoid GC
        self.__resources_frame_ui.resources_name_label = QtWidgets.QLabel()
        self.__resources_frame_ui.resources_name_label.setText('Resources')
        self.__resources_frame_ui.resources_name_label.setFixedWidth(64)
        self.__resources_frame_ui.resources_name_label.setEnabled(False)
        self.__resources_frame_ui.resources_name_lineedit = QtWidgets.QLineEdit()
        self.__resources_frame_ui.resources_name_lineedit.setReadOnly(True)
        self.__resources_frame_ui.resources_name_layout.addWidget(self.__resources_frame_ui.resources_name_label)
        # self.__project_frame_ui.resources_name_layout.addWidget(self.__project_frame_ui.resources_name_lineedit)

        self.resources_list_widget = QtWidgets.QListWidget()
        self.resources_list_widget.setFixedHeight(128)
        # self.resources_list_widget.addItems(cmds.ls(type='transform'))
        # self.resources_list_widget.itemClicked.connect(self.selectInListWidget)
        self.__resources_frame_ui.resources_name_layout.addWidget(self.resources_list_widget)

        self.__resources_frame_ui.resources_path_button.clicked.connect(self.load_resources_path)
        self.__resources_frame.frame_layout.addWidget(self.__resources_frame_ui)

        # 4
        loader = QtUiTools.QUiLoader()
        __nodetree_frame_ui = loader.load("{0}/{1}/{2}".format(ui_path, 'frame', 'node_tree.ui'))
        __nodetree_frame_ui.setMinimumHeight(__nodetree_frame_ui.height())
        self.__nodetree_frame.frame_layout.addWidget(__nodetree_frame_ui)

        self.__tutorial_frame.frame_btn.toggle = False
        self.__project_frame.frame_btn.toggle = True
        # self.__project_frame.frame_btn.collapsed()
        self.__resources_frame.frame_btn.toggle = False
        self.__nodetree_frame.frame_btn.toggle = False

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
        self.__prev_next_common_ui = loader.load("{0}/{1}/{2}".format(ui_path, 'common', 'prev_next.ui'))
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

    def load_project_path(self):
        path = pm.fileDialog2(fileMode=3)[0]
        self.__project_frame_ui.project_path_lineedit.setText(path)

        if self.__project_frame_ui.project_path_lineedit is not None:
            self.__project_frame_ui.project_name_label.setEnabled(True)
            self.__project_frame_ui.project_name_lineedit.setText(io.basename(path))

    def load_resources_path(self):
        path = pm.fileDialog2(fileMode=3)[0]
        self.__project_frame_ui.resources_path_lineedit.setText(path)
        if self.__project_frame_ui.resources_path_lineedit is not None:
            self.__project_frame_ui.resources_name_label.setEnabled(True)
            self.__project_frame_ui.resources_name_lineedit.setText(io.basename(path))

        values = io.list_files(path, 'fbx')
        keys = io.basenames(values)

        self.resources_dicts = common.rebind_dict(keys, values)

        self.resources_list_widget.clear()
        self.resources_list_widget.addItems(self.resources_dicts.keys())

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
