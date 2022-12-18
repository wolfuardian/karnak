# -*- coding: utf-8 -*-
import pymel.core as pm
import maya.cmds as cmds
import xml.etree.ElementTree as ET
import os
import re
import json
import copy
import tempfile
import PySide2.QtCore as qc
import PySide2.QtWidgets as qw
import PySide2.QtGui as qg
import subprocess
import locale

version = '0.2.5-Alpha'

windows_title = u'Point Editor {} (Karnak)'.format(version)
print(u'windows_title = {}'.format(windows_title))
windows_id = 'XML_PDT_ID'

window = qw.QApplication.activeWindow()
for child in qw.QApplication.activeWindow().children():
    if child.objectName() == windows_id:
        child.deleteLater()

f = tempfile.TemporaryFile()

dialog = None


# Qt ui nameing guideline.
# f = frame, ct = context.
# ----------------------------------------------------------------------------------------- #
class MainWindow(qw.QMainWindow):
    def __init__(self, parent=qw.QApplication.activeWindow()):
        super(MainWindow, self).__init__(parent)
        self.setObjectName(windows_id)
        self.setWindowTitle(windows_title)
        self.setFixedWidth(720)
        # self.setSizePolicy(qw.QSizePolicy.Minimum, qw.QSizePolicy.Fixed)

        self.setLayout(qw.QVBoxLayout())
        self.layout().setContentsMargins(8, 8, 8, 8)
        self.layout().setSpacing(8)
        self.layout().setAlignment(qc.Qt.AlignTop)

        # ----------------------------------------------------------------------------------------- #
        # io
        self.io_f = qw.QFrame()
        self.io_f.setFrameStyle(qw.QFrame.NoFrame)
        self.io_f.setSizePolicy(qw.QSizePolicy.Minimum, qw.QSizePolicy.Fixed)
        self.layout().addWidget(self.io_f)

        self.io_f.setLayout(qw.QVBoxLayout())
        self.io_f.layout().setContentsMargins(0, 0, 0, 0)
        self.io_f.layout().setSpacing(8)  # Label spacing to context

        self.io_f_lb = qw.QLabel()
        self.io_f_lb.setFrameStyle(qw.QFrame.NoFrame)
        self.io_f_lb.setText(u'檔案操作')
        self.io_f_lb.setStyleSheet('color: rgb(120, 120, 120);')
        self.io_f_lb.setAlignment(qc.Qt.AlignHCenter | qc.Qt.AlignVCenter)
        self.io_f_lb.setFixedHeight(16)
        self.io_f.layout().addWidget(self.io_f_lb)

        self.io_f_ct = qw.QFrame()
        self.io_f_ct.setFrameStyle(qw.QFrame.NoFrame)
        self.io_f_ct.setSizePolicy(qw.QSizePolicy.Minimum, qw.QSizePolicy.Fixed)
        self.io_f.layout().addWidget(self.io_f_ct)

        self.io_f_ct.setLayout(qw.QHBoxLayout())
        self.io_f_ct.layout().setContentsMargins(0, 0, 0, 0)
        self.io_f_ct.layout().setSpacing(8)

        self.io_f_ct_select_root_btn = qw.QPushButton(u'Select Root')
        self.io_f_ct_select_root_btn.setFixedHeight(36)
        self.io_f_ct_select_root_btn.clicked.connect(self.XMLImportCallback)

        self.io_f_ct.layout().addWidget(self.io_f_ct_select_root_btn)

        self.io_f_ct_import_btn = qw.QPushButton(u'匯入 XML')
        self.io_f_ct_import_btn.setFixedHeight(36)
        self.io_f_ct_import_btn.clicked.connect(self.XMLImportCallback)

        self.io_f_ct.layout().addWidget(self.io_f_ct_import_btn)

        self.io_f_ct_export_btn = qw.QPushButton(u'儲存 XML')
        self.io_f_ct_export_btn.setFixedHeight(36)
        self.io_f_ct_export_btn.clicked.connect(self.XMLSaveCallback)
        self.io_f.layout().addWidget(self.io_f_ct_export_btn)

        # ----------------------------------------------------------------------------------------- #

        # ----------------------------------------------------------------------------------------- #
        # nfo
        self.nfo_f = qw.QFrame()
        self.nfo_f.setFrameStyle(qw.QFrame.NoFrame)
        self.nfo_f.setSizePolicy(qw.QSizePolicy.Minimum, qw.QSizePolicy.Fixed)
        self.layout().addWidget(self.nfo_f)

        self.nfo_f.setLayout(qw.QVBoxLayout())
        self.nfo_f.layout().setContentsMargins(0, 0, 0, 0)
        self.nfo_f.layout().setSpacing(8)  # Label spacing to context

        self.nfo_f_ct = qw.QFrame()
        self.nfo_f_ct.setFrameStyle(qw.QFrame.NoFrame)
        self.nfo_f_ct.setSizePolicy(qw.QSizePolicy.Minimum, qw.QSizePolicy.Fixed)
        self.nfo_f.layout().addWidget(self.nfo_f_ct)

        self.nfo_f_ct.setLayout(qw.QVBoxLayout())
        self.nfo_f_ct.layout().setContentsMargins(0, 0, 0, 0)
        self.nfo_f_ct.layout().setSpacing(0)

        self.nfo_f_ct_le = qw.QLineEdit()
        self.nfo_f_ct_le.setTextMargins(8, 0, 8, 0)
        self.nfo_f_ct_le.setReadOnly(True)
        self.nfo_f_ct_le.setText(u'請選擇 OCMS點位資訊檔案(XML) 的存放位置 ...')
        self.nfo_f_ct_le.setStyleSheet('background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);')
        # info_le.setStyleSheet('background-color: rgb(196, 50, 44); color: rgb(0, 0, 0);')
        self.nfo_f_ct.layout().addWidget(self.nfo_f_ct_le)

        self.nfo_f_ct_lw = qw.QListWidget()
        self.nfo_f_ct_lw.setFixedHeight(128)
        self.nfo_f_ct_lw.addItems(cmds.ls(type='transform'))
        self.nfo_f_ct_lw.itemClicked.connect(self.selectInListWidget)
        self.nfo_f_ct.layout().addWidget(self.nfo_f_ct_lw)
        # selectInTextList
        # ----------------------------------------------------------------------------------------- #

        # ----------------------------------------------------------------------------------------- #
        # set
        self.set_f = qw.QFrame()
        self.set_f.setFrameStyle(qw.QFrame.NoFrame)
        self.set_f.setSizePolicy(qw.QSizePolicy.Minimum, qw.QSizePolicy.Fixed)
        self.layout().addWidget(self.set_f)

        self.set_f.setLayout(qw.QVBoxLayout())
        self.set_f.layout().setContentsMargins(0, 0, 0, 0)
        self.set_f.layout().setSpacing(8)  # Label spacing to context

        self.set_f_lb = qw.QLabel()
        self.set_f_lb.setFrameStyle(qw.QFrame.NoFrame)
        self.set_f_lb.setText(u'設定點位屬性')
        self.set_f_lb.setStyleSheet('color: rgb(120, 120, 120);')
        self.set_f_lb.setAlignment(qc.Qt.AlignHCenter | qc.Qt.AlignVCenter)
        self.set_f_lb.setFixedHeight(16)
        self.set_f.layout().addWidget(self.set_f_lb)

        self.set_f_ct = qw.QFrame()
        self.set_f_ct.setFrameStyle(qw.QFrame.NoFrame)
        self.set_f.layout().addWidget(self.set_f_ct)

        self.set_f_ct.setLayout(qw.QVBoxLayout())
        self.set_f_ct.layout().setContentsMargins(0, 0, 0, 0)
        self.set_f_ct.layout().setSpacing(0)

        # ----------------------------------------------------------------------------------------- #
        # [type]
        self.set_f_ct_type_f = qw.QFrame()
        self.set_f_ct_type_f.setFrameStyle(qw.QFrame.NoFrame)
        self.set_f_ct.layout().addWidget(self.set_f_ct_type_f)

        self.set_f_ct_type_f.setLayout(qw.QHBoxLayout())
        self.set_f_ct_type_f.layout().setContentsMargins(0, 0, 0, 0)
        self.set_f_ct_type_f.layout().setSpacing(8)

        self.set_f_ct_type_f_lb = qw.QLabel()
        self.set_f_ct_type_f_lb.setText(u'Type')
        self.set_f_ct_type_f_lb.setAlignment(qc.Qt.AlignRight | qc.Qt.AlignVCenter)
        self.set_f_ct_type_f.layout().addWidget(self.set_f_ct_type_f_lb)

        self.set_f_ct_type_f_cb = qw.QComboBox()
        self.set_f_ct_type_f_cb.addItems(['Building', 'Floor', 'Device'])
        self.set_f_ct_type_f_cb.setCurrentText('Device')
        self.set_f_ct_type_f_cb.setFixedWidth(416)
        self.set_f_ct_type_f.layout().addWidget(self.set_f_ct_type_f_cb)
        # ----------------------------------------------------------------------------------------- #

        # ----------------------------------------------------------------------------------------- #
        # [name]
        self.set_f_ct_name_f = qw.QFrame()
        self.set_f_ct_name_f.setFrameStyle(qw.QFrame.NoFrame)
        self.set_f_ct.layout().addWidget(self.set_f_ct_name_f)

        self.set_f_ct_name_f.setLayout(qw.QHBoxLayout())
        self.set_f_ct_name_f.layout().setContentsMargins(0, 0, 0, 0)
        self.set_f_ct_name_f.layout().setSpacing(8)

        self.set_f_ct_name_f_lb = qw.QLabel()
        self.set_f_ct_name_f_lb.setText(u'Name')
        self.set_f_ct_name_f_lb.setAlignment(qc.Qt.AlignRight | qc.Qt.AlignVCenter)
        self.set_f_ct_name_f.layout().addWidget(self.set_f_ct_name_f_lb)

        self.set_f_ct_name_f_cb = qw.QLineEdit()
        self.set_f_ct_name_f_cb.setFixedWidth(416)
        self.set_f_ct_name_f.layout().addWidget(self.set_f_ct_name_f_cb)
        # ----------------------------------------------------------------------------------------- #

        # ----------------------------------------------------------------------------------------- #
        # [alias]
        self.set_f_ct_alias_f = qw.QFrame()
        self.set_f_ct_alias_f.setFrameStyle(qw.QFrame.NoFrame)
        self.set_f_ct.layout().addWidget(self.set_f_ct_alias_f)

        self.set_f_ct_alias_f.setLayout(qw.QHBoxLayout())
        self.set_f_ct_alias_f.layout().setContentsMargins(0, 0, 0, 0)
        self.set_f_ct_alias_f.layout().setSpacing(8)

        self.set_f_ct_alias_f_lb = qw.QLabel()
        self.set_f_ct_alias_f_lb.setText(u'Alias')
        self.set_f_ct_alias_f_lb.setAlignment(qc.Qt.AlignRight | qc.Qt.AlignVCenter)
        self.set_f_ct_alias_f.layout().addWidget(self.set_f_ct_alias_f_lb)

        self.set_f_ct_alias_f_cb = qw.QLineEdit()
        self.set_f_ct_alias_f_cb.setFixedWidth(416)
        self.set_f_ct_alias_f.layout().addWidget(self.set_f_ct_alias_f_cb)
        # ----------------------------------------------------------------------------------------- #

        # ----------------------------------------------------------------------------------------- #
        # [id]
        self.set_f_ct_id_f = qw.QFrame()
        self.set_f_ct_id_f.setFrameStyle(qw.QFrame.NoFrame)
        self.set_f_ct.layout().addWidget(self.set_f_ct_id_f)

        self.set_f_ct_id_f.setLayout(qw.QHBoxLayout())
        self.set_f_ct_id_f.layout().setContentsMargins(0, 0, 0, 0)
        self.set_f_ct_id_f.layout().setSpacing(8)

        self.set_f_ct_id_f_lb = qw.QLabel()
        self.set_f_ct_id_f_lb.setText(u'ID')
        self.set_f_ct_id_f_lb.setAlignment(qc.Qt.AlignRight | qc.Qt.AlignVCenter)
        self.set_f_ct_id_f.layout().addWidget(self.set_f_ct_id_f_lb)

        self.set_f_ct_id_f_cb = qw.QLineEdit()
        self.set_f_ct_id_f_cb.setFixedWidth(416)
        self.set_f_ct_id_f.layout().addWidget(self.set_f_ct_id_f_cb)
        # ----------------------------------------------------------------------------------------- #

        # ----------------------------------------------------------------------------------------- #
        # [model]
        self.set_f_ct_model_f = qw.QFrame()
        self.set_f_ct_model_f.setFrameStyle(qw.QFrame.NoFrame)
        self.set_f_ct.layout().addWidget(self.set_f_ct_model_f)

        self.set_f_ct_model_f.setLayout(qw.QHBoxLayout())
        self.set_f_ct_model_f.layout().setContentsMargins(0, 0, 0, 0)
        self.set_f_ct_model_f.layout().setSpacing(8)

        self.set_f_ct_model_f_lb = qw.QLabel()
        self.set_f_ct_model_f_lb.setText(u'Model')
        self.set_f_ct_model_f_lb.setAlignment(qc.Qt.AlignRight | qc.Qt.AlignVCenter)
        self.set_f_ct_model_f.layout().addWidget(self.set_f_ct_model_f_lb)

        self.set_f_ct_model_f_cb = qw.QLineEdit()
        self.set_f_ct_model_f_cb.setFixedWidth(416)
        self.set_f_ct_model_f.layout().addWidget(self.set_f_ct_model_f_cb)
        # ----------------------------------------------------------------------------------------- #

        # ----------------------------------------------------------------------------------------- #
        # [bundle]
        self.set_f_ct_bundle_f = qw.QFrame()
        self.set_f_ct_bundle_f.setFrameStyle(qw.QFrame.NoFrame)
        self.set_f_ct.layout().addWidget(self.set_f_ct_bundle_f)

        self.set_f_ct_bundle_f.setLayout(qw.QHBoxLayout())
        self.set_f_ct_bundle_f.layout().setContentsMargins(0, 0, 0, 0)
        self.set_f_ct_bundle_f.layout().setSpacing(8)

        self.set_f_ct_bundle_f_lb = qw.QLabel()
        self.set_f_ct_bundle_f_lb.setText(u'Bundle')
        self.set_f_ct_bundle_f_lb.setAlignment(qc.Qt.AlignRight | qc.Qt.AlignVCenter)
        self.set_f_ct_bundle_f.layout().addWidget(self.set_f_ct_bundle_f_lb)

        self.set_f_ct_bundle_f_cb = qw.QLineEdit()
        self.set_f_ct_bundle_f_cb.setFixedWidth(416)
        self.set_f_ct_bundle_f.layout().addWidget(self.set_f_ct_bundle_f_cb)
        # ----------------------------------------------------------------------------------------- #

        # ----------------------------------------------------------------------------------------- #
        # [time]
        self.set_f_ct_time_f = qw.QFrame()
        self.set_f_ct_time_f.setFrameStyle(qw.QFrame.NoFrame)
        self.set_f_ct.layout().addWidget(self.set_f_ct_time_f)

        self.set_f_ct_time_f.setLayout(qw.QHBoxLayout())
        self.set_f_ct_time_f.layout().setContentsMargins(0, 0, 0, 0)
        self.set_f_ct_time_f.layout().setSpacing(8)

        self.set_f_ct_time_f_lb = qw.QLabel()
        self.set_f_ct_time_f_lb.setText(u'Time')
        self.set_f_ct_time_f_lb.setAlignment(qc.Qt.AlignRight | qc.Qt.AlignVCenter)
        self.set_f_ct_time_f.layout().addWidget(self.set_f_ct_time_f_lb)

        self.set_f_ct_time_f_cb = qw.QLineEdit()
        self.set_f_ct_time_f_cb.setFixedWidth(416)
        self.set_f_ct_time_f.layout().addWidget(self.set_f_ct_time_f_cb)
        # ----------------------------------------------------------------------------------------- #

        # ----------------------------------------------------------------------------------------- #
        # [noted]
        self.set_f_ct_noted_f = qw.QFrame()
        self.set_f_ct_noted_f.setFrameStyle(qw.QFrame.NoFrame)
        self.set_f_ct.layout().addWidget(self.set_f_ct_noted_f)

        self.set_f_ct_noted_f.setLayout(qw.QHBoxLayout())
        self.set_f_ct_noted_f.layout().setContentsMargins(0, 0, 0, 0)
        self.set_f_ct_noted_f.layout().setSpacing(8)

        self.set_f_ct_noted_f_lb = qw.QLabel()
        self.set_f_ct_noted_f_lb.setText(u'Noted')
        self.set_f_ct_noted_f_lb.setAlignment(qc.Qt.AlignRight | qc.Qt.AlignVCenter)
        self.set_f_ct_noted_f.layout().addWidget(self.set_f_ct_noted_f_lb)

        self.set_f_ct_noted_f_cb = qw.QLineEdit()
        self.set_f_ct_noted_f_cb.setFixedWidth(416)
        self.set_f_ct_noted_f.layout().addWidget(self.set_f_ct_noted_f_cb)
        # ----------------------------------------------------------------------------------------- #

        # ----------------------------------------------------------------------------------------- #
        # edit
        self.edit_f = qw.QFrame()
        self.edit_f.setFrameStyle(qw.QFrame.NoFrame)
        self.edit_f.setSizePolicy(qw.QSizePolicy.Minimum, qw.QSizePolicy.Fixed)
        self.layout().addWidget(self.edit_f)

        self.edit_f.setLayout(qw.QVBoxLayout())
        self.edit_f.layout().setContentsMargins(0, 0, 0, 0)
        self.edit_f.layout().setSpacing(8)  # Label spacing to context

        self.edit_f_lb = qw.QLabel()
        self.edit_f_lb.setFrameStyle(qw.QFrame.NoFrame)
        self.edit_f_lb.setText(u'已新增 / 修改點位')
        self.edit_f_lb.setStyleSheet('color: rgb(120, 120, 120);')
        self.edit_f_lb.setAlignment(qc.Qt.AlignHCenter | qc.Qt.AlignVCenter)
        self.edit_f_lb.setFixedHeight(16)
        self.edit_f.layout().addWidget(self.edit_f_lb)

        self.edit_f_ct = qw.QFrame()
        self.edit_f_ct.setFrameStyle(qw.QFrame.NoFrame)
        self.edit_f_ct.setSizePolicy(qw.QSizePolicy.Minimum, qw.QSizePolicy.Fixed)
        self.edit_f.layout().addWidget(self.edit_f_ct)

        self.edit_f_ct.setLayout(qw.QHBoxLayout())
        self.edit_f_ct.layout().setContentsMargins(0, 0, 0, 0)
        self.edit_f_ct.layout().setSpacing(8)

        self.edit_f_ct_vis_all_btn = qw.QPushButton(u'標示所有')
        self.edit_f_ct_vis_all_btn.setFixedHeight(36)
        # self.edit_f_ct_vis_all_btn.clicked.connect(self.aaaaa)
        self.edit_f_ct.layout().addWidget(self.edit_f_ct_vis_all_btn)

        self.edit_f_ct_del_all_btn = qw.QPushButton(u'刪除所有')
        self.edit_f_ct_del_all_btn.setFixedHeight(36)
        self.edit_f_ct_del_all_btn.clicked.connect(self.Debug_DelNewItems)
        self.edit_f_ct.layout().addWidget(self.edit_f_ct_del_all_btn)
        # ----------------------------------------------------------------------------------------- #

        self.cancel_btn = qw.QPushButton(u'取消')
        self.cancel_btn.setFixedHeight(36)
        self.cancel_btn.setFixedHeight(36)
        self.cancel_btn.clicked.connect(self.cancelCallback)

        self.layout().addWidget(self.cancel_btn)

    def etree_iter_path(self, node, tag=None, path='.'):
        if tag == '*':
            tag = None
        if tag is None or node.tag == tag:
            yield node, path
        for child in node:
            _child_path = '%s/%s' % (path, child.get('name'))
            for child, child_path in self.etree_iter_path(child, tag, path=_child_path):
                yield child, child_path

    def update_XML(self, data):
        # Load from temporaryFile.
        f.seek(0)
        xmlfile = f.read().decode('utf-8')
        try:
            save = pm.fileDialog2(fileMode=0)[0]
            if not save.split('.')[-1] == 'xml':
                save = save + '_.xml'
                print("警告: 附檔名錯誤")
            print(u"已選擇的XML: \'{}\'".format(save))
            print("正在 儲存 XML檔案 至 ...")
        except TypeError:
            print("操作錯誤: 使用者已取消")
            self.nfo_f_ct_le.setText(u'操作錯誤: 使用者已取消')
            self.nfo_f_ct_le.setStyleSheet('background-color: rgb(196, 50, 44); color: rgb(0, 0, 0);')
            return
        except:
            print("未知錯誤: 發生未知的錯誤")
            self.nfo_f_ct_le.setText(u'未知錯誤: 發生未知的錯誤')
            self.nfo_f_ct_le.setStyleSheet('background-color: rgb(196, 50, 44); color: rgb(0, 0, 0);')
            return

        # print( "" )
        # print( "XML updating to ... \'{}\'".format(save) )

        directory = os.path.dirname(xmlfile)

        tree = ET.parse(xmlfile)
        root = tree.getroot()

        def insert_element(par_path, d):
            name = d['name'].encode('ascii', 'ignore')

            parent = '{}'.format(re.split('/' + name, par_path)[0])
            pos, rot, scl = d['position'], d['rotation'], d['scale']
            px, py, pz = pos[0], pos[1], pos[2]
            rx, ry, rz = rot[0], rot[1], rot[2]
            sx, sy, sz = scl[0], scl[1], scl[2]

            print(d['name'])

            elems = []

            for elem, path in self.etree_iter_path(root):
                if path == parent:
                    elems.append(elem)

                    dupe = copy.deepcopy(elem.find('Object'))

                    aaaa = elem.find('Object')
                    print('name', name)
                    print('elem', elem)
                    print('path', path)
                    print('parent', parent)
                    print('dupe', dupe)
                    print('dupe.tag', dupe.tag)
                    print('dupe.get(\'name\')', dupe.get('name'))
                    print('pos', pos)
                    print('rot', rot)
                    print('scl', scl)

                    dupe.set('name', name)
                    new = ET.Element('Data')

                    dupe_transform = dupe.find('Transform')
                    # dupe_position = dupe_transform.find( 'position' ) if dupe_transform.find( 'position' ) else ET.SubElement( dupe_transform, 'position' )

                    if dupe_transform.find('position') == None:
                        ET.SubElement(dupe_transform, 'position')
                    dupe_position = dupe_transform.find('position')
                    dx, dy, dz = float(dupe_position.get('x', 0)), float(dupe_position.get('y', 0)), float(
                        dupe_position.get('z', 0))
                    offset_x, offset_y, offset_z = dx - px, dy - py, dz - pz
                    offset_x = float('{:.1f}'.format(offset_x))
                    offset_y = float('{:.1f}'.format(offset_y))
                    offset_z = float('{:.1f}'.format(offset_z))
                    for dupe_comv2 in dupe.iter('ComponentV2'):
                        if dupe_comv2.get('name') == 'NADILeanTouch.LeanCameraSettingValue':
                            offset_exist = False
                            for prop in dupe_comv2.iter('property'):
                                if prop.get('name') == 'offset':
                                    offset_exist = True
                                    lean_offset = prop.text
                                    convertedDict = json.loads(lean_offset)
                                    convertedDict['x'] = float(convertedDict['x']) + offset_x
                                    convertedDict['y'] = float(convertedDict['y']) + offset_y
                                    convertedDict['z'] = float(convertedDict['z']) + offset_z
                                    text = str(convertedDict)
                                    text = re.sub('u', '', text)
                                    text = re.sub(' ', '', text)
                                    text = re.sub('\'', '\"', text)
                                    prop.text = text
                            if not offset_exist:
                                ET.SubElement(dupe_comv2, 'property')
                                dupe_comv2.set('name', 'offset')
                                lean_offset = {}
                                lean_offset['x'] = offset_x
                                lean_offset['y'] = offset_y
                                lean_offset['z'] = offset_z
                                text = str(lean_offset)
                                text = re.sub('u', '', text)
                                text = re.sub(' ', '', text)
                                text = re.sub('\'', '\"', text)
                                dupe_comv2.text = text

                    print(offset_x, offset_y, offset_z)
                    dupe_position.set('x', '{}'.format(px))
                    dupe_position.set('y', '{}'.format(py))
                    dupe_position.set('z', '{}'.format(pz))
                    if dupe_transform.find('rotation') == None:
                        ET.SubElement(dupe_transform, 'rotation')
                    dupe_rotation = dupe_transform.find('rotation')
                    dupe_rotation.set('x', '{}'.format(rx))
                    dupe_rotation.set('y', '{}'.format(rx))
                    dupe_rotation.set('z', '{}'.format(rx))

                    elem.append(dupe)

        paths = list(data.keys())

        count = 0
        for path in paths:
            dict_data = data[path]
            insert_element(path, dict_data)
            count = count + 1

        tree.write(save, encoding="utf-8")

        self.nfo_f_ct_le.setText(u'狀態: 已新增{}個新點位'.format(count))
        self.nfo_f_ct_le.setStyleSheet('background-color: rgb(0, 153, 68); color: rgb(0, 0, 0);')
        _save = re.sub(r'/', r'\\', save)
        print(_save)
        popen_str = u'explorer /select,\"{}\"'.format(_save)
        print(popen_str)
        subprocess.Popen(popen_str.encode(locale.getpreferredencoding()))

    def XMLImportCallback(self, *pArgs):
        def extnaming(dict):
            str = dict['name'] + '_' + dict['uuid']
            return re.sub('-', '_', str)

        try:
            xmlfile = pm.fileDialog2(fileMode=1)[0]
            if not xmlfile.split('.')[-1] == 'xml':
                print("檔案類型錯誤: 請選擇XML檔案")
                self.nfo_f_ct_le.setText(u'檔案類型錯誤: 請選擇XML檔案')
                self.nfo_f_ct_le.setStyleSheet('background-color: rgb(196, 50, 44); color: rgb(0, 0, 0);')
                return
            print(u"已選擇的XML: \'{}\'".format(xmlfile))
            print("正在匯入 XML檔案 從 ...")
        except TypeError:
            print("操作錯誤: 使用者已取消")
            self.nfo_f_ct_le.setText(u'操作錯誤: 使用者已取消')
            self.nfo_f_ct_le.setStyleSheet('background-color: rgb(196, 50, 44); color: rgb(0, 0, 0);')
            return
        except:
            print("未知錯誤: 發生未知的錯誤")
            self.nfo_f_ct_le.setText(u'未知錯誤: 發生未知的錯誤')
            self.nfo_f_ct_le.setStyleSheet('background-color: rgb(196, 50, 44); color: rgb(0, 0, 0);')
            return

        directory = os.path.dirname(xmlfile)

        tree = ET.parse(xmlfile)
        root = tree.getroot()

        data = {}

        try:
            with open(directory + '\\' + 'data.json', 'r') as fp:
                None
            print("警告: 已找到 JSON資料暫存檔，將覆寫檔案 ...")
        except:
            print("警告: 未找到 JSON資料暫存檔，開始初始化 ...")

        if cmds.ls(root.tag):
            force_continue = cmds.confirmDialog(title='重要提示',
                                                message='檢測到舊的 root 節點，是否繼續? ( 將 清 除 舊 的 節 點 !!! )',
                                                button=['yes', 'no'], defaultButton='yes', cancelButton='no',
                                                dismissString='no', icon='warning', backgroundColor=[1, 1, 1])
            print(force_continue)
            if force_continue == 'no':
                self.nfo_f_ct_le.setText(u'操作錯誤: 使用者已取消')
                self.nfo_f_ct_le.setStyleSheet('background-color: rgb(196, 50, 44); color: rgb(0, 0, 0);')
                return

            print("狀態: 清除 root 節點中 ...")
            for ls in cmds.ls(root.tag, transforms=True, visible=True):
                try:
                    cmds.delete(ls)
                except:
                    None
            print("狀態:  root 節點已清除")

        print("狀態: 開始建立 root 節點 ...")
        if not cmds.ls(root.tag):
            cmds.group(em=True, name=root.tag)
            path = '.'
            data[path] = {
                'name': root.tag,
                'uuid': cmds.ls(root.tag, uuid=True)[0],
                'position': (0, 0, 0),
                'rotation': (0, 0, 0),
                'scale': (0, 0, 0)
            }
            current = extnaming(data[path])
            cmds.rename(root.tag, current)

        print("狀態: 開始建立XML的Object樹結構節點 ...")
        try:
            for elem, path in self.etree_iter_path(root):
                if elem.tag == 'Object':
                    name = elem.get('name')
                    if elem.get('type') == 'Device':
                        cmds.spaceLocator(name=name)
                    else:
                        cmds.group(em=True, name=name)

                    # Initial data.
                    px, py, pz = 0, 0, 0
                    rx, ry, rz = 0, 0, 0
                    sx, sy, sz = 1, 0, 1

                    tr_exist = elem.find('Transform') if elem.find('Transform') else None
                    if tr_exist and elem is not None:
                        for tr in elem.find('Transform'):
                            if tr.tag == 'position':
                                px = tr.attrib['x'] if tr.attrib['x'] else 0
                                py = tr.attrib['y'] if tr.attrib['y'] else 0
                                pz = tr.attrib['z'] if tr.attrib['z'] else 0
                            elif tr.tag == 'rotation':
                                rx = tr.attrib['x'] if tr.attrib['x'] else 0
                                ry = tr.attrib['y'] if tr.attrib['y'] else 0
                                rz = tr.attrib['z'] if tr.attrib['z'] else 0
                            elif tr.tag == 'scale':
                                sx = tr.attrib['x'] if tr.attrib['x'] else 1
                                sy = tr.attrib['y'] if tr.attrib['y'] else 1
                                sz = tr.attrib['z'] if tr.attrib['z'] else 1

                    dict_data = {
                        'name': name,
                        'uuid': cmds.ls(name, uuid=True)[0],
                        'position': (px, py, pz),
                        'rotation': (rx, ry, rz),
                        'scale': (sx, sy, sz)
                    }
                    data[path] = dict_data

                    current = extnaming(data[path])
                    cmds.rename(name, current)
                    cmds.move(px, py, pz, current)
                    cmds.rotate(rx, ry, rz, current)
                    # cmds.scale( sx, sy, sz, current )

                    cmds.addAttr(current, longName='bundle', dataType='string')
                    cmds.addAttr(current, longName='time', dataType='string')
                    try:
                        bundle = elem.get('bundle')
                        time = elem.get('time')
                        cmds.setAttr('{}.bundle'.format(current), bundle, type='string')
                        cmds.setAttr('{}.time'.format(current), time, type='string')
                        # cmds.deleteAttr( current, attribute='greenBow' )
                    except:
                        # cmds.addAttr( current, longName='bundle', dataType='string' )
                        None

                    par_path = '{}'.format(re.split('/' + name, path)[0])
                    parent = extnaming(data[par_path])
                    cmds.parent(current, parent)
        except:
            print("未知錯誤: 發生未知的錯誤")
            self.nfo_f_ct_le.setText(u'未知錯誤: 發生未知的錯誤')
            self.nfo_f_ct_le.setStyleSheet('background-color: rgb(196, 50, 44); color: rgb(0, 0, 0);')
            return

        print("狀態: 回復節點名稱中 ...")
        for ls in data:
            result = extnaming(data[ls]).rsplit('_', 5)[0]
            cmds.rename(extnaming(data[ls]), result)
        print("狀態: 節點名稱已回復")

        print("狀態: 儲存 JSON資料暫存檔 中 ...")
        with open(directory + '\\' + 'data.json', 'w') as fp:
            json.dump(data, fp)
        print("狀態: JSON資料暫存檔 已儲存")

        if xmlfile is None:
            print("未知錯誤: 路徑不能為空")
            self.nfo_f_ct_le.setText(u'未知錯誤: 路徑不能為空')
            self.nfo_f_ct_le.setStyleSheet('background-color: rgb(196, 50, 44); color: rgb(0, 0, 0);')
            return

        f.write(xmlfile.encode('utf-8'))

        self.nfo_f_ct_le.setText(u'狀態: 已載入XML\'{}\''.format(xmlfile))
        self.nfo_f_ct_le.setStyleSheet('background-color: rgb(99, 192, 223); color: rgb(0, 0, 0);')

    def XMLSaveCallback(self, *pArgs):
        # Load from temporaryFile.
        f.seek(0)
        xmlfile = f.read().decode('utf-8')
        print(xmlfile)

        directory = os.path.dirname(xmlfile)

        tree = ET.parse(xmlfile)
        root = tree.getroot()

        try:
            with open(directory + '\\' + 'data.json', 'r') as fp:
                data = json.load(fp)
            print("Info: 已找到 JSON資料暫存檔，讀取中 ...")
        except:
            print("Warning: 未找到 JSON資料暫存檔，請先匯入檔案")
            return

        data_patch = {}

        for elem in cmds.listRelatives(cmds.ls(root.tag), fullPath=True, allDescendents=True, type='transform'):
            path = re.sub('\|' + root.tag, '.', elem)
            path = re.sub('\|', '/', path)
            if path not in data:
                path_elem = re.split('/', path)
                name = path_elem[len(path_elem) - 1]
                uuid = cmds.ls(name, uuid=True)[0]
                pos = cmds.getAttr('{}.translate'.format(name))[0]
                rot = cmds.getAttr('{}.rotate'.format(name))[0]
                scl = cmds.getAttr('{}.scale'.format(name))[0]

                dict_data = {
                    'name': name,
                    'uuid': uuid,
                    'position': pos,
                    'rotation': rot,
                    'scale': scl
                }
                data_patch[path] = dict_data

                cmds.setAttr('{}.useOutlinerColor'.format(name), True)
                cmds.setAttr('{}.outlinerColor'.format(name), 1, 1, 0)

                cmds.setAttr('{}Shape.overrideEnabled'.format(name), True)
                cmds.setAttr('{}Shape.overrideColor'.format(name), 17)  # yellow

                print(name, uuid, pos, rot, scl)

        with open(directory + '\\' + 'data_patch.json', 'w') as fp:
            json.dump(data_patch, fp)

        self.update_XML(data_patch)

    def Debug_DelNewItems(self, *pArgs):
        # Load from temporaryFile.
        f.seek(0)
        xmlfile = f.read().decode('utf-8')

        directory = os.path.dirname(xmlfile)

        tree = ET.parse(xmlfile)
        root = tree.getroot()

        with open(directory + '\\' + 'data.json', 'r') as fp:
            data = json.load(fp)

        count = 0
        for elem in cmds.listRelatives(cmds.ls(root.tag), fullPath=True, allDescendents=True, type='transform'):
            path = re.sub('\|' + root.tag, '.', elem)
            path = re.sub('\|', '/', path)
            if path not in data:
                cmds.delete(elem)
                count = count + 1
        self.nfo_f_ct_le.setText(u'狀態: 已刪除{}個新點位'.format(count))
        self.nfo_f_ct_le.setStyleSheet('background-color: rgb(99, 192, 223); color: rgb(0, 0, 0);')

    #

    def cancelCallback(self, *pArgs):
        if cmds.window(windows_id, exists=True):
            cmds.deleteUI(windows_id)

    def selectInListWidget(self):
        self.nfo_f_ct_le.setText(u'選取的物件名稱: {}'.format(self.nfo_f_ct_lw.currentItem().text()))
        self.nfo_f_ct_le.setStyleSheet('background-color: rgb(99, 192, 223); color: rgb(0, 0, 0);')


# ----------------------------------------------------------------------------------------- #

def create():
    delete()
    global dialog
    if dialog is None:
        dialog = MainWindow()
    dialog.show()


def delete():
    global dialog
    if dialog is None:
        return

    dialog.deleteLater()
    dialog = None


create()
