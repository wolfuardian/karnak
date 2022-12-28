import sys

import maya.OpenMayaUI as omui
from PySide2 import QtWidgets, QtCore, QtGui
from shiboken2 import wrapInstance

from python.eil.util import common


def maya_main_window():
    """
    Return the Maya main window widget as a Python object
    """
    maya_main_ptr = omui.MQtUtil.mainWindow()
    if sys.version_info.major >= 3:
        return wrapInstance(int(maya_main_ptr), QtWidgets.QWidget)
    else:
        return wrapInstance(long(maya_main_ptr), QtWidgets.QWidget)


class QtDefaultWidget(QtWidgets.QWidget):
    """
    QWidget auto-delete Attribute settings.
    """

    def __init__(self, parent=None, *args, **kwargs):
        super(QtDefaultWidget, self).__init__(parent=parent, *args, **kwargs)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)


class _FrameButton(QtWidgets.QWidget):
    """
    Button section of the FrameLayout.
    The open and closed state of the FrameLayout is held on the button side
    """

    def __init__(self, label='', parent=None):
        super(_FrameButton, self).__init__(parent)
        self.__close_pix = QtGui.QPixmap(':/teRightArrow.png')
        self.__open_pix = QtGui.QPixmap(':/teDownArrow.png')

        self.setMinimumSize(288, 32)
        self.setSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Fixed)
        self.setAutoFillBackground(True)

        # self.setBackgroundColor((93, 93, 93))  # Light
        self.setBackgroundColor((60, 60, 60))  # Dark

        layout = QtWidgets.QHBoxLayout()
        layout.setContentsMargins(5, 0, 5, 0)
        layout.setAlignment(QtCore.Qt.AlignLeft | QtCore.Qt.AlignVCenter)
        self.setLayout(layout)

        self.__icon = QtWidgets.QLabel()
        self.__icon.setPixmap(self.__close_pix)
        layout.addWidget(self.__icon)
        self.__label = QtWidgets.QLabel(unicode(' ' + label))

        layout.addWidget(self.__label)

        self.__toggle = True
        self.__collapsed = common.Subject()
        self.__expanded = common.Subject()
        self.__collapsed.listen.add(lambda: self.__icon.setPixmap(self.__close_pix))
        self.__expanded.listen.add(lambda: self.__icon.setPixmap(self.__open_pix))

    @property
    def toggle(self):
        """
        Programmatic processing for status acquisition
        """
        return self.__toggle

    @toggle.setter
    def toggle(self, value):
        """
        Process for programmed state setting
        """
        self.__toggle = value
        self.__expanded.emit() if self.__toggle else self.__collapsed.emit()

    @property
    def collapsed(self):
        """
        Register function when FrameLayout is closed
        """
        return self.__collapsed.listen

    @property
    def expanded(self):
        """
        Register function when a FrameLayout is opened
        """
        return self.__expanded.listen

    def setFont(self, font):
        """
        Font settings
        """
        self.__label.setFont(font)

    def setText(self, text):
        """
        Text settings
        """
        self.__label.setText(text)

    def setBackgroundColor(self, color):
        _p = self.palette()
        _p.setColor(self.backgroundRole(), QtGui.QColor(color[0], color[1], color[2]))
        self.setPalette(_p)

    def mouseReleaseEvent(self, *args, **kwargs):
        """
        FrameLayout button click decision.
        """
        self.__toggle = not self.__toggle
        self.__expanded.emit() if self.__toggle else self.__collapsed.emit()


class FrameLayout(QtWidgets.QWidget):
    """
    FrameLayout created by PySide.
    """

    def __init__(self, parent=None):
        super(FrameLayout, self).__init__(parent)

        self.setSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Minimum)
        layout = QtWidgets.QVBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        layout.setAlignment(QtCore.Qt.AlignTop)
        self.setLayout(layout)

        self.__frame_btn = _FrameButton('Frame Button')
        self.__frame_btn.setObjectName('frame_btn')
        self.__frame_btn.setFont(QtGui.QFont("Microsoft JhengHei", 10, QtGui.QFont.Bold))
        self.__frame_btn.collapsed.add(self.__on_collapsed)
        self.__frame_btn.expanded.add(self.__on_expanded)

        self.__frame = QtWidgets.QWidget(self)
        self.__frame.setObjectName('frame_widget')

        self.__frame_layout = QtWidgets.QVBoxLayout(self.__frame)
        self.__frame_layout.setObjectName('frame_layout')
        # self.__frame_layout.setContentsMargins(8, 8, 0, 8)
        self.__frame_layout.setContentsMargins(0, 0, 0, 0)
        self.__frame_layout.setSpacing(0)

        self.layout().addWidget(self.__frame_btn)
        self.layout().addWidget(self.__frame)

        # self.__frame_btn.toggle = True

    @property
    def frame_btn(self):
        """
        Access to _FrameButton
        """
        return self.__frame_btn

    @property
    def frame_layout(self):
        """
        Access to Layout section
        """
        return self.__frame_layout

    def collapsed(self):
        self.__on_collapsed()

    def __on_collapsed(self):
        """
        Hide Item in Layout when _FrameButton is closed
        """
        for item in self.__frame.findChildren(QtWidgets.QWidget):
            item.setVisible(False)

    def __on_expanded(self):
        """
        Show Item in Layout when _FrameButton is open
        """
        for item in self.__frame.findChildren(QtWidgets.QWidget):
            item.setVisible(True)
