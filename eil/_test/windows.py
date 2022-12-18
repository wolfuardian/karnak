# -*- coding: utf-8 -*-
button_style_sheet = '''
    QPushButton
    {
        background-color: rgb(68, 68, 68); border: 0px;
    }
    QPushButton:pressed
    {
        background-color: rgb(30, 30, 30);
    }
    QPushButton:hover:!pressed
    {
        background-color: rgb(90, 90, 90);
    }
'''
import os.path

from PySide2 import QtCore
from PySide2 import QtWidgets
from PySide2 import QtGui

# f = tempfile.TemporaryFile()

# use it when you are debugging.
for child in QtWidgets.QApplication.allWidgets():
    if child.objectName() == 'main':
        child.deleteLater()

# setSizePolicy(QSizePolicy::Expanding, QSizePolicy::Fixed);

# do not modular gui form, because it would cause ide hard to track.
class Dialog(QtWidgets.QDialog):
    def __init__(self, parent=QtWidgets.QApplication.activeWindow()):
        super(Dialog, self).__init__(parent)
        # self.__importer = XMLImporter(self)
        # self.__creator = XMLCreator(self)
        


        self.setObjectName('main')
        self.setWindowTitle(u'OCMS Editor for Maya {}'.format('0.2.6').encode("utf-8"))
        self.setGeometry(2000, 200, 720, 640)
        self.setFixedWidth(720)
        self.setFixedHeight(640)
        self.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.setLayout(QtWidgets.QVBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().setSpacing(0)
        

        debug_mode = False


        # _.setFrameStyle(*arg)             --FrameStyle  ::Shape
        # 
        # QtWidgets.QFrame.NoFrame          Draws nothing
        # QtWidgets.QFrame.Box              Draws a box around its contents
        # QtWidgets.QFrame.Panel            Draws a panel to make the contents appear raised or sunken
        # QtWidgets.QFrame.StyledPanel      Draws a rectangular panel with a look that depends on the current GUI style. It can be raised or sunken.
        # QtWidgets.QFrame.HLine            Draws a horizontal line that frames nothing (useful as separator)
        # QtWidgets.QFrame.VLine            Draws a vertical line that frames nothing (useful as separator)
        # QtWidgets.QFrame.WinPanel         Draws a rectangular panel that can be raised or sunken like those in Windows 2000. Specifying this shape sets the line width to 2 pixels. WinPanel is provided for compatibility. For GUI style independence we recommend using StyledPanel instead.
        # 
        #                                   --FrameStyle  ::Shadow
        # 
        # QtWidgets.QFrame.Plain            The frame and contents appear level with the surroundings; draws using the palette QPalette.WindowText color (without any 3D effect)
        # QtWidgets.QFrame.Raised           The frame and contents appear raised; draws a 3D raised line using the light and dark colors of the current color group
        # QtWidgets.QFrame.Sunken           The frame and contents appear sunken; draws a 3D sunken line using the light and dark colors of the current color group


        # _.setAlignment(*arg)              --Alignment
        # 
        # QtCore.Qt.AlignLeft               Aligns to the left border, except for Arabic and Hebrew where it aligns to the right.
        # QtCore.Qt.AlignRight              Aligns to the right border, except for Arabic and Hebrew where it aligns to the left.
        # QtCore.Qt.AlignJustify            Produces justified text.
        # QtCore.Qt.AlignHCenter            Aligns horizontally centered.
        # QtCore.Qt.AlignTop                Aligns to the top border.
        # QtCore.Qt.AlignBottom             Aligns to the bottom border.
        # QtCore.Qt.AlignVCenter            Aligns vertically centered
        # QtCore.Qt.AlignCenter             (== Qt::AlignHCenter | Qt::AlignVCenter)
        # QtCore.Qt.TextSingleLine          Ignores newline characters in the text.
        # QtCore.Qt.TextExpandTabs          Expands tabs (see below)
        # QtCore.Qt.TextShowMnemonic        Interprets “&x” as x; i.e., underlined.
        # QtCore.Qt.TextWordWrap            Breaks the text to fit the rectangle.

        def addWidget(
            widget,
            parent,
            layout,
            style=None,
            style_sheet=None,
            contents_margins=None,
            text_margins=None,
            spacing=None,
            width=None,
            height=None,
            icon=None,
            icon_size=None,
            text=None,
            alignment=None,
            text_alignment=None,
            size_policy=None,
            flat=None,
            read_only=None,
            word_wrap=None,
            placeholder_text=None,
            items=None,
            current_text=None,
            font=None
        ):
            widget.setLayout(layout)
            widget.layout().setContentsMargins(0,0,0,0)
            widget.layout().setSpacing(0)
            try:
                widget.setFrameStyle(QtWidgets.QFrame.Panel | QtWidgets.QFrame.Raised)
            except:
                None

            if style is not None:
                widget.setFrameStyle(style)

            if style_sheet is not None:
                widget.setStyleSheet(style_sheet)

            if contents_margins is not None:
                m = contents_margins
                widget.layout().setContentsMargins(m[0],m[1],m[2],m[3])

            if text_margins is not None:
                m = text_margins
                widget.setTextMargins(m[0],m[1],m[2],m[3])

            if spacing is not None:
                widget.layout().setSpacing(spacing)

            if width is not None:
                widget.setFixedWidth(width)
            
            if height is not None:
                widget.setFixedHeight(height)

            if icon is not None:
                widget.setIcon(icon)

            if icon_size is not None:
                widget.setIconSize(icon_size)

            if text is not None:
                widget.setText(text)

            if alignment is not None:
                widget.layout().setAlignment(alignment)

            if text_alignment is not None:
                widget.setAlignment(text_alignment)

            if size_policy is not None:
                sp = size_policy
                widget.setSizePolicy(sp[0],sp[1])

            if flat is not None:
                widget.setFlat(flat)

            if read_only is not None:
                widget.setReadOnly(read_only)

            if word_wrap is not None:
                widget.setWordWrap(word_wrap)

            if placeholder_text is not None:
                widget.setPlaceholderText(placeholder_text)

            if items is not None:
                widget.addItems(items)

            if current_text is not None:
                widget.setCurrentText(current_text)

            if font is not None:
                widget.setFont(font)
            

            parent.layout().addWidget(widget)
            return widget
        self.header = addWidget( QtWidgets.QFrame(),
            self,
            QtWidgets.QVBoxLayout(),
            contents_margins=(0,8,0,8),
            height=48,
            alignment=QtCore.Qt.AlignCenter
        )
        self.header_0_lb = addWidget( QtWidgets.QLabel(),
            self.header,
            QtWidgets.QVBoxLayout(),
            style=QtWidgets.QFrame.NoFrame,
            text="OCMS Editor for Maya 0.2.7",
            text_alignment=QtCore.Qt.AlignCenter
        )
        self.header_1_lb = addWidget( QtWidgets.QLabel(),
            self.header,
            QtWidgets.QVBoxLayout(),
            style=QtWidgets.QFrame.NoFrame,
            text="NADI System Corp. / Last updated 2022-10-24",
            text_alignment=QtCore.Qt.AlignCenter
            
        )
        self.body = addWidget( QtWidgets.QFrame(),
            self,
            QtWidgets.QHBoxLayout(),
            alignment=QtCore.Qt.AlignTop
        )
        self.body_l = addWidget( QtWidgets.QFrame(),
            self.body,
            QtWidgets.QHBoxLayout(),
            style=QtWidgets.QFrame.NoFrame,
            alignment=QtCore.Qt.AlignTop,
            width=360,
            contents_margins=(8,8,8,8),
            # size_policy=(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        )
        self.body_l_body = addWidget( QtWidgets.QFrame(),
            self.body_l,
            QtWidgets.QVBoxLayout(),
            style=QtWidgets.QFrame.NoFrame,
            height=512,
            spacing=8
        )
        self.body_l_body_header = addWidget( QtWidgets.QFrame(),
            self.body_l_body,
            QtWidgets.QHBoxLayout(),
            style=(QtWidgets.QFrame.Box | QtWidgets.QFrame.Sunken),
            height=40,
            alignment=QtCore.Qt.AlignLeft,
            contents_margins=(2,0,2,0),
            spacing=2
        )
        self.body_l_body_header_new_btn = addWidget( QtWidgets.QPushButton(),
            self.body_l_body_header,
            QtWidgets.QVBoxLayout(),
            width=96,
            height=32,
            text="  New",
            font=QtGui.QFont("Segoe UI", 12),
            icon=QtGui.QIcon(getIconFullPath("new_xml.png")),
            icon_size=QtCore.QSize(24,24),
            style_sheet="QPushButton{ background-color: rgb(68, 68, 68); border: 0px; } QPushButton:pressed{ background-color: rgb(30, 30, 30); } QPushButton:hover:!pressed{ background-color: rgb(90, 90, 90); }"
            # flat=True
        )
        self.body_l_body_header_new_btn.clicked.connect(self.OnNewButtonClicked)
        self.body_l_body_header_load_btn = addWidget( QtWidgets.QPushButton(),
            self.body_l_body_header,
            QtWidgets.QVBoxLayout(),
            width=96,
            height=32,
            text="  Load",
            font=QtGui.QFont("Segoe UI", 12),
            icon=QtGui.QIcon(getIconFullPath("load_xml.png")),
            icon_size=QtCore.QSize(24,24),
            style_sheet="QPushButton{ background-color: rgb(68, 68, 68); border: 0px; } QPushButton:pressed{ background-color: rgb(30, 30, 30); } QPushButton:hover:!pressed{ background-color: rgb(90, 90, 90); }"
            # flat=True
        )
        self.body_l_body_header_load_btn.clicked.connect(self.OnLoadButtonClicked)
        self.body_l_body_body = addWidget( QtWidgets.QFrame(),
            self.body_l_body,
            QtWidgets.QVBoxLayout(),
            style=(QtWidgets.QFrame.Box | QtWidgets.QFrame.Sunken),
        )
        self.body_l_body_body_header = addWidget( QtWidgets.QFrame(),
            self.body_l_body_body,
            QtWidgets.QHBoxLayout(),
            style=QtWidgets.QFrame.NoFrame,
            style_sheet="background-color: rgb(60, 60, 60);",
            height=24,
            contents_margins=(8,0,8,0)
            # style=(QtWidgets.QFrame.StyledPanel | QtWidgets.QFrame.Plain)
        )
        self.body_l_body_body_header_lb = addWidget( QtWidgets.QLabel(),
            self.body_l_body_body_header,
            QtWidgets.QVBoxLayout(),
            style=QtWidgets.QFrame.NoFrame,
            text=r"- Root/KSPSmartBuilding/Kaohsiung_B04/Cam/CameraB4_5",
            font=QtGui.QFont("Segoe UI", 7)
        )
        self.body_l_body_body_body = addWidget( QtWidgets.QFrame(),
            self.body_l_body_body,
            QtWidgets.QHBoxLayout(),
            style=QtWidgets.QFrame.NoFrame
        )
        self.body_l_body_body_body_lw = addWidget( QtWidgets.QListWidget(),
            self.body_l_body_body_body,
            QtWidgets.QHBoxLayout(),
            style=QtWidgets.QFrame.NoFrame,
            contents_margins=(8,0,8,0)
        )
        self.body_l_body_foot = addWidget( QtWidgets.QFrame(),
            self.body_l_body,
            QtWidgets.QVBoxLayout(),
            style=QtWidgets.QFrame.NoFrame
        )
        self.body_l_body_foot_header = addWidget( QtWidgets.QFrame(),
            self.body_l_body_foot,
            QtWidgets.QHBoxLayout(),
            height=24,
            style=QtWidgets.QFrame.NoFrame,
        )
        self.body_l_body_foot_header_splitter = addWidget( Splitter(),
            self.body_l_body_foot_header,
            QtWidgets.QHBoxLayout(),
            text=u"點位工具"
        )
        self.body_l_body_foot_body = addWidget( QtWidgets.QFrame(),
            self.body_l_body_foot,
            QtWidgets.QHBoxLayout(),
            style=(QtWidgets.QFrame.Box | QtWidgets.QFrame.Sunken),
            contents_margins=(8,8,8,8),
            spacing=8,
            alignment=(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        )
        self.body_l_body_foot_body_add_node_btn = addWidget( QtWidgets.QPushButton(),
            self.body_l_body_foot_body,
            QtWidgets.QHBoxLayout(),
            width=56,
            height=56,
            icon=QtGui.QIcon(getIconFullPath("add_node.png")),
            icon_size=QtCore.QSize(32,32),
            style_sheet="QPushButton{ background-color: rgb(68, 68, 68); border: 0px; } QPushButton:pressed{ background-color: rgb(30, 30, 30); } QPushButton:hover:!pressed{ background-color: rgb(90, 90, 90); }"
            # flat=True
        )
        self.body_l_body_foot_body_del_node_btn = addWidget( QtWidgets.QPushButton(),
            self.body_l_body_foot_body,
            QtWidgets.QHBoxLayout(),
            width=56,
            height=56,
            icon=QtGui.QIcon(getIconFullPath("del_node.png")),
            icon_size=QtCore.QSize(32,32),
            style_sheet="QPushButton{ background-color: rgb(68, 68, 68); border: 0px; } QPushButton:pressed{ background-color: rgb(30, 30, 30); } QPushButton:hover:!pressed{ background-color: rgb(90, 90, 90); }"
            # flat=True
        )  
        self.body_r = addWidget( QtWidgets.QFrame(),
            self.body,
            QtWidgets.QVBoxLayout(),
            style=QtWidgets.QFrame.NoFrame,
            width=360,
            contents_margins=(8,8,8,8),
            size_policy=(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        )
        self.body_r_body = addWidget( QtWidgets.QFrame(),
            self.body_r,
            QtWidgets.QVBoxLayout(),
            style=QtWidgets.QFrame.NoFrame,
            height=512,
            spacing=8
        )
        self.body_r_body_header = addWidget( QtWidgets.QFrame(),
            self.body_r_body,
            QtWidgets.QHBoxLayout(),
            style=QtWidgets.QFrame.NoFrame,
            height=96,
            spacing=8
        )
        self.body_r_body_header_l = addWidget( QtWidgets.QFrame(),
            self.body_r_body_header,
            QtWidgets.QVBoxLayout(),
            style=QtWidgets.QFrame.NoFrame,
            height=96
        )
        self.body_r_body_header_l_header = addWidget( QtWidgets.QFrame(),
            self.body_r_body_header_l,
            QtWidgets.QHBoxLayout(),
            height=24,
            style=QtWidgets.QFrame.NoFrame
        )
        self.body_r_body_header_l_header_splitter = addWidget( Splitter(),
            self.body_r_body_header_l_header,
            QtWidgets.QHBoxLayout(),
            text=u"模型庫"
        )
        self.body_r_body_header_l_body = addWidget( QtWidgets.QFrame(),
            self.body_r_body_header_l,
            QtWidgets.QHBoxLayout(),
            style=QtWidgets.QFrame.NoFrame,
            alignment=(QtCore.Qt.AlignTop),
            contents_margins=(2,2,2,2)
        )
        self.body_r_body_header_l_body_lb = addWidget( QtWidgets.QLabel(),
            self.body_r_body_header_l_body,
            QtWidgets.QVBoxLayout(),
            style=QtWidgets.QFrame.NoFrame,
            text=r"C:\Program Files\Autodesk\Maya2020\bin\plug-ins\ocms\editor\ui",
            text_alignment=QtCore.Qt.AlignTop,
            word_wrap=True
        )
        self.body_r_body_header_r = addWidget( QtWidgets.QFrame(),
            self.body_r_body_header,
            QtWidgets.QVBoxLayout(),
            style=QtWidgets.QFrame.NoFrame,
            contents_margins=(0,8,0,8),
        )
        self.body_r_body_header_r_btn = addWidget( QtWidgets.QPushButton(),
            self.body_r_body_header_r,
            QtWidgets.QHBoxLayout(),
            width=136,
            height=80,
            icon=QtGui.QIcon(getIconFullPath("set_fbx_dir.png")),
            icon_size=QtCore.QSize(64,64)
        )
        self.body_r_body_body = addWidget( QtWidgets.QFrame(),
            self.body_r_body,
            QtWidgets.QVBoxLayout(),
            QtWidgets.QFrame.NoFrame,
            height=128,
            size_policy=(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        )
        self.body_r_body_body_header = addWidget( QtWidgets.QFrame(),
            self.body_r_body_body,
            QtWidgets.QHBoxLayout(),
            style=QtWidgets.QFrame.NoFrame,
            height=24
        )
        self.body_r_body_body_header_splitter = addWidget( Splitter(),
            self.body_r_body_body_header,
            QtWidgets.QHBoxLayout(),
            text=u"模型描述"
        )
        self.body_r_body_body_body = addWidget( QtWidgets.QFrame(),
            self.body_r_body_body,
            QtWidgets.QHBoxLayout(),
            QtWidgets.QFrame.NoFrame,
        )
        self.body_r_body_body_body_l = addWidget( QtWidgets.QFrame(),
            self.body_r_body_body_body,
            QtWidgets.QVBoxLayout(),
            QtWidgets.QFrame.NoFrame,
            alignment=QtCore.Qt.AlignLeft,
            width=56
        )
        self.body_r_body_body_body_l_0_lb = addWidget( QtWidgets.QLabel(),
            self.body_r_body_body_body_l,
            QtWidgets.QVBoxLayout(),
            style=QtWidgets.QFrame.NoFrame,
            text=u"資料夾",
            text_alignment=(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        )
        self.body_r_body_body_body_l_1_lb = addWidget( QtWidgets.QLabel(),
            self.body_r_body_body_body_l,
            QtWidgets.QVBoxLayout(),
            style=QtWidgets.QFrame.NoFrame,
            text=u"檔案",
            text_alignment=(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        )
        self.body_r_body_body_body_l_2_lb = addWidget( QtWidgets.QLabel(),
            self.body_r_body_body_body_l,
            QtWidgets.QVBoxLayout(),
            style=QtWidgets.QFrame.NoFrame,
            text=u"大小",
            text_alignment=(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        )
        self.body_r_body_body_body_l_3_lb = addWidget( QtWidgets.QLabel(),
            self.body_r_body_body_body_l,
            QtWidgets.QVBoxLayout(),
            style=QtWidgets.QFrame.NoFrame,
            text=u"建立日期",
            text_alignment=(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        )
        self.body_r_body_body_body_l_4_lb = addWidget( QtWidgets.QLabel(),
            self.body_r_body_body_body_l,
            QtWidgets.QVBoxLayout(),
            style=QtWidgets.QFrame.NoFrame,
            text=u"修改日期",
            text_alignment=(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        )
        self.body_r_body_body_body_r = addWidget( QtWidgets.QFrame(),
            self.body_r_body_body_body,
            QtWidgets.QVBoxLayout(),
            QtWidgets.QFrame.NoFrame
        )
        self.body_r_body_body_body_r_0_lb = addWidget( QtWidgets.QLabel(),
            self.body_r_body_body_body_r,
            QtWidgets.QVBoxLayout(),
            style=QtWidgets.QFrame.NoFrame,
            text=u"FireAlarm_火警警報器",
            text_alignment=(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        )
        self.body_r_body_body_body_r_1_lb = addWidget( QtWidgets.QLabel(),
            self.body_r_body_body_body_r,
            QtWidgets.QVBoxLayout(),
            style=QtWidgets.QFrame.NoFrame,
            text=u"FireAlarm.fbx",
            text_alignment=(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        )
        self.body_r_body_body_body_r_2_lb = addWidget( QtWidgets.QLabel(),
            self.body_r_body_body_body_r,
            QtWidgets.QVBoxLayout(),
            style=QtWidgets.QFrame.NoFrame,
            text=u"216 kb",
            text_alignment=(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        )
        self.body_r_body_body_body_r_3_lb = addWidget( QtWidgets.QLabel(),
            self.body_r_body_body_body_r,
            QtWidgets.QVBoxLayout(),
            style=QtWidgets.QFrame.NoFrame,
            text=u"2022/10/18 上午 10:52",
            text_alignment=(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        )
        self.body_r_body_body_body_r_4_lb = addWidget( QtWidgets.QLabel(),
            self.body_r_body_body_body_r,
            QtWidgets.QVBoxLayout(),
            style=QtWidgets.QFrame.NoFrame,
            text=u"2020/07/06 上午 10:11",
            text_alignment=(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft)
        )
        self.body_r_body_foot = addWidget( QtWidgets.QFrame(),
            self.body_r_body,
            QtWidgets.QVBoxLayout(),
            style=QtWidgets.QFrame.NoFrame
        )
        self.body_r_body_foot_header = addWidget( QtWidgets.QFrame(),
            self.body_r_body_foot,
            QtWidgets.QVBoxLayout(),
            style=QtWidgets.QFrame.NoFrame,
            height=24
        )
        self.body_r_body_foot_header_splitter = addWidget( Splitter(),
            self.body_r_body_foot_header,
            QtWidgets.QHBoxLayout(),
            text=u"屬性修改"
        )
        self.body_r_body_foot_body = addWidget( QtWidgets.QFrame(),
            self.body_r_body_foot,
            QtWidgets.QVBoxLayout(),
            style=QtWidgets.QFrame.NoFrame
        )
        self.body_r_body_foot_body_header = addWidget( QtWidgets.QFrame(),
            self.body_r_body_foot_body,
            QtWidgets.QHBoxLayout(),
            style=QtWidgets.QFrame.NoFrame,
            spacing=8
        )
        self.body_r_body_foot_body_header_l = addWidget( QtWidgets.QFrame(),
            self.body_r_body_foot_body_header,
            QtWidgets.QVBoxLayout(),
            style=QtWidgets.QFrame.NoFrame,
            width=64
        )
        self.body_r_body_foot_body_header_l_0_lb = addWidget( QtWidgets.QLabel(),
            self.body_r_body_foot_body_header_l,
            QtWidgets.QVBoxLayout(),
            style=QtWidgets.QFrame.NoFrame,
            text="Type",
            text_alignment=QtCore.Qt.AlignRight
        )
        self.body_r_body_foot_body_header_l_1_lb = addWidget( QtWidgets.QLabel(),
            self.body_r_body_foot_body_header_l,
            QtWidgets.QVBoxLayout(),
            style=QtWidgets.QFrame.NoFrame,
            text="Name",
            text_alignment=QtCore.Qt.AlignRight
        )
        self.body_r_body_foot_body_header_l_2_lb = addWidget( QtWidgets.QLabel(),
            self.body_r_body_foot_body_header_l,
            QtWidgets.QVBoxLayout(),
            style=QtWidgets.QFrame.NoFrame,
            text="Alias",
            text_alignment=QtCore.Qt.AlignRight
        )
        self.body_r_body_foot_body_header_l_3_lb = addWidget( QtWidgets.QLabel(),
            self.body_r_body_foot_body_header_l,
            QtWidgets.QVBoxLayout(),
            style=QtWidgets.QFrame.NoFrame,
            text="ID",
            text_alignment=QtCore.Qt.AlignRight
        )
        self.body_r_body_foot_body_header_l_4_lb = addWidget( QtWidgets.QLabel(),
            self.body_r_body_foot_body_header_l,
            QtWidgets.QVBoxLayout(),
            style=QtWidgets.QFrame.NoFrame,
            text="Model",
            text_alignment=QtCore.Qt.AlignRight
        )
        self.body_r_body_foot_body_header_l_5_lb = addWidget( QtWidgets.QLabel(),
            self.body_r_body_foot_body_header_l,
            QtWidgets.QVBoxLayout(),
            style=QtWidgets.QFrame.NoFrame,
            text="Bundle",
            text_alignment=QtCore.Qt.AlignRight
        )
        self.body_r_body_foot_body_header_l_6_lb = addWidget( QtWidgets.QLabel(),
            self.body_r_body_foot_body_header_l,
            QtWidgets.QVBoxLayout(),
            style=QtWidgets.QFrame.NoFrame,
            text="Noted",
            text_alignment=QtCore.Qt.AlignRight
        )
        self.body_r_body_foot_body_header_r = addWidget( QtWidgets.QFrame(),
            self.body_r_body_foot_body_header,
            QtWidgets.QVBoxLayout(),
            style=QtWidgets.QFrame.NoFrame
        )
        self.body_r_body_foot_body_header_r_0_le = addWidget( QtWidgets.QComboBox(),
            self.body_r_body_foot_body_header_r,
            QtWidgets.QHBoxLayout(),
            items=['Building', 'Floor', 'Device'],
            current_text='Device'
        )
        self.body_r_body_foot_body_header_r_1_le = addWidget( QtWidgets.QLineEdit(),
            self.body_r_body_foot_body_header_r,
            QtWidgets.QHBoxLayout(),
            text="",
            placeholder_text="輸入 名稱"
        )
        self.body_r_body_foot_body_header_r_2_le = addWidget( QtWidgets.QLineEdit(),
            self.body_r_body_foot_body_header_r,
            QtWidgets.QHBoxLayout(),
            text="",
            placeholder_text="輸入 顯示名稱"
        )
        self.body_r_body_foot_body_header_r_3_le = addWidget( QtWidgets.QLineEdit(),
            self.body_r_body_foot_body_header_r,
            QtWidgets.QHBoxLayout(),
            text="",
            placeholder_text="輸入 ID"
        )
        self.body_r_body_foot_body_header_r_4_body = addWidget( QtWidgets.QFrame(),
            self.body_r_body_foot_body_header_r,
            QtWidgets.QHBoxLayout(),
            style=QtWidgets.QFrame.NoFrame
        )
        self.body_r_body_foot_body_header_r_4_body_le = addWidget( QtWidgets.QLineEdit(),
            self.body_r_body_foot_body_header_r_4_body,
            QtWidgets.QHBoxLayout(),
            text="",
            placeholder_text="輸入 模型名稱"
        )
        self.body_r_body_foot_body_header_r_4_body_btn = addWidget( QtWidgets.QPushButton(),
            self.body_r_body_foot_body_header_r_4_body,
            QtWidgets.QHBoxLayout(),
            width=16,
            icon=QtGui.QIcon(getIconFullPath("arrow_left.png")),
            icon_size=QtCore.QSize(8,8),
            flat=True
        )  
        self.body_r_body_foot_body_header_r_5_le = addWidget( QtWidgets.QLineEdit(),
            self.body_r_body_foot_body_header_r,
            QtWidgets.QHBoxLayout(),
            text="",
            placeholder_text="輸入 Bundle路徑"
        )
        self.body_r_body_foot_body_header_r_6_le = addWidget( QtWidgets.QLineEdit(),
            self.body_r_body_foot_body_header_r,
            QtWidgets.QHBoxLayout(),
            text="",
            placeholder_text="輸入 模型筆記"
        )
        self.body_r_body_foot_body_body = addWidget( QtWidgets.QFrame(),
            self.body_r_body_foot_body,
            QtWidgets.QVBoxLayout(),
            style=QtWidgets.QFrame.NoFrame,
            alignment=(QtCore.Qt.AlignTop | QtCore.Qt.AlignRight),
            contents_margins=(8,8,8,8)
        )
        self.body_r_body_foot_body_body_btn = addWidget( QtWidgets.QPushButton(),
            self.body_r_body_foot_body_body,
            QtWidgets.QHBoxLayout(),
            width=144,
            height=16,
            icon=QtGui.QIcon(getIconFullPath("reload.png")),
            icon_size=QtCore.QSize(12,12),
            text=u"重設欄位"
        )  
        self.body_r_foot = addWidget( QtWidgets.QFrame(),
            self.body_r,
            QtWidgets.QHBoxLayout(),
            style=(QtWidgets.QFrame.Box | QtWidgets.QFrame.Sunken),
            # style=QtWidgets.QFrame.NoFrame,
            alignment=QtCore.Qt.AlignRight,
            contents_margins=(2,2,2,2),
            spacing=8
        )
        self.body_r_foot_export_btn = addWidget( QtWidgets.QPushButton(),
            self.body_r_foot,
            QtWidgets.QHBoxLayout(),
            width=136,
            height=48,
            text="  Export XML",
            font=QtGui.QFont("Segoe UI", 12),
            icon=QtGui.QIcon(getIconFullPath("export_xml.png")),
            icon_size=QtCore.QSize(24,24),
            style_sheet="QPushButton{ background-color: rgb(68, 68, 68); border: 0px; } QPushButton:pressed{ background-color: rgb(30, 30, 30); } QPushButton:hover:!pressed{ background-color: rgb(90, 90, 90); }"
        )
        self.body_r_foot_close_btn = addWidget( QtWidgets.QPushButton(),
            self.body_r_foot,
            QtWidgets.QHBoxLayout(),
            width=136,
            height=48,
            text="  Close",
            style_sheet="QPushButton{background-color: rgb(68, 68, 68); border: 0px;}QPushButton:pressed{ background-color: rgb(30, 30, 30); }QPushButton:hover:!pressed{background-color: rgb(90, 90, 90);}",
            font=QtGui.QFont("Segoe UI", 12),
            icon=QtGui.QIcon(getIconFullPath("close.png")),
            icon_size=QtCore.QSize(24,24)
        )
        self.body_r_foot_close_btn.clicked.connect(self.OnCancelButtonClicked)
        self.foot = addWidget( QtWidgets.QFrame(),
            self,
            QtWidgets.QHBoxLayout(),
            style=QtWidgets.QFrame.NoFrame,
            style_sheet="background-color: rgb(90, 90, 90);",
            height=24
        )
        self.foot_logger_le = addWidget( QtWidgets.QLineEdit(),
            self.foot,
            QtWidgets.QHBoxLayout(),
            style_sheet="background-color: rgb(255, 255, 255); color: rgb(0, 0, 0);",
            text_margins=(8,0,8,0),
            height=20,
            text=u"請選擇 OCMS點位資訊檔案(XML) 的存放位置 ...",
            text_alignment=(QtCore.Qt.AlignVCenter | QtCore.Qt.AlignLeft),
            read_only=True
        )
        self.foot_btn = addWidget( QtWidgets.QPushButton(),
            self.foot,
            QtWidgets.QHBoxLayout(),
            width=16,
            icon=QtGui.QIcon(getIconFullPath("arrow_up.png")),
            icon_size=QtCore.QSize(8,8),
            flat=True
        )

        self.foot_btn.setShortcut(self.foot_btn.tr("Alt+F7"))

    def OnNewButtonClicked(self):
        self.__creator.process()
        # cmds.confirmDialog()
        pass

    def OnLoadButtonClicked(self):
        self.__importer.process()

    def OnCancelButtonClicked(self):
        self.close()





# A special widget fot show label with horizotal line.
class Splitter(QtWidgets.QWidget):
    def __init__(self):
        self.text = None
        self.frame_style = None

        QtWidgets.QWidget.__init__(self)

        # self.setMinimumHeight(2)
        self.setLayout(QtWidgets.QHBoxLayout())
        self.layout().setContentsMargins(0,0,0,0)
        self.layout().setSpacing(0)
        self.layout().setAlignment(QtCore.Qt.AlignVCenter)

        self.first_line = QtWidgets.QFrame()
        self.first_line.setFrameStyle(QtWidgets.QFrame.HLine)
        self.first_line.setLineWidth(1)
        self.first_line.setStyleSheet('background-color: rgb(97, 97, 97);')
        self.layout().addWidget(self.first_line)

    def setText(self, text):
        if self.text is not None:
            self.text = text
            self.text_width = QtGui.QFontMetrics(self.font)
            self.width = self.text_width.width(self.text) + 6
            self.label.setText(self.text)
            self.label.setMaximumWidth(self.width)
            return

        self.text = text
        self.first_line.setMaximumWidth(16)

        self.font = QtGui.QFont()
        self.font.setBold(True)

        self.text_width = QtGui.QFontMetrics(self.font)
        self.width = self.text_width.width(self.text) + 30

        self.label = QtWidgets.QLabel()
        self.label.setText(self.text)
        self.label.setFont(self.font)
        self.label.setMaximumWidth(self.width)
        self.label.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
        self.layout().addWidget(self.label)

        self.second_line = QtWidgets.QFrame()
        self.second_line.setFrameStyle(QtWidgets.QFrame.HLine)
        self.second_line.setLineWidth(1)
        self.second_line.setStyleSheet('background-color: rgb(97, 97, 97);')
        self.layout().addWidget(self.second_line)




def getIconFullPath(name):
    return "{}\\icons\\ocms\\{}".format(os.path.abspath(""), name)


window = None
def createDialog():
    import time
    localtime = time.localtime()
    result = time.strftime("%Y-%m-%d %I:%M:%S %p", localtime)
    print("Script has excute in ... {}".format(result))
    deleteDialog()
    global window
    if dialog is None:
        dialog = Dialog()
    dialog.show()

def deleteDialog():
    global window
    if dialog is None:
        return

    dialog.deleteLater()
    dialog = None

createDialog()